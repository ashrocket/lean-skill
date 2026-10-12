---
name: lean
description: "Lean mode: balance local compute, cloud capacity, and token cost while you pursue a goal to verified completion. Use when the user types /lean or $lean, says 'lean mode', 'work lean', 'save tokens', 'use cheaper models', 'offload this', 'push it to the cloud', or 'keep going until it is done', or when disk, memory, or CPU is low during long work. Routes each sub-task to the cheapest runner that can do it well (Python script, Jev, sparecode, Antigravity agy, Claude Code Sonnet, Codex Sol, cloud routines, Codex cloud, ChatGPT Dot, Meta Muse), prefers runs that a subscription includes, and keeps the strongest model for judgment and the final check. Do NOT use it to skip verification or to authorize deletes, posts, or spending that the user did not ask for."
---

# Lean: compute, cost, and completion in balance

The goal comes from the user's request (or the text after `/lean`). Lean mode changes HOW you do the work, not WHAT you are allowed to do.

## 1. Check the machine first

Run `python3 <this skill dir>/scripts/lean_check.py`. It prints a verdict and never prints secrets.

- **TIGHT** (low disk, memory pressure warn/critical, or load above the CPU count): send long or heavy work to a cloud runner (step 3). Do not start local builds, local models (Ollama), simulators, or wide local fan-out.
- **LOCAL-OK**: local background runners are fine. Keep the fan-out small.

Run it again before each large fan-out. Other sessions change the load.

## 2. Delegate down the ladder

Give each sub-task to the lowest rung that can do it well. Run it in the background and write the output to a file.

| Rung | Use for | Runner | Cost basis |
| --- | --- | --- | --- |
| 0 | Repeated, counted, parsed, or data-heavy work | A Python or shell script | Free |
| 1 | One narrow judgment: classify, match, rank, yes/no with a probability | Jev: `scripts/jev_choice.py`, or the `typesafe-ai` skill | Pay per token, tiny |
| 2 | One small code change as a reviewable diff | `sparecode run "TASK" --repo PATH --file F --dry-run` | OpenRouter (capped) or local Ollama |
| 3 | Read, search, summarize, mechanical edits | `agy`, `claude -p --model sonnet`, `codex exec -m gpt-6-sol` at low effort | Subscription |
| 4 | Parallel work inside this session | Agent or Workflow with `model: 'sonnet'` (or `'haiku'`) and `effort: 'low'` | Subscription |
| 5 | Hard reasoning, conflict resolution, the final check | The main session model | Subscription |

Background commands (read-only by default):

```bash
OUT=${TMPDIR:-/tmp}/lean; mkdir -p "$OUT"
# Claude Code Sonnet. Unset the API key so the run stays on the subscription.
# --strict-mcp-config and --disable-slash-commands cut startup context about 35%.
# Do not use --bare: it accepts only an API key, so it leaves the subscription.
env -u ANTHROPIC_API_KEY claude -p "$PROMPT" --model sonnet --effort low \
  --allowedTools "Read,Grep,Glob" --strict-mcp-config --disable-slash-commands \
  --output-format json > "$OUT/claude.json" 2>&1 &
# Codex Sol on the ChatGPT plan.
codex exec -m gpt-6-sol -c model_reasoning_effort=low -s read-only --ephemeral \
  --skip-git-repo-check -o "$OUT/codex.txt" "$PROMPT" > /dev/null 2>&1 &
# Gemini through Antigravity. `agy models` lists the model ids.
agy -p "$PROMPT" --model gemini-3.8-flash-low --sandbox --output-format text > "$OUT/agy.txt" 2>&1 &
```

In Claude Code, prefer the Bash tool's `run_in_background` to a bare `&`; you get a notice when the run ends. Do not poll in short loops.

Each CLI run has a fixed startup cost. Measured on 2026-10-12 for a one-word reply: `claude -p` 23k-36k input tokens, `codex exec` about 16k. Put many small questions into one call. For one tiny judgment, use a script or Jev.

## 3. Move heavy or long work to a cloud runner

Use this when the check says TIGHT, or when a job runs longer than this session should wait.

- **Claude Code routine** (Anthropic cloud, on the subscription): use the `schedule` skill. It can run once or on a cron.
- **Codex cloud** (ChatGPT plan): `codex cloud exec --env <ENV_ID> "$PROMPT"`, then `codex cloud status`, `codex cloud diff <ID>`, and `codex cloud apply <ID>`.
- **ChatGPT Dot** or **Meta Muse**: these have no headless CLI. Write a self-contained brief file and give it to the user to paste.

Cloud runners cannot see local files, local sign-ins, or the keychain. Send only content that is safe to leave the machine: no secrets, no tokens, no private data.

## 4. Stay inside the subscriptions

- `claude -p` uses the claude.ai subscription only when `ANTHROPIC_API_KEY` is unset. `lean_check.py` warns you when it is set.
- `codex exec` and `codex cloud` use the ChatGPT plan when `codex login status` says ChatGPT.
- Jev and hosted sparecode bill per token. Use them for small, capped calls (sparecode budget caps, `--max-budget-usd` for `claude -p`).
- Ask the user before you add a paid key, raise a spending cap, or start a job that a plan will not cover.

## 5. Verify, then continue until done

1. At the start, write the done condition as a check: a command and its expected result.
2. Workers produce. The main model verifies. Check each claim that you will report against primary evidence: a fresh command, the file, or the live page. A worker's summary is not evidence.
3. When a worker fails or returns weak output, move it ONE rung up. Do not jump to the top.
4. Continue until the check passes. If you are blocked, stop and report the exact blocker.

## 6. Report

- The done check and its result.
- A short ledger: which runner did which task, the model, and the tokens or cost where you know them.
- What you did not verify.

## Guardrails

- Lean mode never adds permission. Deletes, posts, pushes, payments, and secret handling still need the user's request.
- Give write tasks to a worker only in a git worktree or a sandbox. Review the diff before you merge it.
- Do not put secrets in prompts, briefs, or output files.
