# Acceptance Cases

These are evaluation inputs and expected observations, not executed results.
Use disposable repositories and an isolated installer environment. Provide an
executing agent the skill, request, fixture, and allowed tools; keep expected
observations with the evaluator. Record file hashes, source refs, tool versions,
actual operations, and unchanged destinations. Distinguish static walkthroughs,
CLI smoke checks, and actual agent execution. Explicit invocation does not test
implicit discovery.

| Case | Request and fixture | Expected observations |
| --- | --- | --- |
| Initial setup | "Set up skills for this new Godot C# repo." No generated project files; user intends unit tests. | User intent selects base and C# entries; report test entries as not yet applicable because their required test setup is absent. Install complete selected folders at repo scope for the current client. No plugin/runtime installation. |
| Mixed repeat run | Base copy is unchanged but older than upstream; one selected skill directory is absent despite a lock entry; another is current. | In one run, update the old copy, install the missing one, and skip the current one. Verify physical files and source records. |
| Conflict isolation | A selected package has a local edit or missing reference; a second uses another source; a third is absent. | Preserve the first two, explain concrete options, and request decisions. Install the independent missing package. Do not run a broad update. |
| Exclusions and conditions | A lasting exclusion exists; a separate this-run skip was used previously; user adds C# to the project. Later the project stops using C#. | Respect the lasting exclusion, reconsider the expired skip, and fill newly applicable C# entries. Later retain but do not update entries no longer selected. Manual deletion alone is not exclusion. |
| Location and client | Current directory is a nested Godot folder; repo has multiple Godot projects and two client destinations, one shared. | Resolve repo root and project selection separately. Honor the selected client and expose any unavoidable shared effect before writing. No user-wide fallback. |
| Upstream failure | One source is unavailable, another removed its skill, and an independent selected item is installable. | Keep existing copies, report unresolved items accurately, and complete the independent item. No deletion, automatic source substitution, or false "current" result. |
| Inspection boundary | "Inspect the setup and recommend changes; do not install." | Read-only selection and differences. No installer mutation or preference-file writes. |
| Fixed choices | User pins one source revision and asks to keep a conflict for this run. An upstream catalog has new entries, but the loaded setup catalog is unchanged. | Honor the pin, keep this run's conflict, and do not silently persist an exclusion or self-update the setup catalog. |
