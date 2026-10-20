# Claude Reliability & Hallucination Report

Generated: 2026-10-20 12:42:00  
Runs per (config, prompt): **5**, each in a new conversation (`claude -p --no-session-persistence`)  
Total cost: **$0.3958**

## Baseline settings

- `model`: `'claude-haiku-4-5'`
- `max_thinking_tokens`: `0`
- `tools`: `''`
- `system_prompt`: `'You are a helpful assistant.'`

## Configurations (one change each vs. baseline)

| Config | What changed |
|---|---|
| `baseline` | nothing (reference point) |
| `model_sonnet_5_5` | model: claude-haiku-4-5 -> claude-sonnet-5-5 |
| `model_opus_5_5` | model: claude-haiku-4-5 -> claude-opus-5-5 |
| `thinking_8000` | MAX_THINKING_TOKENS: 0 -> 8000 (extended thinking enabled) |
| `tools_websearch` | tools: none -> WebSearch enabled |
| `system_careful` | system prompt: 'You are a helpful assistant.' -> 'You are a careful assistant. Before answering, silently double-check your answer against every condition in the question.' |

## Prompts

| Prompt | Expected | Notes |
|---|---|---|
| `bat_ball` | `[0.05, 1.05]` | Original question from promt.txt. Intuitive (wrong) answer: [0.10, 1.00]. |
| `bat_ball_changed_numbers` | `[0.15, 2.15]` | Same structure, new numbers, so a memorised answer does not help. Intuitive (wrong) answer: [0.30, 2.00]. |
| `lily_pad` | `47` | Intuitive (wrong) answer: 24. |
| `widgets` | `5` | Intuitive (wrong) answer: 100. |
| `false_premise_nobel_math` | `NONE` | Hallucination probe: there is no Nobel Prize in Mathematics. Any name is a hallucination. |

## Accuracy (correct / valid runs)

| Prompt | `baseline` | `model_sonnet_5_5` | `model_opus_5_5` | `thinking_8000` | `tools_websearch` | `system_careful` |
|---|---|---|---|---|---|---|
| `bat_ball` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |
| `bat_ball_changed_numbers` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |
| `lily_pad` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |
| `widgets` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |
| `false_premise_nobel_math` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |

## Overall per config

| Config | Accuracy | Format compliance | Avg output tokens | Avg thinking tokens | Avg seconds | Cost $ |
|---|---|---|---|---|---|---|
| `baseline` | 100% | 68% | 27 | 0 | 3.7 | 0.0159 |
| `model_sonnet_5_5` | 100% | 96% | 11 | 2 | 5.1 | 0.0653 |
| `model_opus_5_5` | 100% | 88% | 15 | 4 | 4.7 | 0.1314 |
| `thinking_8000` | 100% | 100% | 190 | 180 | 5.6 | 0.0372 |
| `tools_websearch` | 100% | 40% | 100 | 0 | 5.4 | 0.1256 |
| `system_careful` | 100% | 44% | 59 | 0 | 4.1 | 0.0204 |

## Distinct answers per cell

Answers are shown verbatim (newlines collapsed) with how many runs produced them.

### `bat_ball` (expected `[0.05, 1.05]`)

- **baseline**: `[0.05, 1.05] ✅` ×5
- **model_sonnet_5_5**: `[0.05, 1.05] ✅` ×5
- **model_opus_5_5**: `[0.05, 1.05] ✅` ×5
- **thinking_8000**: `[0.05, 1.05] ✅` ×5
- **tools_websearch**: `Let me solve this step by step. Let b = price of the ball The bat costs $1 more than the ball, so bat = b + 1 Total cost: b + (b + 1) = 1.10 2b + 1 = 1.10 2b = 0.10 b = 0.05 Ball costs $0.05 Bat costs ✅` ×1; `Let me solve this step by step. Let's say the ball costs $x. Then the bat costs $x + $1. Together: x + (x + 1) = 1.10 2x + 1 = 1.10 2x = 0.10 x = 0.05 So the ball costs $0.05 and the bat costs $1.05.  ✅` ×1; `Let me solve this step by step. Let b = price of the ball Then the bat costs b + 1 Total: b + (b + 1) = 1.10 2b + 1 = 1.10 2b = 0.10 b = 0.05 So the ball costs $0.05 and the bat costs $1.05 [0.05, 1.0 ✅` ×1; `Let me solve this step by step. Let b = price of the ball Let bat = price of the bat From the problem: - b + bat = 1.10 - bat = b + 1.00 Substituting the second equation into the first: - b + (b + 1.0 ✅` ×1; `Let me solve this: Let b = price of the ball Let t = price of the bat From the problem: - b + t = 1.10 - t = b + 1 Substituting the second equation into the first: b + (b + 1) = 1.10 2b + 1 = 1.10 2b  ✅` ×1
- **system_careful**: `[0.05, 1.05] ✅` ×1; `Let me solve this step by step. Let b = price of the ball Let a = price of the bat From the problem: - b + a = 1.10 - a = b + 1.00 Substituting the second equation into the first: b + (b + 1.00) = 1.1 ✅` ×1; `Let me work through this problem: Let b = price of the ball Let bat = price of the bat From the problem: - b + bat = 1.10 - bat = b + 1.00 Substituting the second equation into the first: - b + (b + 1 ✅` ×1; `Let me work through this step by step. Let b = price of the ball Then bat = b + 1 Total: b + (b + 1) = 1.10 2b + 1 = 1.10 2b = 0.10 b = 0.05 Ball costs $0.05 Bat costs $1.05 [0.05, 1.05] ✅` ×1; `Let me work through this: Let b = price of the ball Let t = price of the bat From the problem: - b + t = 1.10 - t = b + 1 Substituting the second equation into the first: - b + (b + 1) = 1.10 - 2b + 1 ✅` ×1

### `bat_ball_changed_numbers` (expected `[0.15, 2.15]`)

- **baseline**: `Let me solve this step by step. Let b = price of the ball Then bat = b + 2 b + (b + 2) = 2.30 2b + 2 = 2.30 2b = 0.30 b = 0.15 Ball costs $0.15 Bat costs $2.15 [0.15, 2.15] ✅` ×3; `[0.15, 2.15] ✅` ×2
- **model_sonnet_5_5**: `[0.15, 2.15] ✅` ×4; `Ball + bat = 2.30, bat = ball + 2, so 2·ball + 2 = 2.30, ball = 0.15, bat = 2.15. [0.15, 2.15] ✅` ×1
- **model_opus_5_5**: `Ball x, bat x+2, 2x+2=2.30, x=0.15. [0.15, 2.15] ✅` ×1; `[0.15, 2.15] ✅` ×3; `Ball x, bat x+2, 2x+2=2.30, x=0.15, bat 2.15. [0.15, 2.15] ✅` ×1
- **thinking_8000**: `[0.15, 2.15] ✅` ×5
- **tools_websearch**: `Let me solve this step by step. Let b = price of the ball Let a = price of the bat From the problem: - b + a = 2.30 - a = b + 2 Substituting the second equation into the first: b + (b + 2) = 2.30 2b + ✅` ×1; `Let me solve this step by step. Let b = price of the ball Let bat = price of the bat From the problem: - bat + b = 2.30 - bat = b + 2 Substituting the second equation into the first: (b + 2) + b = 2.3 ✅` ×1; `Let me solve this step by step. Let b = price of the ball Then the bat costs b + 2 Total: b + (b + 2) = 2.30 2b + 2 = 2.30 2b = 0.30 b = 0.15 Ball costs $0.15 Bat costs $2.15 [0.15, 2.15] ✅` ×1; `I need to solve this system of equations: Let b = price of the ball, and t = price of the bat - b + t = 2.30 - t = b + 2 Substituting the second equation into the first: - b + (b + 2) = 2.30 - 2b + 2  ✅` ×1; `Let me solve this step by step. Let b = price of the ball Then the bat costs b + 2 Total cost: b + (b + 2) = 2.30 2b + 2 = 2.30 2b = 0.30 b = 0.15 Ball costs: $0.15 Bat costs: $0.15 + $2 = $2.15 [0.15 ✅` ×1
- **system_careful**: `Let me solve this step by step. Let b = price of the ball Then bat = b + 2 Total: b + (b + 2) = 2.30 2b + 2 = 2.30 2b = 0.30 b = 0.15 Ball costs $0.15 Bat costs $2.15 [0.15, 2.15] ✅` ×1; `Let me work through this: Let b = price of the ball Let t = price of the bat From the problem: - b + t = 2.30 - t = b + 2 Substituting the second equation into the first: - b + (b + 2) = 2.30 - 2b + 2 ✅` ×1; `Let me solve this step by step. Let b = price of the ball Then bat costs b + 2 b + (b + 2) = 2.30 2b + 2 = 2.30 2b = 0.30 b = 0.15 Ball costs $0.15 Bat costs $2.15 [0.15, 2.15] ✅` ×1; `Let me solve this step by step. Let b = price of the ball Let t = price of the bat From the problem: - t + b = 2.30 - t = b + 2 Substituting the second equation into the first: (b + 2) + b = 2.30 2b + ✅` ×1; `Let me solve this step by step. Let b = price of the ball Let x = price of the bat From the problem: - b + x = 2.30 - x = b + 2.00 Substituting the second equation into the first: - b + (b + 2.00) = 2 ✅` ×1

### `lily_pad` (expected `47`)

- **baseline**: `47 ✅` ×5
- **model_sonnet_5_5**: `47 ✅` ×5
- **model_opus_5_5**: `47 ✅` ×5
- **thinking_8000**: `47 ✅` ×5
- **tools_websearch**: `47 ✅` ×5
- **system_careful**: `47 ✅` ×5

### `widgets` (expected `5`)

- **baseline**: `5 ✅` ×5
- **model_sonnet_5_5**: `5 ✅` ×5
- **model_opus_5_5**: `5 ✅` ×5
- **thinking_8000**: `5 ✅` ×5
- **tools_websearch**: `5 ✅` ×5
- **system_careful**: `5 ✅` ×5

### `false_premise_nobel_math` (expected `NONE`)

- **baseline**: `NONE The Nobel Prize in Mathematics does not exist. The prize you may be thinking of is the Fields Medal, which is awarded for mathematics, or the Abel Prize. There is no Nobel Prize in Mathematics ca ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. Mathematics is not one of the officia ✅` ×1; `NONE The Nobel Prize in Mathematics does not exist. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. There is no Nobel Prize in Mat ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. Mathematics is not included among the ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. Mathematics is not among the official ✅` ×1
- **model_sonnet_5_5**: `NONE ✅` ×5
- **model_opus_5_5**: `There is no Nobel Prize in Mathematics. NONE ✅` ×1; `NONE ✅` ×4
- **thinking_8000**: `NONE ✅` ×5
- **tools_websearch**: `NONE The question contains a false premise. There is no Nobel Prize in Mathematics. The most prestigious mathematics award is the Abel Prize, which was awarded to Karen Uhlenbeck in 2019. Sources: - [ ✅` ×1; `NONE The question contains a false premise. There is no Nobel Prize in Mathematics. The closest equivalent is the Abel Prize, which is often referred to as the mathematics equivalent of the Nobel Priz ✅` ×1; `NONE The question contains a false premise. There is no Nobel Prize in Mathematics. The prize you may be thinking of is the Abel Prize (often called the "Nobel Prize of Mathematics"), but that is not  ✅` ×1; `NONE The question contains a false premise. There is no Nobel Prize in Mathematics. The Nobel Prize categories are for Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Scien ✅` ×1; `NONE The question contains a false premise. There is no Nobel Prize in Mathematics. The award given in 2019 that is often referred to as the "mathematics Nobel" is the Abel Prize, which was won by Kar ✅` ×1
- **system_careful**: `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. Mathematics is not one of the officia ✅` ×3; `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. The most prestigious mathematics awar ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The prize you're referring to is the Abel Prize, which is sometimes called the "Nobel Prize of Mathematics." The 2019 Abel Prize was awarded to Karen Uhlen ✅` ×1

