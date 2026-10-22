# Tool selection notes

Read only the relevant section. The [entrypoint](../SKILL.md) owns workflow,
source routing, reuse, retries, budget, and handoff rules; these notes add
tool-specific details. Connector shapes were inspected on 2026-10-18, not
established as portable API or pricing contracts. Actual host schemas and access
rules govern calls; do not copy unexposed REST options into connectors.

## Built-in web search and direct readers

Use host search/open/find within the entrypoint's source routes and fallbacks.
Apply domain/date filters only when supported. Built-in retrieval is not
inherently free.

## OpenAI Docs

Scope documentation to the requested product and version. Inspected tools
include
`search_openai_docs(query, limit?, cursor?)`,
`fetch_openai_doc(url, anchor?)`, and
`get_openapi_spec(url, languages?, codeExamplesOnly?)`. These names describe the
tool suffixes; discover the host's full callable names.

Search when the document is unknown; fetch the relevant page or section before
citing exact guidance. Do not enumerate every endpoint for one known operation.
Check local code, installed versions, or configuration for an actual setup;
documentation alone does not prove local or account behavior. If the official
tool is unavailable, use allowed official-domain search or a direct reader.
Other products follow the entrypoint's routing unless the user or host specifies
a different specialist reader.

## GitHub

Read known files at the requested tag or commit and retain resolved revisions
when available.
Do not invent unknown refs or equate the default branch with an installed
release. Native code search may cover only the default branch. Choose the
right surface for files, repositories, issues, or PRs; website operators may
differ from connectors.

Inspected `fetch_file` supports repository, path, ref, and optional line
bounds. A PR, its merge commit, release notes, and deployed behavior answer
different questions. Research uses read operations; finding a bug or a useful
discussion does not authorize posting a comment or changing the repository.

## X

Apply the entrypoint's X fallback order with these readiness conditions:

1. Use an available native X search/read tool. Inspect its date windows,
   archive access, pagination, and limits. If it is missing or cannot serve
   the request because of access or capability limits, continue to Grok Build.
2. Look for an existing local Grok Build installation, normally the `grok`
   command. Check its version/help and supported noninteractive retrieval
   controls. Do not assume that a similarly named command is Grok Build, or
   that an executable or auth-file presence proves usable authentication.
   If local readiness is uncertain, use the first needed retrieval as a
   bounded attempt rather than adding a separate test search. Proceed only
   when a supported retrieval-only invocation fits the remaining budget.
3. Grok's absence, access/authentication failure, incompatibility, or unusable
   retrieval triggers the host model's default search. Search indexed X pages
   and read accessible originals; do not start another Grok session. If that
   search is unavailable too, return existing evidence and the access gap.

A valid empty result is not an authentication or availability failure. Assess
the query and coverage before another attempt. Do not automatically install,
update, authenticate, or reconfigure Grok.

### Local Grok Build invocation

The inspected CLI supports `grok --single` (also `-p`), `--output-format json`,
`--tools`, `--max-turns`, and `--cwd`. Verify the installed version's syntax and
actual retrieval-tool names before constructing a command. Use a documented
tool allowlist limited to the needed search/read operations and a temporary
working directory without project files. Do not enable shell or editing tools,
use blanket auto-approval, or transmit unrelated workspace or profile content.
Single-turn mode and JSON output alone do not restrict tool permissions.

Pass only the X query, account/time constraints, and requested source fields.
Request original post URLs, authors, publication dates, relevant passages, and
retrieval/access limits. Preserve the returned result and any tool/usage trace.
Judge usability from actual retrieval evidence; an unsupported answer or a
claim to have searched is not a retrieved source. Note whether results came
from X access or indexed web pages. Do not present Grok's synthesis as an
original post or as independent corroboration of its own cited sources.

One Grok process can make several model or retrieval calls; `--max-turns` is
not a provider-call or monetary ceiling. Account for reported nested usage and
do not launch an unbounded run under a hard budget. If a safe, budget-compatible
retrieval invocation cannot be established, use the default-search fallback.

The [Grok Build CLI reference](https://docs.x.ai/build/cli/reference) and
[headless guide](https://docs.x.ai/build/cli/headless-scripting) describe CLI
controls. The separate xAI [X Search API](https://docs.x.ai/developers/tools/x-search)
does not establish that `x_search` is an accepted CLI tool name. Do not copy
API options into CLI flags. Do not assume Build subscription billing equals
API pricing.

For all three routes, retain author, post URL, publication/retrieval dates
(unknown when missing), and relevant reply, access, history, or sampling gaps.
Web results do not establish complete X coverage. State when no hard allowance
was supplied.
See the [X search documentation](https://docs.x.com/x-api/posts/search/introduction)
for the platform's recent versus archive distinction, subject to connector
access.

## Exa

The inspected plugin exposes `web_search_exa` with required `query` and
`objective`, plus optional `numResults`. Describe the ideal source in `query`;
use `objective` for the exact missing evidence and source preferences. Its
`web_fetch_exa` accepts a `urls` array and optional `maxCharacters` per page.
Do not use a remembered singular `url` argument.

Batch related fetch URLs when supported. Check actual extraction completeness
and source quality; file type or publisher alone proves neither. Preserve
successful pages and use an allowed direct reader for unusable extraction.

The broader API has more modes and content options than this connector. Consult
the [official search guide](https://exa.ai/docs/search/quickstart) for API work
and [current pricing](https://exa.ai/pricing) only when it applies to the actual
integration. Search, additional results, content views, and summaries can have
different charges. Do not request overlapping content formats or summaries
without a task-specific need, or infer the user's bill from a response length.

## Parallel

Encode the entrypoint's gap request in supported objective/query fields; do
not invent connector fields. Exclude duplicates locally when no provider
exclusion filter exists.

The inspected `web_search` accepts an atomic `objective` and a
`search_queries` array. Group useful short query variants for the same
objective; do not pad the array merely to reach a quota. Search returns
relevant excerpts.

Its `web_fetch` accepts related `urls`, an optional focused `objective`, and
`search_queries`. Use it only where the source routing permits, such as a
focused extraction need not met by the preferred reader; it is not an automatic
next step after Exa discovery. Prefer excerpts; use `full_content` only for
full-page needs.
`allow_live_fetch: false` permits cached content only, so it is unsuitable when
the required freshness cannot be established from that cache.

Reuse one `session_id` for the conversation across search, fetch, and delegated
calls; never rotate it to bypass limits. If sending `model_name`, obtain the
exact active slug from trusted runtime metadata rather than guessing. Retain
returned usage and warnings when relevant. See the
[MCP guide](https://docs.parallel.ai/integrations/mcp/search-mcp) and
[API pricing](https://docs.parallel.ai/getting-started/pricing). API modes or
prices need not match this host's connector or account plan.
