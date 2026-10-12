# Acceptance Cases

Use these synthetic cases to evaluate conversation behavior. They are not an
automated test suite or evidence that a run has passed.

For explicit trials, give a fresh agent the skill and only the request and stated
context. Deliver follow-ups as separate user turns. Keep expected observations
away from the trial agent. Allow reading the skill; keep these trials free of
file edits, external changes, or fabricated research results. Record the skill
revision or hashes, actual replies, and observations separately from expectations.

## 1. A vague creative idea

Request:

> I want a museum visit to feel a bit like a detective story, but I don't know
> what that means yet. Can we explore it together?

Follow-up:

> The idea of noticing clues sounds interesting, but I haven't chosen a
> direction. I don't want visitors to feel tested.

Observe whether the agent contributes distinct possibilities before asking a
useful framing question, accepts an evolving goal, and uses the reaction to refine
the discussion. It should preserve the user's uncertainty rather than record a
chosen direction or jump into a production plan.

## 2. An architecture trade-off

Request:

> We're designing inventory across two warehouses. Selling the same last item
> twice is unacceptable, but staff also need to keep working during an internet
> outage. Help me think through the architecture before we implement anything.

Follow-up:

> During an outage, staff can record intended sales, but a sale can stay pending
> until it is confirmed centrally. Let's use that rule. What have we settled,
> and what is still open?

Observe whether the agent makes the availability and confirmation trade-off
understandable, presents viable directions with conditions, and asks about the
business rule rather than inventing it. After the follow-up, it should preserve
the accepted rule and distinguish it from open technical choices. No code edits
or unsupported performance claims belong in this discussion.

## 3. A settled scope and a request to finish

Context and request:

> We've agreed that v1 search will use exact titles with case-insensitive
> matching. We accept that typos won't match. Let's wrap up; we can revisit fuzzy
> search if users struggle. What should I carry forward?

Observe whether the agent closes with the decision, its known limitation, and a
useful revisit condition. It should not demand another preference answer, reopen
the accepted trade-off, or begin implementation.

## 4. Evidence rather than more speculation

Request:

> We have compared a short and a detailed onboarding flow several times. The
> only unresolved issue is which one newcomers actually finish more often.
> We have no user data yet. How should we move this discussion forward?

Observe whether the agent proposes a small check that could discriminate between
the alternatives, without inventing results or prescribing a winner. It should
avoid expanding a resolved discussion into another exhaustive pros-and-cons list.

## 5. A deliberate change of focus

Context and request:

> Earlier we picked an email digest for updates. I've realized the more important
> question is whether people need updates at all. Let's step back and discuss that.

Observe whether the agent follows the user's change of focus, preserves the
previous choice as context, and examines the newly questioned premise. Earlier
decisions should not become a reason to block reconsideration.

## 6. Local acceptance within an unfinished discussion

Context and request:

> I want to design a standalone skill that sets up a curated collection of
> agent skills for a Godot project. Some skills are mine and some come from
> third parties; project conditions determine which ones apply. Every run must
> both fill missing entries and update existing ones. We are currently deciding
> which client to target. Help me work through this before we create anything.

Follow-up 1:

> Use the current client by default and allow an explicit target. Go with your
> recommendation for that choice.

Follow-up 2:

> Make it standalone, default to repository scope, and ask me when existing
> content conflicts instead of overwriting it. Go with those choices.

Follow-up 3:

> Let's stop here. Summarize the decisions; leave the remaining questions for
> another day.

Deliver each follow-up separately without adding a request to find gaps. After
the first two acceptances, observe whether the agent preserves settled choices
and advances a material unresolved issue with reasoning and a focused question,
or an authorized factual check. Relevant issues include installation scope,
ownership and local edits, or how exclusions affect previously installed skills;
this list is illustrative, not a required agenda. A recap alone or an offer to
continue only if asked does not advance the unfinished discussion. The agent
should not expand into an exhaustive checklist or create files. After the final
follow-up, it should summarize and defer without demanding another answer.

## Routing checks

Evaluate selection separately using the skill's invocation policy:

- Positive: explicitly invoke `$talk-it-through` with the initial request from
  case 1 or 2; the skill should remain available.
- Negative: submit those same requests without naming the skill; they should not
  invoke it implicitly because `policy.allow_implicit_invocation` is `false`.
- Negative: "What does HTTP 404 mean?" should receive a direct factual answer.
- Negative: "The wording is approved. Replace the heading with 'Order history'."
  should proceed as an editing task rather than reopen the wording discussion.

Policy and description review is static evidence. Explicitly loading the skill
for the conversation trials does not establish implicit selection, installed
discovery, or behavior in another client. For a before-and-after comparison,
record both revisions and use equivalent requests and environments.
