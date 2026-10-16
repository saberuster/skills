# Sources and design choices

These links support maintenance of the skill. They are not runtime dependencies
or a requirement to browse during editing. The instructions and synthetic
examples here are independently written; external material is not reproduced
or included in this repository's license grant.

The source review on 2026-10-17 informed the choices below. A source's published
instructions describe its design, not demonstrated editing quality. Dynamic
branch links can change; recheck originals before importing further guidance.

| Source | Adopted principle | Boundary |
| --- | --- | --- |
| [Cursor pstack unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) | A direct editing workflow, plain words, concrete actions, and protection against over-compression. | Treat patterns as contextual signals; do not inherit blanket punctuation bans or explicit-only invocation. |
| [blader/humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md) | Check formulaic structures and protect non-prose content. | Preserving voice does not authorize adding opinions or experiences. |
| [ctx-humanize](https://github.com/activememory/ctx/blob/main/internal/assets/claude/skills/ctx-humanize/SKILL.md) | Preserve certainty, coverage, exact content, and requirement keywords. | Review examples against the preservation contract too; an instruction to preserve facts is not proof that every example does. |
| [hannsxpeter/humanizer](https://github.com/hannsxpeter/humanizer/blob/main/SKILL.md) | Light or no edits for good text; inspect implied causes, timing, and newly added stance. | Do not adopt unvalidated frequency thresholds or automatic author research. |
| [Waza write](https://github.com/tw93/Waza/blob/3f135d26dab706d889b93b7ca0f4ab37f6b07579/plugins/waza/skills/write/SKILL.md) | Treat over-editing as failure; prefer fewer useful changes and evidence-backed voice. | Its house style, punctuation tooling, and additional writing modes are not general requirements. |
| [humanizer-zh](https://github.com/ai-zixun/humanizer-zh/blob/main/SKILL.md) | Consider Chinese syntax, empty slogans, paragraph continuity, and claim strength. | Do not adopt author imitation, universal punctuation preferences, or fixed translations of project terms. |
| [BMAD prose review](https://github.com/bmad-code-org/BMAD-METHOD/blob/819d373e/src/core-skills/bmad-editorial-review-prose/SKILL.md) | Minimal useful fixes, deliberate style preservation, and no findings as a valid outcome. | Do not inherit word-count gates or removal of meaningful uncertainty. |
| [Slopbeth preservation](https://github.com/ehmo/slopkit/blob/main/skills/slopbeth/references/voice-and-preservation.md), [benchmark limits](https://github.com/ehmo/slopkit/blob/main/skills/slopbeth/BENCHMARKS.md) | Check facts and voice separately; include good-text controls and adversarial cases. | Self-defined lint scores and change ratios do not establish overall quality or competitor superiority. |
| [unslop adversarial evaluation PR](https://github.com/theclaymethod/unslop/pull/1) | Test units, contextual false positives, loss of qualifiers, and scoring shortcuts. | Historical reported failures are test ideas, not independently reproduced claims about a current release. |
| [CAN-ASC-3.1:2025 wording and expression](https://accessible.canada.ca/standards-and-technical-guides/standards-and-technical-guides-database/can-asc-312025-plain-language/13-wording-and-expression) | Choose wording for the reader; terminology, passive voice, and punctuation need contextual exceptions. | Accessibility guidance is not a universal literary style; never simplify away numerical precision. |
| [Microsoft style guide directory](https://learn.microsoft.com/en-us/globalization/reference/microsoft-style-guides), [Gengo Chinese guide](https://gengo.com/zh/translators/resources/style-guide/) | Language and locale matter to wording and typography. | The Microsoft directory alone does not establish a specific Chinese rule; platform-specific translation requirements remain outside this skill. |

Prefer meaningful before-and-after checks to banned-word counts or AI-origin
claims. Assess improvement, factual preservation, voice, exact content, and
edit scope separately. A serious loss in one dimension cannot be canceled by
a higher style score in another.
