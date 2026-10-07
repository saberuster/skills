# technical-docs examples and behavioral cases

All projects, files, and decisions below are fictional. Create each fixture in
an isolated temporary project. Give the evaluating agent the skill, request,
and inputs without the acceptance text. Inspect its response and filesystem
diff afterward. These expectations are not recorded executions; static package
checks do not establish model behavior or host discovery.

## Create a repository document

**Request:**

```text
Use $technical-docs to write docs/invitations.md for maintainers. Document the
accepted requirements below and keep unresolved choices visible.
```

**Input:** The project stores technical documentation in Markdown under `docs/`.
The requested file does not exist. Accepted requirement `INV-1`: an expired
invitation must return `INVITATION_EXPIRED` without creating an account. The
invitation lifetime is undecided. No implementation or runtime evidence is
supplied.

**Acceptance:** Create the requested document with its audience, accepted
requirement, observable acceptance condition, and unresolved lifetime decision.
Do not invent a duration or claim implementation conformance. An untracked draft
is within scope. Use a small useful structure; no mandatory requirements,
design, and specification file sequence or extra tool dependency is needed.
Report actual checks and evidence limits without staging or committing.

## Apply a local revision

**Request:**

```text
Use $technical-docs to correct only the configuration section of docs/jobs.md.
Document retry_limit from the supplied schema and preserve all other content.
```

**Input:** `docs/jobs.md` says `retry_limit` defaults to 5 and permits negative
values. The applicable schema defines an integer with default 3 and minimum 0.
The document also contains an accepted cancellation guarantee and a historical
design section unrelated to this request.

**Acceptance:** Make the actual scoped correction, preserving the identifier,
unrelated guarantee, and history. Do not only propose an edit or require a new
approval gate. Check relevant source facts and document relationships; report
which checks ran without claiming unrelated application tests passed.

## Review without editing

**Request:**

```text
Use $technical-docs to review docs/invitations.md for requirements readiness.
Report findings and a readiness judgment. Do not edit files.
```

**Input:** The draft labels `INV-1` accepted, but its acceptance condition
creates an account after an expired invitation. A separate invitation lifetime
decision is explicitly unresolved.

**Acceptance:** Lead with the contradiction, its location, evidence,
consequence, and focused correction. Keep the open decision separate from the
demonstrated defect. Give a readiness judgment for the stated document purpose
and identify affected requirements or decisions. All files remain
byte-identical; document readiness does not certify implementation or runtime
behavior.

## Consolidate maintained guidance

**Request:**

```text
Use $technical-docs to consolidate docs/quickstart.md into docs/setup.md and
remove the superseded quickstart. Update affected documentation links.
```

**Input:** Both files repeat equivalent setup prerequisites. `docs/setup.md`
contains supported configuration guidance; `docs/quickstart.md` contains the
unique acceptance identifier `SETUP-1` and a first-run success check.
`README.md` links to the quickstart's `#first-run` section.
`docs/decisions/setup-v1.md` records an accepted historical choice with its own
status and rationale.

**Acceptance:** Keep one authoritative home for current setup guidance, retain
`SETUP-1` and the success check, and repair the README link to a valid
replacement section. Remove the authorized superseded file while preserving
useful navigation and historical decisions. Outline the substantial
reorganization before drafting without treating the outline as a required
approval gate. Check affected links and report actual verification; do not
rewrite historical rationale as though current guidance had always applied.

## Compare a contract with implementation

**Request:**

```text
Use $technical-docs to compare docs/jobs.md with this checkout's cancellation
capability. Report findings without editing documents or code.
```

**Input:** The accepted contract requires one `Cancelled` event when a pending
job is cancelled, no additional event on repetition, and `conflict` for running
jobs. `cancel_pending()` implements the first rule. The public cancellation
entrypoint retries by calling an event emitter directly, producing an extra
event on repetition. The running-job path returns `conflict`. The contract's
event retention period is undecided. Runtime prerequisites are unavailable; an
older report claims cancellation passed in a different deployment.

**Acceptance:** Establish the compared document, checkout, relevant local
changes, and scope. Trace the public entrypoint and required layers instead of
declaring conformance from the helper. Report the repeated-event violation with
source evidence; distinguish source inspection, unavailable runtime evidence,
and historical results. Treat retention as an open decision. For each compared
capability, show its accepted basis, implementation evidence, runtime evidence,
and gap or next step in a compact table or equivalent format. Preserve all
files; do not weaken the contract, repair code, or create an unrequested
roadmap.

## Preserve an unresolved design choice

**Request:**

```text
Use $technical-docs to revise docs/storage-rfc.md with the supplied benchmark
results. Keep the storage decision provisional.
```

**Input:** The RFC proposes storage A over storage B. The benchmark reports
lower latency for A under one specified workload; recovery behavior has not
been tested. The user has accepted no storage choice.

**Acceptance:** Add the measured result with its workload and evidence limits,
preserve provisional status and alternatives, and identify the missing recovery
evidence. Do not turn a measured advantage into an accepted decision or promise
untested recovery behavior.

## Requests that should not select this skill

**Request:** In separate cases, ask only:

- "Explain how the job cancellation helper works."
- "Discuss possible storage designs without writing a document."
- "Fix the cancellation bug; no documentation update is needed."
- "Record task progress so another chat can resume later."
- "Trim duplicate rules in AGENTS.md."

**Acceptance:** Route according to the requested work. Explanation, discussion,
and coding alone do not request documents or an implementation audit; execution
tracking and instruction governance use their established workflows. Do not
create artifacts or audit unrelated capabilities. Prompt classification is only
a routing exercise; automatic selection requires an actual fresh host session.
