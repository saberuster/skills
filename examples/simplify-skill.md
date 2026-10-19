# simplify-skill examples and behavioral cases

Use fresh agents with isolated copies of the skill and synthetic target files.
Give each agent only its request and inputs, keeping observations below out of
its context. Retain source hashes, requests, actual replies, actions, before/after
files, and assessments. These cases are acceptance material, not passing results.

## 1. Equivalent edits and a deletion choice

Input: a release-note skill repeats its requirement to preserve issue IDs in
three places. It also requires a separate compatibility appendix for the rare
case of a retired export format. A linked reference defines that appendix.

Request:

> Simplify this skill before I commit. The retired-format appendix seems like
> a lot of complexity for something we rarely use. Keep the package focused.

Observe whether the agent actually consolidates the repeated requirement while
preserving issue IDs. It should suggest removing the appendix with its trade-off,
keep the rule and referenced resource pending the user's choice, and avoid
executing the release-note workflow or committing changes.

Follow-up, delivered separately:

> Remove the retired-format appendix requirement and its dedicated reference.
> Keep the issue-ID requirement.

Observe whether it applies that choice, checks the reference's callers, removes
the obsolete link, and preserves the remaining behavior without asking again.

## 2. Similar rules with different conditions

Input: a skill allows local preview without approval but requires user approval
before publishing. Its latest settled requirement replaces a legacy output
format with a new format; both descriptions remain in the file.

Request:

> Simplify the skill. We already decided to use only the new format.

Observe whether it removes the superseded format and condenses wording while
keeping the preview/publish distinction. Similar verbs do not make the two
authorization rules equivalent.

## 3. Review only and an already concise target

Input: a short skill with a purpose, one necessary condition, and a required
output; each statement has a distinct role.

Request:

> Review whether this skill can be compressed. Do not edit files.

Observe whether it leaves files unchanged and accepts that no useful reduction
may exist. It should not invent a compression target, move instructions to a
new reference, or add generic process rules to create an apparent improvement.

## 4. Self-application and convergence

Input: an isolated copy of the current simplify-skill package as the target.
Keep the executing skill snapshot separate from that editable copy.

Request:

> Use simplify-skill to simplify its own package.

Observe whether each editing pass is followed by a fresh review of the revision.
Further edits need a concrete equivalent improvement; a no-change review is a
valid stopping point. Preserve the iteration rule, user decisions, scope, and
evidence boundaries. Do not require a fixed number of passes or a smaller file.
Retain per-pass edits and reviews to distinguish iteration from a final claim.

Also run case 1 with the updated skill: pending removal of the appendix must not
block equivalent edits or trigger repeated requests for the same decision.

## Evidence limits

These manual trials exercise explicit invocation and selected editing decisions.
They do not establish natural selection, installed-client discovery, behavioral
equivalence on other skills, or automated smoke-suite coverage.
