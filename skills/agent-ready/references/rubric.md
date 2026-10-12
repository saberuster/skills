# Task-based readiness rubric

Use these dimensions as lenses on the sampled tasks, not mandatory architecture
layers. For a small script, a function, explicit arguments, and one reproducible
check can satisfy several dimensions. For a larger system, follow the relevant
runtime boundaries rather than reading everything. Record applicability and
uncertainty; do not compute a weighted score.

## 1. Navigation and bounded context

Can a new agent find the entrypoint, owner, applicable rules, and verification
command for the task without loading most of the project? Trace names and
references from a user action or command to implementation. Check whether
navigation notes describe the current code. Recommend a small map only if a
specific lookup is difficult; do not reward documents merely for existing.

## 2. Module boundaries and local changes

For one representative change, identify the files and contracts that must move
together and why. Distinguish necessary coordination from hidden coupling,
duplicated rules, and unexpected dependency direction. Inspect callers and
side effects; attractive folders or small files do not prove locality. Keep a
cohesive single module when extraction would add indirection without reducing
the task's reasoning or regression burden.

## 3. State ownership and contracts

Identify who creates, mutates, persists, and resets the state on the traced path.
Check invariants at actual boundaries, data formats, errors, ordering, retries,
and lifecycle where relevant. Look for competing sources of truth or implicit
initialization. Prefer one clear owner or one checked contract over introducing
interfaces for every object. A type declaration alone does not prove that
external inputs or transitions obey the contract.

## 4. Reproducible runtime and environment

Trace the documented command to executable configuration: versions, dependency
resolution, assets, secrets placeholders, working directory, and local services.
Check whether another authorized environment could reproduce it. Distinguish a
missing tool in the review host from a project setup defect. Treat supplied CI
logs as historical evidence; record actual attempts separately. Do not install
or contact services just to turn an unknown into a pass.

## 5. Observability and control

Can an agent observe the task's meaningful output and intermediate state, bound
the run, select a scenario, and stop or reset it safely? Look for useful errors,
correlation identifiers, inspectable state, and explicit inputs at relevant
boundaries. A command that exits zero without exposing the user-visible result
may not verify the task. Prefer a narrow diagnostic or fixture hook over a new
telemetry platform for a small local tool.

## 6. Defect reproduction and layered verification

Trace an assertion back to the entrypoint and result it claims to cover.
Separate pure rule tests, component or integration checks, end-to-end workflows,
visual checks, and human judgment. Identify mocks or direct calls that bypass
the actual failing UI, adapter, persistence, or lifecycle. Capture initial
state, versions, time assumptions, input/action sequence, expected and observed
results, and a bounded rerun. Test quantity is not evidence of path coverage.

## 7. Parallel isolation and recovery

Check both source changes and runtime resources. Separate branches or worktrees
can still share ports, databases, caches, environment files, save directories,
or account state. Inspect path resolution and configuration before launching
parallel runs. Where needed, suggest per-run namespaces, disposable state, or
serialization with explicit ownership. Check cleanup and rollback boundaries
without executing destructive recovery. Do not require parallel agents for
work that is simpler to do serially.

## 8. Maintained knowledge and machine-checked constraints

Compare the instructions an agent would follow with current scripts and code.
Identify a canonical home for volatile facts, ownership for updates, and a
cheap way to detect drift when a demonstrated problem justifies it. Assess
whether lint, schema, type, dependency, or boundary checks enforce the stated
constraint. Distinguish their guarantees from behavioral tests. Prefer an
existing check or a small rule to duplicated manuals or a custom agent system.
