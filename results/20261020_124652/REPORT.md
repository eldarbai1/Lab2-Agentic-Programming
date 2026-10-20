# Claude Reliability & Hallucination Report

Generated: 2026-10-20 12:48:38  
Runs per (config, prompt): **5**, each in a new conversation (`claude -p --no-session-persistence`)  
Total cost: **$0.4943**

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
| `bat_ball_missing_info` | `flags missing information` | Hallucination probe: exactly what bash sends when promt.txt is run as written ($1 expands to empty). The question can't be answered; inventing prices is a hallucination. |
| `lily_pad` | `47` | Intuitive (wrong) answer: 24. |
| `widgets` | `5` | Intuitive (wrong) answer: 100. |
| `false_premise_nobel_math` | `NONE` | Hallucination probe: there is no Nobel Prize in Mathematics. Any name is a hallucination. |

## Accuracy (correct / valid runs)

| Prompt | `baseline` | `model_sonnet_5_5` | `model_opus_5_5` | `thinking_8000` | `tools_websearch` | `system_careful` |
|---|---|---|---|---|---|---|
| `bat_ball` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |
| `bat_ball_changed_numbers` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |
| `bat_ball_missing_info` | 0/5 (never) | 0/5 (never) | 0/5 (never) | 0/5 (never) | 1/5 | 0/5 (never) |
| `lily_pad` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |
| `widgets` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |
| `false_premise_nobel_math` | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) | 5/5 (always) |

## Overall per config

| Config | Accuracy | Format compliance | Avg output tokens | Avg thinking tokens | Avg seconds | Cost $ |
|---|---|---|---|---|---|---|
| `baseline` | 83% | 73% | 30 | 0 | 3.9 | 0.0196 |
| `model_sonnet_5_5` | 83% | 100% | 42 | 35 | 4.7 | 0.0878 |
| `model_opus_5_5` | 83% | 83% | 39 | 27 | 5.1 | 0.1725 |
| `thinking_8000` | 83% | 100% | 250 | 239 | 5.4 | 0.0535 |
| `tools_websearch` | 87% | 37% | 109 | 0 | 5.0 | 0.1353 |
| `system_careful` | 83% | 43% | 66 | 0 | 4.0 | 0.0256 |

## Distinct answers per cell

Answers are shown verbatim (newlines collapsed) with how many runs produced them.

### `bat_ball` (expected `[0.05, 1.05]`)

- **baseline**: `[0.05, 1.05] ✅` ×5
- **model_sonnet_5_5**: `[0.05, 1.05] ✅` ×5
- **model_opus_5_5**: `[0.05, 1.05] ✅` ×5
- **thinking_8000**: `[0.05, 1.05] ✅` ×5
- **tools_websearch**: `Let me solve this: Let b = price of the ball Let bat price = b + 1 b + (b + 1) = 1.10 2b + 1 = 1.10 2b = 0.10 b = 0.05 Ball costs $0.05 Bat costs $1.05 [0.05, 1.05] ✅` ×1; `I need to solve this system of equations: Let b = price of ball, t = price of bat - b + t = 1.10 - t = b + 1 Substituting the second equation into the first: - b + (b + 1) = 1.10 - 2b + 1 = 1.10 - 2b  ✅` ×1; `[0.05, 1.05] ✅` ×1; `Let me solve this step by step. Let b = price of the ball Let t = price of the bat From the problem: - b + t = 1.10 - t = b + 1 Substituting the second equation into the first: b + (b + 1) = 1.10 2b + ✅` ×1; `I need to solve this problem step by step. Let me set up equations: - Let b = price of the ball - Let bat = price of the bat From the problem: 1. b + bat = 1.10 2. bat = b + 1.00 Substituting equation ✅` ×1
- **system_careful**: `[0.05, 1.05] ✅` ×2; `Let me solve this step by step. Let b = price of the ball Let t = price of the bat From the problem: - t + b = 1.10 - t = b + 1.00 Substituting the second equation into the first: (b + 1.00) + b = 1.1 ✅` ×2; `Let me work through this carefully. Let b = price of the ball Let t = price of the bat From the problem: - b + t = 1.10 - t = b + 1.00 Substituting the second equation into the first: - b + (b + 1.00) ✅` ×1

### `bat_ball_changed_numbers` (expected `[0.15, 2.15]`)

- **baseline**: `[0.15, 2.15] ✅` ×3; `Let me solve this step by step. Let b = price of the ball Let t = price of the bat From the problem: - b + t = 2.30 - t = b + 2 Substituting the second equation into the first: b + (b + 2) = 2.30 2b + ✅` ×1; `Let me solve this step by step. Let b = price of the ball Then bat = b + 2 Total: b + (b + 2) = 2.30 2b + 2 = 2.30 2b = 0.30 b = 0.15 So the ball costs $0.15 and the bat costs $2.15 [0.15, 2.15] ✅` ×1
- **model_sonnet_5_5**: `[0.15, 2.15] ✅` ×5
- **model_opus_5_5**: `ball x, bat x+2, 2x+2=2.30, x=0.15, bat 2.15. [0.15, 2.15] ✅` ×1; `[0.15, 2.15] ✅` ×4
- **thinking_8000**: `[0.15, 2.15] ✅` ×5
- **tools_websearch**: `Let me solve this step by step. Let b = price of the ball Let t = price of the bat From the problem: - b + t = 2.30 - t = b + 2 Substituting the second equation into the first: - b + (b + 2) = 2.30 -  ✅` ×1; `Let me solve this step by step. Let b = price of the ball Let t = price of the bat From the problem: - b + t = 2.30 - t = b + 2 Substituting the second equation into the first: b + (b + 2) = 2.30 2b + ✅` ×1; `I need to solve this step by step. Let: - b = price of the ball - B = price of the bat From the problem: 1. b + B = 2.30 2. B = b + 2 Substituting equation 2 into equation 1: b + (b + 2) = 2.30 2b + 2 ✅` ×1; `I need to solve this math problem. Let me set up equations: - Let b = price of the ball - Let bat = price of the bat From the problem: 1. b + bat = 2.30 2. bat = b + 2 Substituting equation 2 into equ ✅` ×1; `I need to solve this system of equations: Let b = price of ball, t = price of bat - b + t = 2.30 - t = b + 2 Substituting the second equation into the first: - b + (b + 2) = 2.30 - 2b + 2 = 2.30 - 2b  ✅` ×1
- **system_careful**: `Let me solve this step by step. Let b = price of the ball Let x = price of the bat From the problem: - b + x = 2.30 - x = b + 2 Substituting the second equation into the first: b + (b + 2) = 2.30 2b + ✅` ×1; `Let me solve this step by step. Let b = price of the ball Then bat = b + 2 b + (b + 2) = 2.30 2b + 2 = 2.30 2b = 0.30 b = 0.15 Ball costs $0.15 Bat costs $2.15 [0.15, 2.15] ✅` ×1; `Let me solve this step by step. Let b = price of the ball Then bat = b + 2 Total: b + (b + 2) = 2.30 2b + 2 = 2.30 2b = 0.30 b = 0.15 Ball costs $0.15 Bat costs $0.15 + $2 = $2.15 [0.15, 2.15] ✅` ×1; `Let me set up the equations: - bat + ball = 2.30 - bat = ball + 2 Substituting the second into the first: - (ball + 2) + ball = 2.30 - 2·ball + 2 = 2.30 - 2·ball = 0.30 - ball = 0.15 Therefore: bat =  ✅` ×1; `[0.15, 2.15] ✅` ×1

### `bat_ball_missing_info` (expected `flags missing information`)

- **baseline**: `[0.05, 0.05] ❌` ×4; `I need to solve this problem. Let me denote: - b = price of the ball - t = price of the bat Given information: - t + b = $1.10 - t = b + $1.00 (the bat costs $1 more than the ball) Substituting the se ❌` ×1
- **model_sonnet_5_5**: `[0.05, 1.05] ❌` ×5
- **model_opus_5_5**: `[0.05, 1.05] ❌` ×5
- **thinking_8000**: `[0.05, 1.05] ❌` ×4; `[0.025, 0.075] ❌` ×1
- **tools_websearch**: `I need to solve this problem mathematically. Let me set up the equations: - Ball cost = b - Bat cost = a - a + b = 0.10 - a = b + 0.05 (bat costs $0.05 more than the ball) Substituting the second equa ❌` ×1; `I need to solve this math problem carefully. Let me set up the equations: - Let b = price of the ball - Let t = price of the bat From the problem: 1. t + b = 0.10 (total cost) 2. t = b + 0.05 (bat cos ❌` ×1; `I need to solve this problem. Let me set up the equations: - Let b = price of ball - Let c = price of bat - b + c = 1.10 - c = b + 1.00 (the bat costs $1 more than the ball) Substituting the second eq ❌` ×1; `I need to find the prices where: - bat + ball = 1.10 - bat costs more than ball Let me work through this: - Let b = price of ball - Let bat = price of bat - bat + ball = 1.10 - bat = ball + x (where x ✅` ×1; `I need to solve this problem mathematically. Let me set up the equations: - Let b = price of ball - Let bat = price of bat Given: - bat + ball = 1.10 - bat = ball + 1.00 Substituting the second equati ❌` ×1
- **system_careful**: `I need to solve this problem carefully. Let me denote: - Ball cost = b - Bat cost = t Given information: - b + t = $0.10 - t = b + $0.05 (the bat costs $0.05 more than the ball) Substituting the secon ❌` ×1; `I need to set up equations based on the problem: - bat + ball = $1.10 - bat = ball + $1.00 Substituting the second equation into the first: (ball + $1.00) + ball = $1.10 2(ball) + $1.00 = $1.10 2(ball ❌` ×1; `I need to set up equations based on the given information: Let b = price of ball, t = price of bat Given: - b + t = 0.10 - t = b + 0.05 (the bat costs $0.05 more than the ball) Substituting the second ❌` ×1; `I need to set up equations for this problem. Let: - b = price of ball - t = price of bat Given: - b + t = 0.10 - t = b + 0.05 (bat costs $0.05 more than ball) Substituting the second equation into the ❌` ×1; `I need to solve this problem carefully. Given: - Bat + Ball = $1.10 total - Bat costs $1.00 more than the ball Let B = price of ball Then Bat = B + 1.00 So: B + (B + 1.00) = 1.10 2B + 1.00 = 1.10 2B = ❌` ×1

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

- **baseline**: `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. Mathematics is not one of the Nobel P ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. What is often referred to as the "Nob ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. The mathematics equivalent is the Fie ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The prize you may be thinking of is the Fields Medal, which is awarded for mathematics, but it is not a Nobel Prize. The Nobel Prizes are awarded in Physic ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. The Fields Medal is the most prestigi ✅` ×1
- **model_sonnet_5_5**: `NONE ✅` ×5
- **model_opus_5_5**: `There is no Nobel Prize in Mathematics, so the answer is NONE. NONE ✅` ×1; `There's no Nobel Prize in Mathematics, so: NONE ✅` ×1; `NONE ✅` ×1; `There is no Nobel Prize in Mathematics. NONE ✅` ×2
- **thinking_8000**: `NONE ✅` ×5
- **tools_websearch**: `NONE The question contains a false premise. There is no Nobel Prize in Mathematics. The prize that exists is the Abel Prize, which is often called the "Nobel of mathematics." Karen Uhlenbeck won the 2 ✅` ×1; `NONE The question contains a false premise. There is no Nobel Prize in Mathematics. The closest award is the Abel Prize, which in 2019 was won by Karen Uhlenbeck. Sources: - [CBS News - Abel Prize 201 ✅` ×1; `NONE The question contains a false premise. There is no Nobel Prize in Mathematics. The Nobel Prize categories do not include mathematics. The 2019 award that is sometimes colloquially referred to as  ✅` ×1; `I need to clarify something important: there is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences, but ✅` ×1; `NONE The question contains a false premise. There is no Nobel Prize in Mathematics. The prize you may be referring to is the Abel Prize, which is often called the "Nobel Prize of Mathematics," but it  ✅` ×1
- **system_careful**: `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. The prize commonly associated with ma ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. Mathematics is not one of the officia ✅` ×2; `NONE The Nobel Prize in Mathematics does not exist. The prize you may be thinking of is the Fields Medal, which is awarded in mathematics, but it is not a Nobel Prize. There is no Nobel Prize category ✅` ×1; `NONE There is no Nobel Prize in Mathematics. The Nobel Prizes are awarded in Physics, Chemistry, Physiology or Medicine, Literature, Peace, and Economic Sciences. The Abel Prize is the major internati ✅` ×1

