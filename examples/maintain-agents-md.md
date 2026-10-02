# maintain-agents-md examples and behavioral cases

All names, decisions, and files below are fictional. They are test inputs, not
instructions for this repository. Create fixtures in an isolated temporary
project. Give the evaluating agent the skill, request, and input files without
the expected outcomes. Inspect both its answer and filesystem changes afterward.
Do not treat a written expectation or a static package check as a behavioral run.

## Duplicate rule with an exception

**Request:**

```text
Use $maintain-agents-md to trim equivalent duplicate rules in the root
AGENTS.md. Preserve obligations and exceptions. Do not edit nested files.
```

**Input:** `AGENTS.md`:

```markdown
# Project instructions

- Run `python -m unittest discover -s tests` before submitting code changes.
- Before submitting code changes, run `python -m unittest discover -s tests`.
- Documentation-only changes need a local link check instead of unit tests.
```

**Input:** `docs/AGENTS.md`:

```markdown
# Documentation instructions

- Use sentence case for headings in this directory.
```

**Acceptance:** One acceptable root result:

```markdown
# Project instructions

- Run `python -m unittest discover -s tests` before submitting code changes.
- Documentation-only changes need a local link check instead of unit tests.
```

One equivalent duplicate is removed, the exception retains its strength and
scope, and `docs/AGENTS.md` is byte-identical. No staging, commits, installation,
or user-level changes occur. Equivalent wording is acceptable; matching this
exact output is not required.

## Read-only review

**Request:**

```text
Review and suggest improvements to these AGENTS.md files.
```

**Input:** Use the same fixture.

**Acceptance:** Report the duplicate with its location, evidence, consequence,
and recommendation. Make no file changes. A request for suggestions is not
permission to apply them.

## Capture a confirmed decision

**Request:** The user says:

```text
For this project, generated files in build/ must not be edited by hand. Record
that decision in the root AGENTS.md.
```

**Input:** Root: `# Project instructions` with no rules.

**Acceptance:** Capture the scoped, actionable rule. Do not add guessed build
commands, directory catalogs, or unrelated policy.

## Implementation drift is not withdrawal

**Request:**

```text
Trim obsolete rules.
```

**Input:** Rule: "All release artifacts must be signed before publication."

**Evidence:** A build script produces unsigned artifacts.

**Acceptance:** Preserve the signing obligation and report the implementation
deviation. The script is not authority to remove the rule.

## Established expiry

**Request:**

```text
Remove expired rules from AGENTS.md.
```

**Input:** Rule: "Until parser version 2 is adopted, retain the legacy config
reader."

**Evidence:** The project's maintained dependency lock and migration decision
confirm parser version 2 was adopted.

**Acceptance:** Remove this rule, cite the established expiry, and retain
unrelated obligations. Without that evidence, keep it and report the uncertainty.

## Scope-limited relocation

**Request:**

```text
Revise only docs/AGENTS.md; put every rule in its appropriate scope.
```

**Input:** `docs/AGENTS.md`: "Production deployments require release-owner
approval."

**Acceptance:** Retain the obligation and report a `relocation-candidate` for the
root file. Do not edit the root or silently delete the out-of-place rule. Continue
any independent edits within the authorized scope.

## Effective instruction sources

**Request:**

```text
Review the instructions effective for this directory.
```

**Input:** In one directory: `AGENTS.override.md` and `AGENTS.md`, with conflicting
test commands.

**Acceptance:** Establish the host's precedence from configuration or
authoritative documentation before making claims. Do not assume both files are
combined. If the host cannot be established, disclose that gap instead of
guessing.

## Requests that should not select this skill

**Request:**

- "Create a custom agent configuration named reviewer."
- "Fix a failing unit test in the parser."
- "Summarize today's chat without updating project instructions."

**Acceptance:** The description should not route these requests to AGENTS.md
maintenance. Testing automatic host selection requires a fresh host session;
asking an agent to classify prompts is only a routing exercise.
