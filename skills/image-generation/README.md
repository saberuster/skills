# Image generation

Skills for developing, extracting, structuring, and reviewing GPT Image prompt
text. These skills do not generate or process images.

## Skills

Choose by the main work still needed. Honor an explicitly selected skill;
an image supplied only as context does not require the image entry.

| Main work | Skill |
| --- | --- |
| Develop an idea or resolve consequential creative choices | [Brief to Image Prompt](brief-to-image-prompt/README.md) |
| Observe an image or extract its requested visual features | [Image to Prompt](image-to-prompt/README.md) |
| Structure known requirements, edit a prompt, or review one | [GPT Image Prompting](gpt-image-prompting/README.md) |

Both entries use the core's shared output and revision rules. By default,
drafting returns one complete prompt; requested alternatives are independently
usable. Review-only requests return findings, and scoped extraction can return
only the requested reusable fragment.

## Installation

Install each skill from its own subfolder using the
[shared installation protocol](../../docs/installation.md). Both entry skills
require `gpt-image-prompting` in the host's available skills. Install packages
under their existing skill names; this collection is not an installable skill.
