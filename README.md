# lean

Lean mode for AI coding agents. Type `/lean <goal>`. The agent:

1. checks the machine (disk, memory pressure, load) and moves heavy work to the cloud when the machine is tight,
2. gives each sub-task to the cheapest runner that can do it well (a script, Jev, sparecode, Gemini through Antigravity, Claude Code Sonnet, Codex Sol),
3. stays inside the subscriptions it already has,
4. verifies the result against primary evidence and continues until the goal is done.

Blog post: https://ashley.raiteri.net/blog/2026-10-12-lean-mode/

## The prompt

If you do not want a skill, paste [PROMPT.md](PROMPT.md) into any agent.

## Install

Claude Code (plugin):

```
/plugin marketplace add ashrocket/lean-skill
/plugin install lean@lean-skill
/reload-plugins
```

Claude Code (personal skill, short name `/lean`):

```bash
git clone https://github.com/ashrocket/lean-skill ~/lean-skill
ln -s ~/lean-skill/skills/lean ~/.claude/skills/lean
```

Codex (`$lean`):

```bash
ln -s ~/lean-skill/skills/lean ~/.codex/skills/lean
```

## What is inside

- `skills/lean/SKILL.md`: the procedure: check, delegate, offload, stay on plan, verify, report.
- `skills/lean/scripts/lean_check.py`: prints LOCAL-OK or TIGHT, the runners it found, and billing warnings (for example, `ANTHROPIC_API_KEY` set means `claude -p` bills the API). Stdlib only. It never prints secrets.
- `skills/lean/scripts/jev_choice.py`: asks [Jev](https://docs.typesafe.ai/llms.txt) one typed choice question and logs token use.

The runners are optional. The skill uses the ones that `lean_check.py` finds.

## Measured startup cost (2026-10-12, one-word reply)

| Runner | Model | Input tokens |
| --- | --- | --- |
| `claude -p` (default) | claude-sonnet-5-5 | 35,584 |
| `claude -p --strict-mcp-config --disable-slash-commands` | claude-sonnet-5-5 | 22,994 |
| `codex exec` | gpt-6-sol | 15,966 (total) |

Each call has a fixed cost. Put many small questions into one call. For one small judgment, use a script or Jev.

## License

MIT
