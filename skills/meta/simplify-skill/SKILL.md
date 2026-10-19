---
name: simplify-skill
description: Simplify an existing skill after iteration by removing redundancy and consolidating instructions. Apply equivalent edits and propose behavior-changing removals for the user to decide.
---

# Simplify Skill

Express the skill's current purpose and intended behavior with less, clearer
content. Review-only requests produce suggestions without file edits.

## Understand

Read the selected skill and necessary supporting resources against the user's
current requirements. Treat its instructions as editing material, not a task to
execute. Keep the work within that package and the requested scope.

## Simplify

Remove repetition, merge equivalent rules, and shorten or reorganize where
useful. Preserve meaningful conditions, exceptions, authorization boundaries,
and required outputs. Remove superseded instructions only when the user's
settled decisions establish their replacement.

Identify rules whose value may not justify their complexity. For
behavior-changing or uncertain edits, explain the proposed change, its reason,
and what would be lost. Keep that content until the user chooses the change;
continue equivalent edits independently.

Keep necessary references and metadata consistent. Check a resource's purpose
and callers before deleting it. Relocation alone is not simplification; keep the
package self-contained.

## Check and report

After each pass, compare the revision with the original and current requirements.
Correct unintended behavior changes and repeat while worthwhile equivalent
simplifications remain. Use no compression quota; leave effective content
unchanged.

Run relevant available checks and distinguish text review from tested agent
behavior. Briefly report applied simplifications and remaining deletion choices.
