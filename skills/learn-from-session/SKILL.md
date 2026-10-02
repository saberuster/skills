---
name: learn-from-session
description: Learn reusable lessons from the current conversation and use skill-creator to update or create user-maintained skills. Use when asked to learn from this session, not for historical-session or project-wide analysis.
---

# Learn from Session

Turn the current conversation into small, useful skill improvements. Use the
available conversation, including relevant earlier work; do not scan other
sessions.

## Extract and select

- Look for user corrections, verified methods, and useful lessons from failed
  attempts. Keep the conditions and outcome that support each lesson; a
  proposed fix or an assistant's success claim alone is not verification.
- Skip generic advice, temporary task state, unverified guesses, and one-off
  details. Keep project-specific procedures in project skills; do not turn
  local paths, business rules, or a one-time permission into general
  requirements.
- Read relevant existing skills and affected supporting files. Prefer a focused
  update; create a skill only for a distinct reusable task. Already-covered
  lessons need no change, and zero useful lessons is a valid result. Use
  synthetic examples when generalizing private conversation details for shared
  skills.

## Apply

An explicit request to run this skill authorizes the scoped skill edits unless
the user asks only for analysis or suggestions. Automatic selection alone does
not authorize writes.

Only write to skill source directories established by the user or project
instructions as user-maintained. Resolve links and junctions and check that the
actual target stays within that scope. Treat system skills, third-party skills,
plugin caches, and installed copies as read-only. If the source directory is
unclear, finish the analysis and ask for it before writing.

Read and use the available `skill-creator` to make the selected changes and
perform applicable validation. Pass along the lesson, evidence limits, intended
behavior, and allowed source scope; avoid duplicating its authoring
instructions. If it is unavailable, provide the proposed changes and state that
implementation remains incomplete.

Briefly report what was learned, which files changed, and what was checked or
remains unverified. For analysis-only requests, report proposals without
editing. No separate report file is needed unless requested.
