# lean design system

lean is a lean-mode skill for AI coding agents. It checks the machine, sends each sub-task to the cheapest runner that can do it well, and verifies the result. The identity borrows from lean manufacturing: an andon light stack shows the machine state, and kanban cards route work to the cheapest runner. The product ships as a Claude Code plugin and a Codex skill, and its audience is developers who run agents and want lower token cost.

## Voice

1. Write short, active sentences. Example: "Lean mode for AI coding agents."
2. Name the action first. Example: "Type `/lean <goal>`."
3. State the check, then the result. Example: "Checks the machine, then sends work to the cheapest runner."
4. Give real numbers. Example: "Startup cost: 15,966 input tokens (one-word reply)."
5. No hype. Do not promise savings that the repo does not measure. Example: "Each call has a fixed cost." (README.md:55)

## Colour

| Token | Value | Role | Contrast |
| --- | --- | --- | --- |
| `floor` | #f1f3f4 | Page ground | Ground for all text pairs |
| `ink` | #1b1f22 | Headings and body text | 14.91 to 1 on floor |
| `steel` | #5c6670 | Muted text, tagline | 5.26 to 1 on floor; 5.85 to 1 on kanban |
| `kanban` | #ffffff | Cards | Ground for card text |
| `andon-green` | #1e7f4f | Primary action fill, go state | White text 5.00 to 1 |
| `andon-amber` | #c98a00 | Andon disc, caution state | Non-text only |
| `amber-ink` | #8a5a00 | Amber text | 5.32 to 1 on floor |
| `andon-red` | #c62828 | Stop state | 5.62 to 1 on kanban |

Text pairs pass 4.5 to 1. `andon-amber` is not a text colour.

## Type

| Family | Source | Used for |
| --- | --- | --- |
| Barlow Semi Condensed | Google Fonts (hosted; no file) | Headings, wordmark, cover name |
| Barlow | Google Fonts (hosted; no file) | Body text, captions |
| IBM Plex Mono | Google Fonts (hosted; no file) | Commands |

Each preview loads its own Google Fonts link:
- Cover: `https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600&family=Barlow:wght@400&display=swap`
- Hero: `https://fonts.googleapis.com/css2?family=Barlow+Semi+Condensed:wght@600&family=Barlow:wght@400&family=IBM+Plex+Mono:wght@400&display=swap`

Scale (see `tokens.json`):

| Style | Family | Size / line | Weight | Used for |
| --- | --- | --- | --- | --- |
| cover-name | display | 96px / 96px | 600 | Cover name only |
| display | display | 56px / 60px | 600 | Hero headline |
| heading | display | 28px / 34px | 600 | Section heads, wordmark |
| body | body | 18px / 28px | 400 | Running text, hero sub-line |
| small | body | 15px / 22px | 400 | Captions, button labels |
| command | mono | 16px / 24px | 400 | Commands |

## Layout and spacing

- Content maximum width: 1080px. Pages are width-fluid below that. (Not in the brief; chosen here.)
- Spacing steps: `space-1` 8px, `space-2` 16px, `space-3` 24px, `space-4` 40px.
- Radius, three steps (the brief names the cover pattern built from radii; the values are chosen here): `radius-sm` 4px (buttons), `radius-md` 12px (kanban cards), `radius-disc` 32px (andon discs).
- No shadows. Cards separate from the floor by the white `kanban` fill.

## Logo and wordmark

No logo file exists in the repo. Nothing was copied to `assets/Logos/`, and no logo was drawn.

The wordmark is plain type: the word "lean", lowercase, Barlow Semi Condensed 600, at the `heading` size (28px). Tracking is the default. Clear space and minimum size are not set: the brief names no logo file, so they are an owner decision.

Do not:
- set the wordmark in capitals ("LEAN");
- change the weight to 400 or 700;
- set it in a font other than Barlow Semi Condensed;
- add an icon before it.

## Landing page anatomy

The landing page is the README front page. There is no landing page in the repo yet. The Hero preview shows the page this system implies.

1. Top bar: wordmark "lean" on the left.
2. Hero: the headline `/lean <goal>`, the one-sentence purpose, the action "Install lean", and the blog post link text ("Read the blog post"). The Hero preview shows the text without a URL: the validator allows only Google Fonts URLs in previews, so the URL stays in the repo README. Component: `components/Hero/`.
3. Kanban card: three steps (check the machine, route each sub-task, verify the result). Plain text on `kanban`.
4. Install block: commands in `command` style, on `floor`, inside the `kanban` card.

## Status

new
