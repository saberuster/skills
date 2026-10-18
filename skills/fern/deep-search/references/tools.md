# Tool selection notes

Use only the relevant section. These notes describe capabilities and connector
shapes inspected on 2026-10-18, not a portable API contract or price guarantee.
The host's actual tool definitions and access rules govern each call. Do not
copy REST API options into a connector that does not expose them.

## Built-in web search and direct readers

Use the host's search/open/find capabilities for direct reads, the specified
GitHub raw-file and X fallbacks, and permitted provider-unavailable routes.
Exa owns planned first-round general discovery. Known substantive pages outside
specialist routes prefer Exa content when their needed text is missing; status
endpoints and small factual reads can use the host reader directly. Domain and
date filters apply only if supported. Built-in retrieval is not inherently free.

## OpenAI Docs

For OpenAI product contracts, use its official documentation tool scoped to
the requested product and version. Current tools include
`search_openai_docs(query, limit?, cursor?)`,
`fetch_openai_doc(url, anchor?)`, and
`get_openapi_spec(url, languages?, codeExamplesOnly?)`. These names describe the
tool suffixes; discover the host's full callable names.

Search when the right document is unknown, then fetch its relevant page or
section before citing exact guidance. With a known document URL, fetch it
directly. Use an endpoint spec for request/response contracts when appropriate;
do not enumerate every endpoint for one known operation. Check local code,
installed versions, or configuration for questions about an actual setup.
Documentation alone does not prove local or account behavior. If the official
tool is unavailable, use allowed official-domain web search or a direct reader.
Other products' known substantive documentation follows the Exa content route
unless the user or host specifies a different specialist reader.

## GitHub

Use GitHub tools first to search or read GitHub content, including candidates
found through Exa or Parallel. Read a known file at the requested tag or commit;
retain the resolved revision when available. If the ref is unknown, do not
invent one or equate the default branch with an installed release. Native code
search may cover only the default branch. Choose the right search surface for
files, repositories, issues, or PRs; website operators may differ from connectors.

If the native file reader is unavailable or cannot serve the request, use the
host's built-in web reader on the matching raw file, preserving repository,
path, and revision. Do not send GitHub content to Exa content/fetch, including
GitHub raw hosts. Issues, PRs, discussions, and release pages have no raw-file
equivalent: use their native tools or accessible original pages. If those paths
fail, preserve the access gap rather than inventing content or a raw URL.

Current GitHub `fetch_file` supports repository, path, ref, and optional line
bounds. A PR, its merge commit, release notes, and deployed behavior answer
different questions. Research uses read operations; finding a bug or a useful
discussion does not authorize posting a comment or changing the repository.

## X

Follow this order for a request requiring X retrieval. Reuse adequate cached
material first, and respect an explicit user-selected provider.

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
3. If Grok is absent, inaccessible, unauthenticated, incompatible, or unable
   to retrieve useful source material, use the current host model's default
   search capability. Search indexed X pages and read accessible originals.
   Keep this fallback with the host model; do not start another Grok session
   or silently route it to Exa or Parallel. If the default search is also
   unavailable, return existing evidence and the access gap.

A valid empty result is not an authentication or availability failure. Assess
the query and requested coverage before spending another attempt. Preserve
successful partial results and retrieve only the missing part. Do not install,
update, authenticate, or reconfigure Grok automatically, and do not retry an
auth/quota failure in a loop.

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

For all three routes, state missing replies, inaccessible posts, historical
gaps, or limited sampling when relevant; web results do not establish complete
X coverage. In the handoff, preserve author, post URL, publication date, and
retrieval date when available; label missing dates unknown. Name the next
request's owner and carry forward the task ledger's used/remaining allowance,
or state that no hard allowance was supplied.
See the [X search documentation](https://docs.x.com/x-api/posts/search/introduction)
for the platform's recent versus archive distinction, subject to connector
access.

## Exa

Use search for the first round's distinct discovery objectives. Size result
sets for each direction's evidence requirements; neither a universal handful
nor a large quota establishes coverage. Search may already return adequate
passages, so inspect and reuse them before fetching content.

The inspected plugin exposes `web_search_exa` with required `query` and
`objective`, plus optional `numResults`. Describe the ideal source in `query`;
use `objective` for the exact missing evidence and source preferences. Its
`web_fetch_exa` accepts a `urls` array and optional `maxCharacters` per page.
Do not use a remembered singular `url` argument.

Use content/fetch directly for a known, likely substantive article, document,
paper, or technical guide outside OpenAI Docs, GitHub, and X routes. Recognize
the candidate using available title, publisher, description, URL context, or
excerpts; do not spend a discovery request merely to classify it. Select only
relevant pages with needed content absent from existing evidence. Batch related
URLs when supported and choose a content allowance that retains required
sections and qualifiers. Assess the actual extraction for completeness and
source quality; file type or publisher alone does not prove either. Preserve
successful pages and use an allowed direct reader for inaccessible or unusable
content. This preference does not establish measured extraction superiority.

The broader API has more modes and content options than this connector. Consult
the [official search guide](https://exa.ai/docs/search/quickstart) for API work
and [current pricing](https://exa.ai/pricing) only when it applies to the actual
integration. Search, additional results, content views, and summaries can have
different charges. Do not request overlapping content formats or summaries
without a task-specific need, or infer the user's bill from a response length.

## Parallel

Use search after first-round assessment for unresolved directions. Give the
request a specific missing question, known findings and source URLs, the new
evidence sought, and a stopping condition. Encode these in supported objective
and query fields; do not invent connector fields. Exclude duplicate results
locally when a provider has no exclusion filter. If the first round already
meets the plan, skip Parallel. A known missing passage needs a direct read,
not a repeated discovery search.

The inspected `web_search` accepts an atomic `objective` and a
`search_queries` array. Group useful short query variants for the same objective;
do not pad the array merely to reach a quota. Search returns relevant excerpts,
which can avoid a fetch when they contain the needed evidence and qualifiers.

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
