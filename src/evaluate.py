#!/usr/bin/env python3
"""Script 3: Evaluation across 5 folds with error analysis."""

import argparse
import csv
import json
import logging
import random
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import (
    accuracy_score, classification_report, f1_score,
    precision_score, recall_score,
)
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent                   # src/
PROJECT_ROOT = HERE.parent                               # repo root
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"                 # folds + JSON configs
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "results"           # checkpoints + reports


def seed_everything(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def load_model_and_tokenizer(checkpoint_dir: Path, device: torch.device):
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    model_dir = checkpoint_dir / "deberta_asc_best"
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.to(device)
    model.eval()
    return model, tokenizer


def score_pairs(model, tokenizer, sentences, definitions, device, max_length=384, batch_size=32):
    """Score a list of (sentence, definition) pairs. Returns list of P(label=1) scores."""
    scores = []
    for i in range(0, len(sentences), batch_size):
        batch_sents = sentences[i:i + batch_size]
        batch_defs = definitions[i:i + batch_size]
        enc = tokenizer(
            batch_sents, batch_defs,
            max_length=max_length, truncation=True, padding=True,
            return_tensors="pt",
        )
        enc = {k: v.to(device) for k, v in enc.items()}
        with torch.no_grad():
            logits = model(**enc).logits
        probs = torch.softmax(logits, dim=-1)[:, 1].cpu().numpy()
        scores.extend(probs.tolist())
    return scores


def aggregate_fold_predictions(data_dir: Path, results_dir: Path,
                               device: torch.device, max_length: int = 384):
    """Load each fold's best checkpoint, score that fold's test set, combine."""
    all_predictions = []

    for fold_i in range(5):
        ckpt_dir = results_dir / "checkpoints" / f"fold_{fold_i}"
        test_path = data_dir / "folds" / f"fold_{fold_i}" / "test.csv"
        if not ckpt_dir.exists() or not test_path.exists():
            log.warning("Fold %d missing checkpoint or test file, skipping", fold_i)
            continue

        model, tokenizer = load_model_and_tokenizer(ckpt_dir, device)
        rows = list(csv.DictReader(open(test_path, encoding="utf-8")))

        sentences = [r["sentence"] for r in rows]
        definitions = [r["asc_definition"] for r in rows]
        scores = score_pairs(model, tokenizer, sentences, definitions, device, max_length)

        for r, s in zip(rows, scores):
            all_predictions.append({
                **r,
                "score": s,
                "pred_label": 1 if s >= 0.5 else 0,
                "fold": fold_i,
            })

        del model
        if device.type == "mps":
            torch.mps.empty_cache()
        elif device.type == "cuda":
            torch.cuda.empty_cache()

        log.info("Fold %d: scored %d test rows", fold_i, len(rows))

    return all_predictions


def core_metrics(predictions: list[dict]) -> dict:
    """Compute overall and per-Situation metrics."""
    y_true = [int(p["label"]) for p in predictions]
    y_pred = [p["pred_label"] for p in predictions]

    overall = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_weighted": f1_score(y_true, y_pred, average="weighted", zero_division=0),
    }

    # Per-tier accuracy (neg rows only)
    tier_acc = {}
    for tier in ("T1", "T2", "T3"):
        tier_preds = [(int(p["label"]), p["pred_label"]) for p in predictions
                      if p.get("tier") == tier]
        if tier_preds:
            t, p_ = zip(*tier_preds)
            tier_acc[tier] = accuracy_score(t, p_)
        else:
            tier_acc[tier] = None

    # Per-Situation F1
    by_sit = defaultdict(lambda: {"true": [], "pred": []})
    for p in predictions:
        by_sit[p["target_situation"]]["true"].append(int(p["label"]))
        by_sit[p["target_situation"]]["pred"].append(p["pred_label"])

    per_sit = {}
    for sit, data in sorted(by_sit.items()):
        per_sit[sit] = {
            "f1": f1_score(data["true"], data["pred"], average="binary", zero_division=0),
            "precision": precision_score(data["true"], data["pred"], zero_division=0),
            "recall": recall_score(data["true"], data["pred"], zero_division=0),
            "support": len(data["true"]),
        }

    return {"overall": overall, "tier_accuracy": tier_acc, "per_situation": per_sit}


def candidate_constrained_eval(
    predictions: list[dict],
    verb_candidates: dict,
    asc_definitions: dict,
    model, tokenizer, device, max_length: int = 384,
) -> dict:
    """For each positive test row, score against only candidate Situations for its verb."""
    pos_preds = [p for p in predictions if int(p["label"]) == 1]

    correct = 0
    total = 0
    unseen_verbs = 0
    results_by_sit = defaultdict(lambda: {"correct": 0, "total": 0})

    for p in tqdm(pos_preds, desc="Constrained eval"):
        verb = p.get("verb_lemma", "")
        gold_sit = p["target_situation"]
        candidates = verb_candidates.get(verb, list(asc_definitions.keys()))

        if verb not in verb_candidates:
            unseen_verbs += 1

        if gold_sit not in candidates:
            candidates = list(set(candidates + [gold_sit]))

        sents = [p["sentence"]] * len(candidates)
        defs = [asc_definitions[c] for c in candidates]
        scores = score_pairs(model, tokenizer, sents, defs, device, max_length)

        best_idx = int(np.argmax(scores))
        pred_sit = candidates[best_idx]

        if pred_sit == gold_sit:
            correct += 1
            results_by_sit[gold_sit]["correct"] += 1
        results_by_sit[gold_sit]["total"] += 1
        total += 1

    constrained_acc = correct / max(1, total)
    return {
        "constrained_accuracy": constrained_acc,
        "total": total,
        "correct": correct,
        "unseen_verbs": unseen_verbs,
        "per_situation": {k: v["correct"] / max(1, v["total"])
                          for k, v in results_by_sit.items()},
    }


def random_baseline(predictions: list[dict], verb_candidates: dict) -> dict:
    """Random selection among candidates for each verb."""
    pos_preds = [p for p in predictions if int(p["label"]) == 1]
    correct = 0
    total = 0
    for p in pos_preds:
        verb = p.get("verb_lemma", "")
        gold = p["target_situation"]
        candidates = verb_candidates.get(verb, [""])
        if candidates and random.choice(candidates) == gold:
            correct += 1
        total += 1
    return {"random_accuracy": correct / max(1, total), "total": total}


def corpus_vs_synthetic(predictions: list[dict]) -> dict:
    """Compare F1 for corpus-attested vs. synthetic rows."""
    results = {}
    for source_type in ("corpus", "synthetic"):
        if source_type == "synthetic":
            subset = [p for p in predictions if p.get("match_path") == "synthetic"]
        else:
            subset = [p for p in predictions if p.get("match_path", "") != "synthetic"]
        if subset:
            y_true = [int(p["label"]) for p in subset]
            y_pred = [p["pred_label"] for p in subset]
            results[source_type] = {
                "f1": f1_score(y_true, y_pred, average="binary", zero_division=0),
                "count": len(subset),
            }
    return results


def write_report(metrics: dict, constrained: dict, baseline: dict,
                 corpus_synth: dict, tier_acc: dict, out_path: Path):
    """Write evaluation_report.md."""
    lines = ["# ASC Cross-Encoder Evaluation Report\n"]

    lines.append("## Overall Metrics\n")
    o = metrics["overall"]
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    for k, v in o.items():
        lines.append(f"| {k} | {v:.4f} |")

    lines.append("\n## Per-Tier Negative Accuracy\n")
    lines.append("| Tier | Accuracy |")
    lines.append("|------|----------|")
    for tier in ("T1", "T2", "T3"):
        val = tier_acc.get(tier)
        lines.append(f"| {tier} | {f'{val:.4f}' if val is not None else 'N/A'} |")

    lines.append("\n## Candidate-Constrained Evaluation\n")
    lines.append(f"- Constrained accuracy: **{constrained['constrained_accuracy']:.4f}** ({constrained['correct']}/{constrained['total']})")
    lines.append(f"- Unseen verbs (fell back to all 62): {constrained['unseen_verbs']}")
    lines.append(f"- Random baseline accuracy: **{baseline['random_accuracy']:.4f}**")
    lines.append(f"- Lift over random: **{constrained['constrained_accuracy'] - baseline['random_accuracy']:+.4f}**")

    lines.append("\n## Corpus vs. Synthetic\n")
    lines.append("| Source | F1 | Count |")
    lines.append("|--------|-----|-------|")
    for src, data in corpus_synth.items():
        lines.append(f"| {src} | {data['f1']:.4f} | {data['count']} |")

    lines.append("\n## Per-Situation F1\n")
    lines.append("| Situation | F1 | Precision | Recall | Support |")
    lines.append("|-----------|-----|-----------|--------|---------|")
    ps = metrics["per_situation"]
    for sit in sorted(ps):
        s = ps[sit]
        flag = " ⚠" if s["f1"] < 0.7 else ""
        lines.append(f"| {sit}{flag} | {s['f1']:.3f} | {s['precision']:.3f} | {s['recall']:.3f} | {s['support']} |")

    # Flag summary
    flagged = [sit for sit, s in ps.items() if s["f1"] < 0.7]
    lines.append(f"\n## Situations Needing Attention (F1 < 0.7)\n")
    if flagged:
        for sit in flagged:
            lines.append(f"- **{sit}**: F1={ps[sit]['f1']:.3f}")
    else:
        lines.append("None — all Situations above 0.7 threshold.")

    t1_low = [tier for tier, val in tier_acc.items() if val and val < 0.6]
    if t1_low:
        lines.append(f"\n## Tier Accuracy Warnings\n")
        for t in t1_low:
            lines.append(f"- **{t}** accuracy below 60%: {tier_acc[t]:.3f}")

    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    log.info("Report written to %s", out_path)


def main():
    parser = argparse.ArgumentParser(description="Evaluate ASC cross-encoder")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR,
                        help=f"Directory holding folds/ and *.json configs "
                             f"(default: {DEFAULT_DATA_DIR})")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR,
                        help=f"Directory holding checkpoints/ and cv_summary.json "
                             f"(default: {DEFAULT_RESULTS_DIR})")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-length", type=int, default=384)
    args = parser.parse_args()

    seed_everything(args.seed)
    device = get_device()
    data_dir = args.data_dir
    results_dir = args.results_dir

    # 3a. Aggregate predictions across folds
    log.info("Aggregating predictions across 5 folds...")
    predictions = aggregate_fold_predictions(data_dir, results_dir, device, args.max_length)
    log.info("Total test predictions: %d", len(predictions))

    # 3b. Core metrics
    metrics = core_metrics(predictions)
    log.info("Overall F1 (macro): %.4f", metrics["overall"]["f1_macro"])
    log.info("Tier accuracy: %s", metrics["tier_accuracy"])

    # 3c. Candidate-constrained evaluation
    verb_candidates = json.load(open(data_dir / "verb_candidates.json"))
    asc_definitions = json.load(open(data_dir / "asc_definitions.json"))

    # Use the best fold's model for constrained eval
    cv_summary = json.load(open(results_dir / "cv_summary.json"))
    best_fold = cv_summary.get("best_fold", 0)
    log.info("Using fold %d for constrained evaluation", best_fold)
    model, tokenizer = load_model_and_tokenizer(
        results_dir / "checkpoints" / f"fold_{best_fold}", device
    )

    constrained = candidate_constrained_eval(
        predictions, verb_candidates, asc_definitions, model, tokenizer, device, args.max_length
    )
    log.info("Constrained accuracy: %.4f (%d/%d)",
             constrained["constrained_accuracy"], constrained["correct"], constrained["total"])

    # 3d. Baseline
    baseline = random_baseline(predictions, verb_candidates)
    log.info("Random baseline: %.4f", baseline["random_accuracy"])

    # 3f. Corpus vs synthetic
    corpus_synth = corpus_vs_synthetic(predictions)
    for src, data in corpus_synth.items():
        log.info("%s F1: %.4f (n=%d)", src, data["f1"], data["count"])

    # 3g. Write report
    results_dir.mkdir(parents=True, exist_ok=True)
    write_report(
        metrics, constrained, baseline, corpus_synth,
        metrics["tier_accuracy"],
        results_dir / "evaluation_report.md",
    )

    del model
    log.info("Done.")


if __name__ == "__main__":
    main()
