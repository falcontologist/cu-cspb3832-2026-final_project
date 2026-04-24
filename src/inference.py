#!/usr/bin/env python3
"""Script 4: End-to-end inference pipeline for ASC classification."""

import argparse
import csv
import json
import logging
import sys
from pathlib import Path

import numpy as np
import torch

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent                   # src/
PROJECT_ROOT = HERE.parent                               # repo root
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"                 # verb_candidates, asc_definitions
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "results"           # checkpoints + cv_summary


def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def load_pipeline(data_dir: Path, results_dir: Path,
                  fold: int | None, ensemble: bool, device: torch.device):
    """Load model(s), tokenizer, verb candidates, and ASC definitions."""
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    verb_candidates = json.load(open(data_dir / "verb_candidates.json"))
    asc_definitions = json.load(open(data_dir / "asc_definitions.json"))

    if fold is None and not ensemble:
        cv_summary = json.load(open(results_dir / "cv_summary.json"))
        fold = cv_summary.get("best_fold", 0)
        log.info("Auto-selected best fold: %d", fold)

    models = []
    tokenizer = None
    if ensemble:
        for fi in range(5):
            ckpt = results_dir / "checkpoints" / f"fold_{fi}" / "deberta_asc_best"
            if ckpt.exists():
                m = AutoModelForSequenceClassification.from_pretrained(ckpt)
                m.to(device)
                m.eval()
                models.append(m)
                if tokenizer is None:
                    tokenizer = AutoTokenizer.from_pretrained(ckpt)
        log.info("Ensemble mode: loaded %d models", len(models))
    else:
        ckpt = results_dir / "checkpoints" / f"fold_{fold}" / "deberta_asc_best"
        m = AutoModelForSequenceClassification.from_pretrained(ckpt)
        m.to(device)
        m.eval()
        models.append(m)
        tokenizer = AutoTokenizer.from_pretrained(ckpt)
        log.info("Single model: fold %d", fold)

    return models, tokenizer, verb_candidates, asc_definitions


def extract_verb(sentence: str) -> str:
    """Use spaCy to extract the main verb (ROOT dependency) and return its lemma."""
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ in ("VERB", "AUX"):
            return token.lemma_
    for token in doc:
        if token.pos_ == "VERB":
            return token.lemma_
    return doc[0].lemma_ if doc else ""


_nlp = None
def get_verb_lemma(sentence: str) -> str:
    """Cached spaCy pipeline for verb extraction."""
    global _nlp
    if _nlp is None:
        import spacy
        _nlp = spacy.load("en_core_web_sm")
    doc = _nlp(sentence)
    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ in ("VERB", "AUX"):
            return token.lemma_
    for token in doc:
        if token.pos_ == "VERB":
            return token.lemma_
    return doc[0].lemma_ if doc else ""


def score_candidates(
    sentence: str,
    candidate_situations: list[str],
    asc_definitions: dict,
    models: list,
    tokenizer,
    device: torch.device,
    max_length: int = 384,
) -> list[tuple[str, float]]:
    """Score sentence against each candidate Situation's definition. Returns sorted (sit, score)."""
    if not candidate_situations:
        return []

    sents = [sentence] * len(candidate_situations)
    defs = [asc_definitions[c] for c in candidate_situations]

    enc = tokenizer(
        sents, defs,
        max_length=max_length, truncation=True, padding=True,
        return_tensors="pt",
    )
    enc = {k: v.to(device) for k, v in enc.items()}

    all_probs = []
    for model in models:
        with torch.no_grad():
            logits = model(**enc).logits
        probs = torch.softmax(logits, dim=-1)[:, 1].cpu().numpy()
        all_probs.append(probs)

    avg_probs = np.mean(all_probs, axis=0)
    results = list(zip(candidate_situations, avg_probs.tolist()))
    results.sort(key=lambda x: -x[1])
    return results


def classify_sentence(
    sentence: str,
    models: list,
    tokenizer,
    verb_candidates: dict,
    asc_definitions: dict,
    device: torch.device,
    max_length: int = 384,
) -> dict:
    """Full pipeline for a single sentence."""
    verb = get_verb_lemma(sentence)
    candidates = verb_candidates.get(verb, list(asc_definitions.keys()))
    fallback = verb not in verb_candidates

    valid_candidates = [c for c in candidates if c in asc_definitions]
    if not valid_candidates:
        valid_candidates = list(asc_definitions.keys())
        fallback = True

    scored = score_candidates(sentence, valid_candidates, asc_definitions,
                              models, tokenizer, device, max_length)

    return {
        "sentence": sentence,
        "verb_lemma": verb,
        "predicted_situation": scored[0][0] if scored else "",
        "score": round(scored[0][1], 4) if scored else 0.0,
        "candidate_count": len(valid_candidates),
        "fallback": fallback,
        "all_scores": {sit: round(s, 4) for sit, s in scored},
    }


def run_interactive(models, tokenizer, verb_candidates, asc_definitions, device, max_length):
    """Interactive mode: read sentences from stdin."""
    print("ASC Classifier — enter sentences (Ctrl-D to quit):")
    for line in sys.stdin:
        sentence = line.strip()
        if not sentence:
            continue
        result = classify_sentence(sentence, models, tokenizer, verb_candidates,
                                    asc_definitions, device, max_length)
        print(f"\n  Verb: {result['verb_lemma']}")
        print(f"  Prediction: {result['predicted_situation']} (score={result['score']:.4f})")
        print(f"  Candidates ({result['candidate_count']}):")
        for sit, s in sorted(result["all_scores"].items(), key=lambda x: -x[1]):
            marker = " ←" if sit == result["predicted_situation"] else ""
            print(f"    {sit}: {s:.4f}{marker}")
        if result["fallback"]:
            print("  (verb not in lookup — scored against all 62 Situations)")
        print()


def run_batch(input_path, output_path, models, tokenizer, verb_candidates,
              asc_definitions, device, max_length):
    """Batch mode: read CSV, classify each row, write results."""
    from tqdm import tqdm
    rows = list(csv.DictReader(open(input_path, encoding="utf-8")))
    results = []
    for r in tqdm(rows, desc="Classifying"):
        sentence = r.get("sentence", "")
        if not sentence:
            continue
        result = classify_sentence(sentence, models, tokenizer, verb_candidates,
                                    asc_definitions, device, max_length)
        results.append({
            "sentence": result["sentence"],
            "verb_lemma": result["verb_lemma"],
            "predicted_situation": result["predicted_situation"],
            "score": result["score"],
            "candidate_count": result["candidate_count"],
            "all_scores_json": json.dumps(result["all_scores"]),
        })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    log.info("Wrote %d results to %s", len(results), output_path)


def main():
    parser = argparse.ArgumentParser(description="ASC inference pipeline")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR,
                        help=f"Directory with verb_candidates.json + asc_definitions.json "
                             f"(default: {DEFAULT_DATA_DIR})")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR,
                        help=f"Directory with checkpoints/ + cv_summary.json "
                             f"(default: {DEFAULT_RESULTS_DIR})")
    parser.add_argument("--sentence", type=str, default=None,
                        help="Single sentence to classify")
    parser.add_argument("--input-file", type=Path, default=None,
                        help="CSV file with 'sentence' column for batch mode")
    parser.add_argument("--output-file", type=Path, default=None,
                        help="Output CSV for batch mode")
    parser.add_argument("--fold", type=int, default=None,
                        help="Use specific fold checkpoint (default: best)")
    parser.add_argument("--ensemble", action="store_true",
                        help="Average scores across all 5 folds")
    parser.add_argument("--max-length", type=int, default=384)
    args = parser.parse_args()

    device = get_device()
    models, tokenizer, verb_candidates, asc_definitions = load_pipeline(
        args.data_dir, args.results_dir, args.fold, args.ensemble, device
    )

    if args.sentence:
        result = classify_sentence(args.sentence, models, tokenizer,
                                    verb_candidates, asc_definitions, device, args.max_length)
        print(f"\nInput:  \"{result['sentence']}\"")
        print(f"Verb:   {result['verb_lemma']}")
        print(f"Result: {result['predicted_situation']} (score={result['score']:.4f})")
        print(f"\nAll candidates ({result['candidate_count']}):")
        for sit, s in sorted(result["all_scores"].items(), key=lambda x: -x[1]):
            marker = " ←" if sit == result["predicted_situation"] else ""
            print(f"  {sit}: {s:.4f}{marker}")

    elif args.input_file:
        out = args.output_file or args.input_file.with_suffix(".results.csv")
        run_batch(args.input_file, out, models, tokenizer, verb_candidates,
                  asc_definitions, device, args.max_length)

    else:
        run_interactive(models, tokenizer, verb_candidates, asc_definitions,
                        device, args.max_length)


if __name__ == "__main__":
    main()
