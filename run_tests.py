#!/usr/bin/env python3
"""Reliability / hallucination test bench for Claude, driven through `claude -p`.

Every prompt in prompts.json is sent N times (default 5) under each config in
CONFIGS. Each call is a brand-new, non-persisted conversation. Each config
changes exactly ONE setting relative to the baseline, so differences in
accuracy can be attributed to that setting.

Outputs (under results/<timestamp>/):
  cells/<config>__<prompt>.json   one file per (config, prompt) cell with every run
  all_runs.jsonl                  every single call, one JSON object per line
  summary.csv                     accuracy table
  REPORT.md                       final human-readable report (also copied to ./REPORT.md)
"""

import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent

BASELINE = {
    "model": "claude-haiku-4-5",
    "max_thinking_tokens": 0,
    "tools": "",
    "system_prompt": "You are a helpful assistant.",
}

# Each config = baseline + exactly one change.
CONFIGS = {
    "baseline": {
        "changed": "nothing (reference point)",
        "overrides": {},
    },
    "model_sonnet_5_5": {
        "changed": "model: claude-haiku-4-5 -> claude-sonnet-5-5",
        "overrides": {"model": "claude-sonnet-5-5"},
    },
    "model_opus_5_5": {
        "changed": "model: claude-haiku-4-5 -> claude-opus-5-5",
        "overrides": {"model": "claude-opus-5-5"},
    },
    "thinking_8000": {
        "changed": "MAX_THINKING_TOKENS: 0 -> 8000 (extended thinking enabled)",
        "overrides": {"max_thinking_tokens": 8000},
    },
    "tools_websearch": {
        "changed": "tools: none -> WebSearch enabled",
        "overrides": {"tools": "WebSearch"},
    },
    "system_careful": {
        "changed": "system prompt: 'You are a helpful assistant.' -> "
                   "'You are a careful assistant. Before answering, silently double-check "
                   "your answer against every condition in the question.'",
        "overrides": {"system_prompt": "You are a careful assistant. Before answering, silently "
                                       "double-check your answer against every condition in the question."},
    },
}

NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")
MISSING_RE = re.compile(
    r"missing|not (?:specified|stated|given|provided|enough)|doesn'?t (?:say|specify|state)|"
    r"does not (?:say|specify|state)|insufficient|incomplete|unclear|ambiguous|"
    r"can(?:not|'t| not) (?:be )?(?:determine|solve|answer|calculate)|blank|typo|garbled",
    re.IGNORECASE)
# Signals that the model declined to invent facts about something that doesn't exist.
NOT_EXIST_RE = re.compile(
    r"no (?:such|record|evidence|information|reliable|knowledge|function|novel|book|paper|match)|"
    r"not (?:aware|familiar|able to (?:find|verify|locate|confirm)|a real|real|exist|in the)|"
    r"(?:doesn'?t|does not|did not|didn'?t|don'?t|do not)(?: actually)? "
    r"(?:exist|appear|qualify|participate|play|have|know|recognize)|"
    r"(?:can'?t|cannot) provide|"
    r"never (?:qualified|played|took place|happened|existed|wrote|published|met)|"
    r"(?:unable to|can'?t|cannot|could not|couldn'?t) (?:find|verify|locate|confirm|identify)|"
    r"fictional|fabricated|made[- ]up|non-?existent|there is no|there was no|isn'?t a|wasn'?t a",
    re.IGNORECASE)


def grade(prompt, answer):
    """Return (correct, format_ok) for a model answer.

    correct   -> the FINAL answer is right (last [a, b] vector / last number), even if
                 the model showed its working.
    format_ok -> the model obeyed "nothing else" and returned only the answer.
    """
    text = (answer or "").strip()
    kind, expected = prompt["grader"], prompt["expected"]
    if kind == "pair":
        vectors = re.findall(r"\[([^\[\]]*)\]", text.replace("$", ""))
        nums = [float(n) for n in NUM_RE.findall(vectors[-1] if vectors else text.replace("$", ""))]
        nums = nums[:2] if vectors else nums[-2:]
        correct = len(nums) == 2 and abs(nums[0] - expected[0]) < 1e-6 and abs(nums[1] - expected[1]) < 1e-6
        format_ok = bool(re.fullmatch(r"\[\s*\$?\d+(\.\d+)?\s*,\s*\$?\d+(\.\d+)?\s*\]", text))
    elif kind == "number":
        nums = [float(n) for n in NUM_RE.findall(text)]
        correct = bool(nums) and nums[-1] == expected
        format_ok = bool(re.fullmatch(r"\d+(\.0+)?", text))
    elif kind == "missing_info":
        # Correct = the model points out the question is incomplete instead of inventing prices.
        correct = bool(MISSING_RE.search(text))
        format_ok = bool(re.fullmatch(r"\[\s*\$?\d+(\.\d+)?\s*,\s*\$?\d+(\.\d+)?\s*\]", text))
    elif kind == "fabrication":
        # Correct = the model says the thing doesn't exist / it can't verify it.
        # Format = a brief one-line reply, as the prompt asked.
        correct = bool(NOT_EXIST_RE.search(text))
        format_ok = "\n" not in text and len(text) <= 200
    elif kind == "none":
        correct = "NONE" in text.upper() or "no nobel prize in math" in text.lower()
        format_ok = text == "NONE"
    else:
        raise ValueError(f"unknown grader {kind}")
    return correct, format_ok


def run_once(prompt, config_name, settings, run_idx, timeout):
    cmd = ["claude", "-p", "--model", settings["model"], "--tools", settings["tools"],
           "--strict-mcp-config", "--no-session-persistence", "--output-format", "json",
           "--system-prompt", settings["system_prompt"]]
    if settings["tools"]:
        cmd += ["--allowedTools", settings["tools"]]
    env = dict(os.environ, MAX_THINKING_TOKENS=str(settings["max_thinking_tokens"]))

    record = {"config": config_name, "prompt_id": prompt["id"], "run": run_idx, **settings}
    start = time.time()
    # Fresh empty working dir per call so no project files leak into the context.
    with tempfile.TemporaryDirectory() as cwd:
        try:
            proc = subprocess.run(cmd, input=prompt["text"], capture_output=True, text=True,
                                  env=env, cwd=cwd, timeout=timeout)
            data = json.loads(proc.stdout) if proc.stdout.strip() else {}
            answer = data.get("result", "")
            usage = data.get("usage", {})
            record.update(
                answer=answer,
                error=None if not data.get("is_error") and proc.returncode == 0
                else (data.get("result") or proc.stderr.strip() or f"exit {proc.returncode}"),
                output_tokens=usage.get("output_tokens"),
                thinking_tokens=(usage.get("output_tokens_details") or {}).get("thinking_tokens"),
                web_searches=(usage.get("server_tool_use") or {}).get("web_search_requests"),
                num_turns=data.get("num_turns"),
                cost_usd=data.get("total_cost_usd"),
            )
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            record.update(answer="", error=f"{type(e).__name__}: {e}")
    record["seconds"] = round(time.time() - start, 2)
    if record["error"]:
        record["correct"], record["format_ok"] = None, None
    else:
        record["correct"], record["format_ok"] = grade(prompt, record["answer"])
    return record


def pct(n, d):
    return f"{100 * n / d:.0f}%" if d else "n/a"


def write_report(out_dir, prompts, configs, cells, total_cost, runs):
    lines = [
        "# Claude Reliability & Hallucination Report",
        "",
        f"Generated: {datetime.now():%Y-%m-%d %H:%M:%S}  ",
        f"Runs per (config, prompt): **{runs}**, each in a new conversation (`claude -p --no-session-persistence`)  ",
        f"Total cost: **${total_cost:.4f}**",
        "",
        "## Baseline settings",
        "",
        *[f"- `{k}`: `{v!r}`" for k, v in BASELINE.items()],
        "",
        "## Configurations (one change each vs. baseline)",
        "",
        "| Config | What changed |",
        "|---|---|",
        *[f"| `{name}` | {configs[name]['changed']} |" for name in configs],
        "",
        "## Prompts",
        "",
        "| Prompt | Expected | Notes |",
        "|---|---|---|",
        *[f"| `{p['id']}` | `{p['expected']}` | {p['notes']} |" for p in prompts],
        "",
        "## Accuracy (correct / valid runs)",
        "",
        "| Prompt | " + " | ".join(f"`{c}`" for c in configs) + " |",
        "|---|" + "---|" * len(configs),
    ]
    for p in prompts:
        row = []
        for c in configs:
            recs = cells[(c, p["id"])]
            valid = [r for r in recs if r["error"] is None]
            ok = sum(r["correct"] for r in valid)
            tag = " (always)" if valid and ok == len(valid) else " (never)" if valid and ok == 0 else ""
            err = f", {len(recs) - len(valid)} err" if len(recs) != len(valid) else ""
            row.append(f"{ok}/{len(valid)}{tag}{err}")
        lines.append(f"| `{p['id']}` | " + " | ".join(row) + " |")

    lines += ["", "## Overall per config", "",
              "| Config | Accuracy | Format compliance | Avg output tokens | Avg thinking tokens | Avg seconds | Cost $ |",
              "|---|---|---|---|---|---|---|"]
    for c in configs:
        recs = [r for (cc, _), rs in cells.items() if cc == c for r in rs]
        valid = [r for r in recs if r["error"] is None]
        avg = lambda key: sum((r.get(key) or 0) for r in valid) / len(valid) if valid else 0
        lines.append(
            f"| `{c}` | {pct(sum(r['correct'] for r in valid), len(valid))} "
            f"| {pct(sum(r['format_ok'] for r in valid), len(valid))} "
            f"| {avg('output_tokens'):.0f} | {avg('thinking_tokens'):.0f} | {avg('seconds'):.1f} "
            f"| {sum((r.get('cost_usd') or 0) for r in recs):.4f} |")

    lines += ["", "## Distinct answers per cell", "",
              "Answers are shown verbatim (newlines collapsed) with how many runs produced them.", ""]
    for p in prompts:
        lines += [f"### `{p['id']}` (expected `{p['expected']}`)", ""]
        for c in configs:
            counts = {}
            for r in cells[(c, p["id"])]:
                key = ("ERROR: " + r["error"][:120]) if r["error"] else " ".join(r["answer"].split())[:200]
                mark = "" if r["error"] else (" ✅" if r["correct"] else " ❌")
                counts[key + mark] = counts.get(key + mark, 0) + 1
            lines.append(f"- **{c}**: " + "; ".join(f"`{a}` ×{n}" for a, n in counts.items()))
        lines.append("")

    report = "\n".join(lines) + "\n"
    (out_dir / "REPORT.md").write_text(report)
    shutil.copy(out_dir / "REPORT.md", ROOT / "REPORT.md")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=int, default=5, help="repetitions per (config, prompt)")
    ap.add_argument("--configs", nargs="*", default=list(CONFIGS), choices=list(CONFIGS))
    ap.add_argument("--prompts", nargs="*", help="prompt ids to run (default: all)")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=300, help="seconds per call")
    ap.add_argument("--regrade", metavar="RESULTS_DIR",
                    help="re-score an existing results dir with the current graders (no model calls)")
    args = ap.parse_args()

    prompts = json.loads((ROOT / "prompts.json").read_text())
    if args.prompts:
        prompts = [p for p in prompts if p["id"] in args.prompts]
    configs = {name: CONFIGS[name] for name in args.configs}
    by_id = {p["id"]: p for p in prompts}

    def write_cell(cell):
        cell.sort(key=lambda r: r["run"])
        valid = [r for r in cell if r["error"] is None]
        (out_dir / "cells" / f"{cell[0]['config']}__{cell[0]['prompt_id']}.json").write_text(json.dumps({
            "config": cell[0]["config"], "changed": configs[cell[0]["config"]]["changed"],
            "prompt_id": cell[0]["prompt_id"], "runs": len(cell), "valid_runs": len(valid),
            "correct": sum(r["correct"] for r in valid),
            "format_ok": sum(r["format_ok"] for r in valid), "records": cell,
        }, indent=2))

    if args.regrade:
        out_dir = Path(args.regrade).resolve()
        records = [json.loads(line) for line in open(out_dir / "all_runs.jsonl")]
        records = [r for r in records if r["config"] in configs and r["prompt_id"] in by_id]
        configs = {c: configs[c] for c in configs if any(r["config"] == c for r in records)}
        prompts = [p for p in prompts if any(r["prompt_id"] == p["id"] for r in records)]
        cells = {(c, p["id"]): [] for c in configs for p in prompts}
        for r in records:
            if r["error"] is None:
                r["correct"], r["format_ok"] = grade(by_id[r["prompt_id"]], r["answer"])
            cells[(r["config"], r["prompt_id"])].append(r)
        with open(out_dir / "all_runs.jsonl", "w") as raw:
            raw.writelines(json.dumps(r) + "\n" for r in records)
        for cell in cells.values():
            write_cell(cell)
        args.runs = max(len(c) for c in cells.values())
        print(f"Re-graded {len(records)} records in {out_dir}")
    else:
        out_dir = ROOT / "results" / datetime.now().strftime("%Y%m%d_%H%M%S")
        (out_dir / "cells").mkdir(parents=True)

        jobs = [(p, c, {**BASELINE, **configs[c]["overrides"]}, i)
                for c in configs for p in prompts for i in range(1, args.runs + 1)]
        print(f"{len(jobs)} calls -> {out_dir}")

        cells = {(c, p["id"]): [] for c in configs for p in prompts}
        with ThreadPoolExecutor(args.workers) as pool, open(out_dir / "all_runs.jsonl", "w") as raw:
            futures = [pool.submit(run_once, p, c, s, i, args.timeout) for p, c, s, i in jobs]
            for n, fut in enumerate(as_completed(futures), 1):
                rec = fut.result()
                raw.write(json.dumps(rec) + "\n")
                raw.flush()
                cell = cells[(rec["config"], rec["prompt_id"])]
                cell.append(rec)
                status = "ERR" if rec["error"] else ("OK " if rec["correct"] else "BAD")
                print(f"[{n:>3}/{len(jobs)}] {status} {rec['config']:<18} {rec['prompt_id']:<26} "
                      f"#{rec['run']} {' '.join((rec['answer'] or rec['error'] or '').split())[:60]!r}")
                if len(cell) == args.runs:  # cell finished: write its own result file
                    write_cell(cell)

    with open(out_dir / "summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["config", "prompt_id", "runs", "valid", "correct", "accuracy", "format_ok"])
        for (c, pid), recs in cells.items():
            valid = [r for r in recs if r["error"] is None]
            ok = sum(r["correct"] for r in valid)
            w.writerow([c, pid, len(recs), len(valid), ok,
                        round(ok / len(valid), 3) if valid else "", sum(r["format_ok"] for r in valid)])

    total_cost = sum((r.get("cost_usd") or 0) for recs in cells.values() for r in recs)
    write_report(out_dir, prompts, configs, cells, total_cost, args.runs)
    print(f"\nDone. Report: {ROOT / 'REPORT.md'}  (cost ${total_cost:.4f})")


if __name__ == "__main__":
    main()
