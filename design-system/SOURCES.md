# Sources

Project root: the repository root, one level above `design-system/`.

| File read | Lines read | What came from it |
| --- | --- | --- |
| design-systems/profiles/lean-skill.json (outside project) | all | Project facts: no visual identity, no logo files, blog URL, surfaces |
| README.md | 1-12, 19-37 (Install), 41-48 (What is inside) | Name "lean", purpose (line 3, "Lean mode for AI coding agents.", used verbatim as the Hero sub-line), blog post label "Blog post:" and URL (line 10; the URL is not written into previews, so the Hero has no blog link), install commands (Claude Code plugin, Codex skill) |
| skills/lean/SKILL.md | 1-30 | Purpose wording and the runner ladder, used for voice and the Hero steps |
| PROMPT.md | 1-6 | Plain-text version of the four steps (check, delegate, verify, report) |

Owner brief (not a file): concept, palette, type, cover pattern, hero copy. These are new choices. No value in tokens.json comes from existing code, because the project has none (no CSS, no colour in source).

Files checked and not used: .claude-plugin/ and .agents/ hold manifests and skill links only (no visual values). LICENSE is MIT text.

Not copied: no secrets, env files, personal data or real people's names are in the system or previews. The blog URL is not written into any preview (the validator allows only Google Fonts URLs there); it lives in README.md.
