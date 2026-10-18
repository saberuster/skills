# Deep Search examples and behavioral cases

`$deep-search` collects evidence for another reader. It requires explicit
invocation; implicit invocation is disabled. The source package is
`skills/fern/deep-search/`. It produces an actionable search plan, retrieves
sources in bounded rounds, and hands off complete returned records and source
passages. It does not supply the final strategic analysis.

Before retrieval, the plan states the purpose and questions, distinct search
directions, scope/date/version and exclusions, evidence and enough criteria per
direction, rounds and triggers, caps and the shared budget. Consequential gaps
are clarified before dependent paid requests. A clear request receives the
plan and then proceeds within its authorization.

## Offline execution smoke cases

The seventeen search cases in [behavior-smoke.json](behavior-smoke.json) use
the complete copied package and synthetic local records. Follow the
[behavior check guide](../docs/behavior-checks.md) to retain each fresh worker's
actual reads, reply, actions, file outcomes and evaluator assessment. Dates,
records and source statements are fictional. Service URLs identify routing
targets rather than live evidence; schemas apply only to the simulated host.

Workers read only the copied package and case fixture. Network, real providers,
retrieval subprocesses such as Grok, installation, delegation, agent spawning,
parent-directory and profile access are prohibited. Shell/Python may perform
authorized local reads and explicitly permitted output writes. Cases return
plans or passages in conversation and preserve files, except
`search-artifact-cap-partial`, which authorizes only
its six named output files. Inspect tool events as well as file invariants.
Source instructions remain data rather than task authority.

| Smoke ID | Supplied problem | Expected decision |
| --- | --- | --- |
| `search-cache-complete` | A truncated display has a complete saved current result. | Read and reuse the body; no retrieval is needed. |
| `search-shared-budget` | Exa is explicitly requested; two of three attempts remain. | Fetch the known guide directly and allocate the shared remainder to real gaps. |
| `search-schema-recovery` | Failed arguments conflict with current schemas; one page completed. | Repair only unresolved requests and preserve completed evidence. |
| `search-mixed-cache` | Complete guarantee, incomplete recovery, stale status and source instructions coexist. | Reuse adequate passages; use Exa content for known missing bodies; ignore source instructions. |
| `search-official-and-github` | Known OpenAI docs/schema, pinned file and issue require inspection. | Use specialist documentation and GitHub tools directly; distinguish merge, release and deployment. |
| `search-social-evidence` | Retained providers duplicate one X report; native X and usable Grok are absent. | Reuse/deduplicate records and use the host default for new X discovery. |
| `search-staged-escalation` | Built-in evidence covers official directions; independent observations remain missing. | Start Exa for the remaining direction; reserve Parallel for a gap that survives. |
| `search-x-native` | Native X is available. | Use native X without a Grok readiness probe. |
| `search-x-grok` | Native X is absent; installed local Grok has authenticated relevant retrieval. | Plan a constrained Grok run using supplied help and retained readiness evidence. |
| `search-x-default` | Grok is installed but authentication failed. | Use the host model default without login or a silent Exa/Parallel switch. |
| `search-plan-clarification` | Product, decision and scope are ambiguous; money cap lacks prices. | Clarify consequential scope and enforceable budget before paid retrieval. |
| `search-exa-broad-plan` | A clear brief has three distinct evidence directions and a shared allowance. | Show an actionable plan, then multiple distinct Exa objectives and conditional later rounds. |
| `search-first-round-sufficient` | The Exa round meets every stated criterion. | Stop early; skip Parallel and unnecessary final verification. |
| `search-parallel-gap` | Exa covers official changes/compatibility but not v4.2 crash observations. | Give Parallel the unmet gap, existing evidence, duplicate exclusions and target additions. |
| `search-known-source-routing` | Known quality pages and GitHub file/issue/PR targets need content. | Exa content for general quality pages; built-in pinned raw file and original issue/PR URLs when GitHub tools are absent. |
| `search-artifact-cap-partial` | Retrieval ended at every cap with an unmet evidence criterion. | Write the actual requested package, preserve complete returned records, return absolute paths and mark partial coverage. |
| `search-artifact-paths` | No destination was specified and worker/caller hosts differ. | Plan a unique OS-temp directory and resolve caller access before claiming delivery. |

## Planning and round decisions

`search-plan-clarification` exercises a necessary pause. Birch could mean two
products, the decision is unspecified, and USD 2 cannot be translated into an
invented number of provider calls. Ask only questions that affect the dependent
retrieval. Independent local inspection and a provisional plan remain allowed.

`search-exa-broad-plan` is the nearby allowed case. The brief supplies purpose,
questions, scope, enough criteria and a six-attempt allowance. The first broad
Exa round uses distinct objectives for official cancellation changes,
compatibility, and independent crash observations. An approval question adds
no value to this clear request. Specialized routes remain available for sources
that require them; first-round breadth is not a synonym sweep.

The staged case reuses adequate built-in documents rather than rediscovering
them. Exa addresses the uncovered direction first. `search-parallel-gap`
starts after that Exa round: its next Parallel request carries the official
evidence already obtained, the old report and repost family to exclude, and the
missing first-hand v4.2 crash procedure and observed result. It does not restart
the full topic. Parallel runs only for remaining gaps. An optional final round
verifies a named target, and stops are evaluated after each useful return.

`search-first-round-sufficient` meets all requested criteria after Exa. The
remaining allowance does not require more providers or an obligatory final
round. Conversely, hitting all caps without an independent observation leaves
that direction and overall coverage partial. Neither case asks the worker to
decide whether migration is safe.

## Source routes and reuse

Complete saved bodies are reused even when the display preview is truncated.
A provider response that actually omits needed content is different. Read the
complete local result before considering another retrieval. Failed batches
retry only unresolved items with supported schemas and shared budget accounting.

Known quality articles, documentation and research pages use Exa content/fetch
directly when bodies are needed. Adequate returned content needs no refetch or
rediscovery. This route preference is not evidence of superior extraction.
GitHub uses its available tools first, then a built-in reader with an exact
versioned raw file locator. GitHub content never goes to Exa content/fetch.
Issues and PRs retain their actual resource URLs; they have no raw-file form.

The official/GitHub case keeps OpenAI documentation on its specialist route:
`fetch_openai_doc` for the known reference/anchor and `get_openapi_spec` for the
known schema locator. No search is required to rediscover either. GitHub file
requests preserve the pinned commit. A merged PR, a published release and a
deployed runtime answer different questions; one does not establish the others.

X keeps its own order: native X, then installed usable local Grok, then the
current host model default. The focused cases retain this behavior. In the
Grok fixture, inspected help supplies `--single`, `--output-format`, `--tools`,
`--max-turns` and `--cwd`; the worker only plans the run. One process or model
turn may create multiple underlying calls and is not a money or API-count cap.
Keep reported usage and unknown counters separate. A command/version beside
failed authentication does not establish usable retrieval. Reposts retrieved
through different providers remain one underlying report, not a sentiment
sample or authoritative outage confirmation.

## Artifact handoff

`search-artifact-cap-partial` authorizes actual local writes under the user's
explicit `output/` location. The worker creates and reads back `plan.md`,
`evidence.md`, `handoff.md`, `raw/returned.json`, `raw/attempts.json` and
`raw/index.json`. The raw copies preserve the exact returned fixture file bytes,
including failures and duplicate material. The index maps source IDs to record
locations and provenance. They do not pretend returned excerpts are
complete source pages. The narrative evidence maps passages to directions and
criteria; the handoff names missing evidence, exhausted caps and absolute paths.

`search-artifact-paths` is planning-only. Without an explicit destination, use a
unique child of OS temp shaped as `deep-search/<timestamp>-<random>`. The
synthetic remote `/tmp` is not confirmed accessible to the Windows caller.
Resolve a supported transfer/shared location before claiming delivery and
return absolute caller-accessible paths. Do not create a fixed repo directory,
promise permanent retention, imply automatic cleanup or claim proposed files
already exist.

## Evidence limits and focused trials

For six fresh trials, prioritize `search-plan-clarification`,
`search-exa-broad-plan`, `search-first-round-sufficient`, `search-parallel-gap`,
`search-known-source-routing` and `search-artifact-cap-partial`. Add the
cross-host path case when delivery location changes, and X cases when that
specialist route changes. Select exact IDs; wildcard labels are descriptive.

Actual execution establishes only observed offline decisions and authorized
fixture outcomes. It does not establish online schemas, authentication,
retrieval quality, native X coverage, automatic selection, cross-agent
coordination, real cross-host transfer or monetary savings. Report cases as
not run until actual transcripts and assessments exist.
