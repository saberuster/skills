"""Harness regression checks with synthetic responses, never agent/model runs."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import behavior_trials as trials

ROOT = Path(__file__).resolve().parents[1]


class DelegationFixtureTests(unittest.TestCase):
    """Exercise real case preparation, without inferring agent behavior."""

    def test_selected_cases_copy_policy_and_keep_assessments_outside_workspace(self):
        cases = [
            "fern-delegation-short-audit",
            "fern-delegation-fresh-context",
            "fern-delegation-plan",
        ]
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "trials"
            prepared = trials.prepare(output, cases)
            self.assertEqual({Path(path).name for path in prepared}, set(cases))
            asset = "assets/codex/user-instructions.md"
            source = ROOT / "skills/fern/setup-fern" / asset
            for path in prepared:
                trial = Path(path)
                with self.subTest(case=trial.name):
                    inputs = trials.read_json(trial / "input.json")
                    self.assertNotIn("evaluation", inputs)
                    self.assertFalse((trial / "workspace/evaluator.json").exists())
                    self.assertEqual(
                        (trial / "workspace/skill" / asset).read_bytes(),
                        source.read_bytes(),
                    )
                    manifest = trials.read_json(trial / "manifest.json")
                    self.assertEqual(
                        trials.hashes(trial / "workspace"), manifest["initial_hashes"]
                    )
            turns = trials.read_json(output / "fern-delegation-plan/input.json")[
                "turns"
            ]
            self.assertEqual(len(turns), 2)
            audit = output / "fern-delegation-short-audit/workspace"
            versions = [
                trials.read_json(audit / name)["version"]
                for name in ("release.json", "package.json")
            ]
            self.assertEqual(versions, ["1.4.2", "1.4.2"])
            self.assertEqual(
                (audit / "docs/release.txt").read_text(), "Current release: 1.4.1\n"
            )


class BehaviorTrialsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "source"
        self.spec_path = self.root / "examples/behavior-smoke.json"
        self.spec_path.parent.mkdir()
        shutil.copyfile(trials.SPEC, self.spec_path)
        shutil.copytree(ROOT / "examples/fixtures", self.spec_path.parent / "fixtures")
        source_packages = trials.skill_packages(ROOT)
        for case in trials.read_json(self.spec_path)["cases"]:
            package = self.source / source_packages[case["skill"]].relative_to(ROOT)
            (package / "references").mkdir(parents=True, exist_ok=True)
            (package / "SKILL.md").write_text("Synthetic complete source\n")
            (package / "references/detail.txt").write_text("Bundled resource\n")
        self.run = self.root / "run"
        trials.prepare(self.run, source_root=self.source, spec_path=self.spec_path)

    def evidence(
        self, case, *, missing=False, failed=False, incomplete=False, unsupported=False
    ):
        trial = self.run / case
        inputs = trials.read_json(trial / "input.json")
        transcript = {
            "turns": [
                {
                    "request": request,
                    "response": "Synthetic response for harness tests.",
                }
                for request in inputs["turns"]
            ]
        }
        if incomplete:
            transcript["turns"].pop()
        criteria = trials.read_json(trial / "evaluator.json")["criteria"]
        assessment = {
            "evaluator": "synthetic harness test evaluator",
            "criteria": {
                item["id"]: {
                    "status": "failed" if failed else "passed",
                    "reason": "Synthetic assessment exercises result aggregation only.",
                    "evidence": ["Synthetic transcript; no actual behavior claim."],
                }
                for item in criteria
            },
        }
        if missing:
            assessment["criteria"].pop(criteria[0]["id"])
        if unsupported:
            assessment["criteria"][criteria[0]["id"]]["evidence"] = []
        transcript_path = self.root / "transcript.json"
        assessment_path = self.root / "assessment.json"
        trials.write_json(transcript_path, transcript)
        trials.write_json(assessment_path, assessment)
        return trials.record(
            trial,
            transcript_path,
            assessment_path,
            "unittest synthetic runner",
            "no model",
        )

    def test_fixture_isolation_and_full_source_copy(self):
        baseline = trials.hashes(self.source)
        trial = self.run / "reflect-proposal"
        self.assertEqual(
            (trial / "workspace/skill/references/detail.txt").read_text(),
            "Bundled resource\n",
        )
        (trial / "workspace/sources/csv-export/SKILL.md").write_text("Changed\n")
        self.assertEqual(trials.hashes(self.source), baseline)
        self.assertNotEqual(
            trials.hashes(trial / "workspace"), trials.hashes(trial / "before")
        )
        inputs = trials.read_json(trial / "input.json")
        self.assertNotIn("evaluation", inputs)
        self.assertFalse((trial / "workspace/evaluator.json").exists())
        self.assertEqual(
            len(list(self.run.iterdir())),
            len(trials.read_json(self.spec_path)["cases"]),
        )

    def test_prepare_never_overwrites(self):
        baseline = trials.hashes(self.run)
        with self.assertRaisesRegex(ValueError, "overwrite"):
            trials.prepare(self.run, source_root=self.source)
        self.assertEqual(trials.hashes(self.run), baseline)

    def test_delegation_requires_all_turns_and_assessment_evidence(self):
        # Synthetic responses exercise evidence accounting, not the policy.
        self.assertEqual(
            self.evidence("fern-delegation-plan", incomplete=True)["outcome"],
            "unverified",
        )
        self.assertEqual(
            self.evidence("fern-delegation-short-audit", missing=True)["outcome"],
            "unverified",
        )
        self.assertEqual(
            self.evidence("fern-delegation-fresh-context", unsupported=True)["outcome"],
            "unverified",
        )

    def test_nested_skill_preparation_records_actual_source_and_resources(self):
        trial = self.run / "docs-schema"
        manifest = trials.read_json(trial / "manifest.json")
        self.assertEqual(
            Path(manifest["source_path"]),
            (self.source / "skills/fern/technical-writing").resolve(),
        )
        self.assertIn("references/detail.txt", manifest["source_hashes"])
        self.assertEqual(
            (trial / "workspace/skill/references/detail.txt").read_text(),
            "Bundled resource\n",
        )

    def test_unicode_fixture_round_trip_and_unchanged_record(self):
        spec = trials.read_json(self.spec_path)
        case = next(c for c in spec["cases"] if c["id"] == "agents-review")
        content = "# Project Overview\n\n\u4e2d\u6587\u6b63\u6587\u3002\n"
        case["files"]["AGENTS.md"] = content
        trials.write_json(self.spec_path, spec)
        self.run = self.root / "unicode-run"
        trials.prepare(
            self.run,
            cases=["agents-review"],
            source_root=self.source,
            spec_path=self.spec_path,
        )
        trial = self.run / "agents-review"
        for tree in ("workspace", "before"):
            self.assertEqual(
                (trial / tree / "AGENTS.md").read_bytes(), content.encode("utf-8")
            )
        result = self.evidence("agents-review")
        self.assertEqual(result["outcome"], "passed")
        self.assertEqual(result["file_changes"], [])
        self.assertEqual(
            (trial / "after/AGENTS.md").read_bytes(), content.encode("utf-8")
        )

    def test_semantic_assessment_missing_cannot_pass(self):
        result = self.evidence("reflect-proposal", missing=True)
        self.assertEqual(result["outcome"], "unverified")
        self.assertEqual(result["file_changes"], [])

    def test_failed_semantic_assessment_cannot_pass(self):
        self.assertEqual(
            self.evidence("agents-review", failed=True)["outcome"], "failed"
        )

    def test_positive_assessment_without_evidence_cannot_pass(self):
        self.assertEqual(
            self.evidence("reflect-proposal", unsupported=True)["outcome"], "unverified"
        )

    def test_incomplete_multiturn_transcript_cannot_pass(self):
        result = self.evidence("talk-acceptance", incomplete=True)
        self.assertEqual(result["outcome"], "unverified")
        self.assertFalse(result["transcript_complete"])

    def test_real_forbidden_file_diff_overrides_positive_assessment(self):
        trial = self.run / "agents-review"
        (trial / "workspace/docs/AGENTS.md").write_text("Unauthorized rewrite\n")
        result = self.evidence("agents-review")
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["file_changes"][0]["path"], "docs/AGENTS.md")
        self.assertEqual(result["file_changes"][0]["kind"], "modified")
        self.assertEqual(
            (trial / "after/docs/AGENTS.md").read_text(), "Unauthorized rewrite\n"
        )

    def test_docs_require_edit_and_preserved_sections(self):
        self.assertEqual(self.evidence("docs-schema")["outcome"], "failed")

    def test_scoped_docs_change_preserves_real_unrelated_bytes(self):
        path = self.run / "docs-schema/workspace/docs/jobs.md"
        path.write_text(
            path.read_text().replace(
                "defaults to 5 and permits negative integers",
                "is an integer, defaults to 3, and has minimum 0",
            ),
            newline="\n",
        )
        self.assertEqual(self.evidence("docs-schema")["outcome"], "passed")

    def test_docs_history_deletion_overrides_positive_assessment(self):
        path = self.run / "docs-schema/workspace/docs/jobs.md"
        path.write_text("# Jobs\n\n## Configuration\n\nretry_limit defaults to 3.\n")
        self.assertEqual(self.evidence("docs-schema")["outcome"], "failed")

    def test_docs_reject_changes_outside_configuration(self):
        mutations = {
            "title": lambda text: text.replace("# Jobs", "# New title"),
            "preamble": lambda text: text.replace(
                "# Jobs\n", "# Jobs\nNew preamble.\n"
            ),
            "append": lambda text: text + "\nNew out-of-scope content.\n",
            "h1": lambda text: text.replace(
                "## Cancellation guarantee",
                "# Unauthorized new top-level section\n\n## Cancellation guarantee",
            ),
            "reorder": lambda text: (
                text.split("## Cancellation guarantee")[0]
                + "## Historical design"
                + text.split("## Historical design")[1]
                + "\n## Cancellation guarantee"
                + text.split("## Cancellation guarantee")[1].split(
                    "## Historical design"
                )[0]
            ),
            "duplicate": lambda text: (
                text
                + "\n## Cancellation guarantee"
                + text.split("## Cancellation guarantee")[1].split(
                    "## Historical design"
                )[0]
            ),
        }
        for name, mutate in mutations.items():
            with self.subTest(mutation=name):
                self.run = self.root / ("run-" + name)
                trials.prepare(self.run, ["docs-schema"], self.source, self.spec_path)
                path = self.run / "docs-schema/workspace/docs/jobs.md"
                corrected = path.read_text().replace(
                    "defaults to 5 and permits negative integers",
                    "is an integer, defaults to 3, and has minimum 0",
                )
                path.write_text(mutate(corrected), newline="\n")
                self.assertEqual(self.evidence("docs-schema")["outcome"], "failed")

    def test_fenced_heading_text_is_inside_configuration(self):
        path = self.run / "docs-schema/workspace/docs/jobs.md"
        corrected = path.read_text().replace(
            "defaults to 5 and permits negative integers",
            "is an integer, defaults to 3, and has minimum 0",
        )
        path.write_text(
            corrected.replace(
                "## Cancellation guarantee",
                "```text\n# Literal heading\n## Literal subheading\n```\n\n"
                "## Cancellation guarantee",
            ),
            newline="\n",
        )
        self.assertEqual(self.evidence("docs-schema")["outcome"], "passed")

    def test_malformed_transcript_rejected_without_record(self):
        transcript = self.root / "malformed.json"
        assessment = self.root / "assessment.json"
        trials.write_json(transcript, {"turns": ["not an object"]})
        trials.write_json(assessment, {"criteria": {}})
        with self.assertRaisesRegex(ValueError, "turns"):
            trials.record(
                self.run / "reflect-proposal",
                transcript,
                assessment,
                "test",
                "no model",
            )
        self.assertFalse((self.run / "reflect-proposal/result.json").exists())

    def test_mock_mutation_log_fails_even_when_packages_unchanged(self):
        log = self.run / "skills-local-edits/workspace/evidence/commands.jsonl"
        log.parent.mkdir()
        log.write_text(json.dumps({"args": ["update"], "mutation": True}) + "\n")
        result = self.evidence("skills-local-edits")
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["file_changes"][0]["path"], "evidence/commands.jsonl")

    def test_source_byte_drift_prevents_attribution(self):
        (self.source / "skills/fern/reflect/references/detail.txt").write_text(
            "New source revision\n"
        )
        result = self.evidence("reflect-proposal")
        self.assertEqual(result["outcome"], "unverified")
        self.assertEqual(result["source_drift"][0]["path"], "references/detail.txt")

    def test_unrelated_source_change_does_not_invalidate_trial(self):
        (self.source / "skills/fern/technical-writing/SKILL.md").write_text(
            "Unrelated\n"
        )
        self.assertEqual(self.evidence("reflect-proposal")["outcome"], "passed")

    def test_definition_and_fixture_hashes_recorded(self):
        manifest = trials.read_json(self.run / "skills-local-edits/manifest.json")
        spec = trials.read_json(self.spec_path)
        case = next(c for c in spec["cases"] if c["id"] == "skills-local-edits")
        self.assertEqual(
            manifest["definition_hash"], trials.definition_hash(case, self.spec_path)
        )
        self.assertIn("references/detail.txt", manifest["source_hashes"])

    def test_case_definition_drift_cannot_pass(self):
        spec = trials.read_json(self.spec_path)
        case = next(c for c in spec["cases"] if c["id"] == "reflect-proposal")
        case["context"] = "Changed source case"
        trials.write_json(self.spec_path, spec)
        result = self.evidence("reflect-proposal")
        self.assertEqual(result["outcome"], "unverified")
        self.assertTrue(result["definition_drift"])

    def test_result_cannot_be_overwritten(self):
        self.evidence("reflect-proposal")
        with self.assertRaisesRegex(ValueError, "already recorded"):
            self.evidence("reflect-proposal")

    def test_links_rejected_from_source(self):
        linked = self.source / "skills/fern/reflect/outside.txt"
        try:
            linked.symlink_to(self.root / "sentinel.txt")
        except OSError:
            self.skipTest("Host does not permit creating test symbolic links")
        with self.assertRaisesRegex(ValueError, "Links"):
            trials.hashes(self.source / "skills/fern/reflect")


if __name__ == "__main__":
    unittest.main()
