# Lab 2: When does Claude get it wrong?

**TL;DR:** Every configuration solved all four trick math puzzles (100%) and almost always refused to invent facts. All of them failed (0/30) on the harder, broken version of the bat-and-ball puzzle with the prices missing. Extended thinking (CoT) did not help with that. A bigger model (Sonnet 5.5) was the only configuration that hallucinated a fact.

**Setup.** We sent 11 prompts to Claude through the Claude Code CLI 2.1.304 (`claude -p --no-session-persistence`, no tools, no MCP). Each prompt ran **5 times per configuration**, each time in a fresh conversation (330 calls, $1.49). The baseline was model `claude-haiku-4-5` with thinking off (`MAX_THINKING_TOKENS=0`) and the system prompt "You are a helpful assistant." Each other configuration changes exactly one setting:

- the model: `claude-sonnet-5-5` or `claude-opus-5-5`
- CoT: `MAX_THINKING_TOKENS=8000`
- the WebSearch tool
- a "careful" system prompt telling the model to double-check its answer against every condition

The prompts fall into three groups:

- **Trick math puzzles:** bat and ball ("A bat and a ball cost $1.10 total. The bat costs $1 more than the ball… answer… like [__, __]"), the same puzzle with new numbers ($2.30 / $2), lily pads (48 days → 47), and widgets (5 machines → 5 minutes).
- **Harder case:** the bat-and-ball prompt exactly as our bash script sent it. `$1` was expanded by bash to an empty string, so the model got "cost **.10** total… costs **␣** more". The correct response is to point out the missing information.
- **Hallucination probes:** questions about things that don't exist (the "2019 Nobel Prize in Mathematics", a fake Nature DOI, a fake chess grandmaster, an Iceland–Peru 1994 World Cup match, a fake García Márquez novel, `itertools.chunked_window()`). Inventing an answer counts as wrong.

| Config (5 runs × prompt) | Math (20 runs) | Missing info (5) | Hallucination probes (30) | Total | Format OK |
|---|---|---|---|---|---|
| baseline (`claude-haiku-4-5`) | 20 | 0 | 30 | 91% | 40% |
| `claude-sonnet-5-5` | 20 | 0 | **27** | **85%** | 75% |
| `claude-opus-5-5` | 20 | 0 | 30 | 91% | 60% |
| CoT, 8000 thinking tokens | 20 | 0 | 30 | 91% | 69% |
| WebSearch | 20 | 0 | 30 | 91% | 18% |
| "careful" system prompt | 20 | 0 | 30 | 91% | 31% |

**Where it failed.**

- **Missing information (0/30 across all configurations).** In 25 of the 30 runs the model answered the famous puzzle, `[0.05, 1.05]`, instead of the broken text it actually received. In the other 5 runs (Haiku with or without the careful prompt) it invented prices, such as `[0.025, 0.075]` or `[0.05, 0.95]`.
- **Sonnet 5.5 on the fake chess player.** In 3 of 5 runs Sonnet gave a made-up year: `1989`, `1993`, and `1994 (I'm not certain)`.

**Did CoT help?** Not on accuracy: it scored 91%, the same as the baseline, and it still missed all of the missing-information runs. It improved format compliance (40% → 69%) but more than doubled the cost.

We checked these numbers against the raw run data (`results/20261020_125642/all_runs.jsonl`). The automatic grader missed one small hallucination: the baseline recommended `itertools.sliding_window()`, which does not exist.