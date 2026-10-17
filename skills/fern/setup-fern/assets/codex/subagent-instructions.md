## Subagent delegation

Proactively delegate independent work when parallelism can save time or
improve quality. Choose roles according to the work needed; do not require
a fixed sequence of specialists for every task.

Give each subagent a bounded outcome, relevant context, clear file or
responsibility ownership, and the evidence expected in its response.
Reuse an existing agent for related follow-up work when appropriate.

For parallel implementation, assign disjoint ownership where practical.
Tell workers that they share the checkout with others, must preserve
others' edits, and should adapt to changes they encounter. Resolve
overlapping edits before continuing dependent work.

Use roles as follows:

- explorer: answer a focused question about the codebase.
- worker: implement a scoped change with explicit ownership.
- architect: resolve consequential, unresolved architecture decisions.
  This role analyzes only and must not delegate or coordinate other agents.
- docs_researcher: resolve version-sensitive technical questions using
  official sources.
- debugger: investigate a reported failure and recommend a focused fix.
- validator: run relevant checks and report evidence and failure causes.
- reviewer: provide an independent review of the supplied work.
- visual_reviewer: assess visual requirements against accessible evidence.

Preserve each role's instructions and boundaries. Diagnosis and validation
do not authorize implementing fixes; review roles remain read-only.
Permissions are inherited from the parent session.

When spawning built-in explorers, use model="gpt-6-luna" and
reasoning_effort="high", unless the user specifies otherwise. If an explicit
model override requires a fresh or limited-history context, use that mode
and provide the context needed for the task. Let configuration and custom
agent files supply the other model and reasoning defaults.

Continue independent work while delegated tasks run. Collect results needed
for the requested outcome before finalizing. The primary agent owns
coordination, integration, conflict resolution, and final reporting within
the user's authorized scope. Distinguish inspected facts, executed checks,
and unverified conclusions.
