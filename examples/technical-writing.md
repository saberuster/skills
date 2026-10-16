# technical-writing examples and behavioral cases

All projects, files, and decisions below are fictional. Create each fixture in
an isolated temporary project. Give the evaluating agent the skill, request,
and inputs without the acceptance text. Inspect its response and filesystem
diff afterward. These expectations are not recorded executions; static package
checks do not establish model behavior or host discovery.

## Create a repository document

**Request:**

```text
Use $technical-writing to write docs/invitations.md for maintainers. Document the
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

## Write a substantial document with a known structure

**Request:**

```text
Use $technical-writing to write docs/worker-operations.md for on-call maintainers.
Follow docs/service-operations.md's headings: Startup, Configuration, Monitoring,
and Recovery. Use the supplied worker commands, schema, and recovery runbook.
```

**Input:** The reference document establishes the maintained structure. The
worker sources supply enough verified material for several pages, including
startup prerequisites, configuration defaults, health checks, and recovery
steps. The audience, destination, scope, and section order are clear.

**Acceptance:** Inspect the reference and relevant sources, then write the
requested artifact directly using the established headings. Length alone does
not require a separate outline or approval step. Preserve exact commands and
identifiers, identify any remaining evidence limits, and check relevant links
and command examples. Report actual checks without claiming runtime execution
unless it occurred.

## Write a clear task guide

**Request:**

```text
Use $technical-writing to turn the supplied notes into docs/download-snapshot.md
for new Birch operators. Help them download a project snapshot and keep the
unresolved retention decision visible.
```

**Input:** Operators know the project interface but have not encountered
snapshots. A snapshot is a saved copy of project metadata; it excludes uploaded
files. Accepted steps: open **Snapshots**, select **Create snapshot**, wait for
Birch to display **Ready** automatically, then select **Download**. If the
browser asks for a destination, choose a writable folder. Success means the
downloaded archive is present there. Snapshot retention is undecided. The local
`docs/troubleshooting.md` has a `Download errors` heading and instructions for
download failures. The notes have a vague `Stuff` heading, repeat that creating
a snapshot creates a snapshot, call the download control both a button and an
export action, link to troubleshooting as `click here`, and describe it only as
the green control on the right. No executable tool or runtime evidence is
supplied.

**Acceptance:** Create the requested guide with its goal or first useful action
near the start. Explain snapshot for this audience, preserve its contents and
exclusions, and use precise wording, clear actors, consistent interface terms,
and focused paragraphs without empty repetition. Number the operator's actions;
present the automatic **Ready** state as a system result rather than a separate
operator action. Put the destination condition before its instruction. Use
informative headings and a descriptive link to the valid troubleshooting
section. Identify controls in text without depending solely on color, position,
or an image. Preserve the retention unknown and distinguish documented expected
results from an executed download. Equivalent wording and useful structures are
acceptable; no fixed sentence length, extra document, or approval step is
required.

## Apply a local revision

**Request:**

```text
Use $technical-writing to correct only the configuration section of docs/jobs.md.
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
Use $technical-writing to review docs/invitations.md for requirements readiness.
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

**Ordinary review variation:** Use the same input with this request:

```text
Use $technical-writing to review docs/invitations.md for contradictions and
unclear requirements. Report findings without editing files.
```

**Acceptance:** Report the contradiction and unresolved decision with evidence
and focused corrections. No readiness assessment is requested or required by
the project, so omit an automatic Ready, Conditionally ready, or Not ready
rating. Preserve all files.

## Consolidate maintained guidance

**Request:**

```text
Use $technical-writing to consolidate docs/quickstart.md into docs/setup.md and
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
useful navigation and historical decisions. Draft an outline only if the scope
or resulting structure needs clarification; the size of the reorganization
alone does not require one. Check affected links and report actual verification;
do not rewrite historical rationale as though current guidance had always
applied.

## Check navigation after copying one package

**Request:**

```text
Use $technical-writing to revise only source/skills/atlas/README.md for standalone
distribution. Check its navigation in the repository and after copying just
the atlas package. The publisher identifies https://docs.example.com/atlas/setup
as the canonical setup reference; network access is unavailable in this case.
```

**Input:** In a temporary fixture, `source/skills/atlas/README.md` has a Setup
link to `../../docs/setup.md` and a Usage link to `references/usage.md`. Both
targets exist in the source tree. Copy only `source/skills/atlas/` to
`delivery/atlas/`; the destination contains the README and bundled usage
document, with no copy of `source/docs/`. Give the agent this fixture root and
the request above. This fixture is a local copy, not a real skill installation.

**Acceptance:** Observe that both original local links resolve in the source
repository, but only `references/usage.md` resolves in the package copy. Revise
the source README to retain the bundled usage reference and use the supplied
canonical setup URL. Copy the revised package into a fresh delivery directory
and check navigation there. Report the local path checks actually performed
and the external URL's unverified access; do not claim a successful network
check or install the package into a user profile. Preserve the source setup
document and unrelated package content. This case applies to distribution;
ordinary repository documents can retain valid repository-relative links.

## Compare a contract with implementation

**Request:**

```text
Use $technical-writing to compare docs/jobs.md with this checkout's cancellation
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
and historical results from the intended contract. Treat retention as an open
decision and identify unknowns. Report the findings and supporting evidence in
proportion to this focused comparison; a per-capability matrix is optional when
it makes the result clearer. Identify the relevant gap or next verification
step without requiring a repeated evidence checklist for every capability.
Preserve all files; do not weaken the contract, repair code, or create an
unrequested roadmap.

## Preserve an unresolved design choice

**Request:**

```text
Use $technical-writing to revise docs/storage-rfc.md with the supplied benchmark
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
