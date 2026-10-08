---
name: learn-from-session
description: Learn reusable lessons from the current conversation and use skill-creator to update or create user-maintained skills. Use when asked to learn from this session, not for historical-session or project-wide analysis.
---

# Learn from Session

## Extract and select

- Look for user corrections, verified methods, and useful lessons from failed
  attempts. Keep the conditions and outcome that support each lesson; a
  proposed fix or an assistant's success claim alone is not verification.
- Also look for repeated code, fixed command sequences, and stable processing
  steps, even when they succeeded without corrections. Use recurrence in this
  conversation or user-provided reuse evidence; do not infer unseen history.
- Skip generic advice, temporary task state, unverified guesses, and one-off
  details. Keep project-specific procedures in project skills; do not turn
  local paths, business rules, or a one-time permission into general
  requirements.
- Read relevant existing skills and affected supporting files. Prefer a focused
  update; create a skill only for a distinct reusable task. Already-covered
  lessons need no change, and zero useful lessons is a valid result. Use
  synthetic examples when generalizing private conversation details for shared
  skills.
- Reuse existing tools and helpers first. Use instructions for judgment,
  templates for fixed structures, and consider scripts for deterministic steps.
  Weigh complexity, error risk, and reuse against invocation and maintenance
  cost. Keep simple commands, even with parameters, as examples unless a script
  reduces repeated implementation, fragile handling, or steps; repetition or
  line count alone is insufficient. Keep judgment separate from executable steps.

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

For selected scripts, pass inputs, outputs, prerequisites, failure behavior,
and representative verification cases to `skill-creator`. Keep each script in
the source skill that owns the task, and document when and how to call it.

Briefly report what was learned, which files changed, and what was checked or
remains unverified. For analysis-only requests, report proposals without
editing. No separate report file is needed unless requested.
