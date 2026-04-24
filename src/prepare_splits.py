#!/usr/bin/env python3
"""Script 1: Data loading, pair construction, verb→candidate lookup, and 5-fold CV splits."""

import argparse
import csv
import json
import logging
import os
import random
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.model_selection import StratifiedKFold

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent                   # src/
PROJECT_ROOT = HERE.parent                               # repo root
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_DOCS_DIR = PROJECT_ROOT / "docs"


def seed_everything(seed: int):
    random.seed(seed)
    np.random.seed(seed)


def load_csvs(directory: Path, label: int, file_suffix: str) -> list[dict]:
    rows = []
    for p in sorted(directory.glob(f"*{file_suffix}")):
        sit = p.stem.replace(file_suffix.replace(".csv", ""), "")
        for r in csv.DictReader(open(p, encoding="utf-8")):
            r["_file_situation"] = sit
            r["label"] = label
            rows.append(r)
    return rows


def extract_definitions(scope_map_path: Path, out_path: Path) -> dict:
    """Extract ASC definitions from scope map or load existing file."""
    if out_path.exists():
        log.info("Loading existing definitions from %s", out_path)
        return json.load(open(out_path))

    import re
    text = open(scope_map_path, encoding="utf-8").read()
    pattern = re.compile(
        r"### (?P<name>.+?) \(\d+ ex.*?\)\n(?P<body>.*?)(?=\n### |\n---|\n## )",
        re.DOTALL,
    )
    defs = {}
    for m in pattern.finditer(text):
        name = m.group("name").strip()
        body = m.group("body")
        evt = re.search(r"\*\*(?:Event type|IN)\*\*:\s*(.+?)(?:\n|$)", body)
        subj = re.search(r"\*\*Subject role\*\*:\s*(.+?)(?:\n|$)", body)
        if evt:
            event_type = evt.group(1).strip().rstrip(".")  + "."
            subject = subj.group(1).strip().rstrip(".") if subj else ""
            definition = event_type
            if subject:
                definition += f" The grammatical subject is the {subject.lower()}."
            defs[name] = definition

    with open(out_path, "w") as f:
        json.dump(defs, f, indent=2)
    log.info("Extracted %d definitions → %s", len(defs), out_path)
    return defs


def load_tier_labels(path: Path) -> dict:
    """Load tier_labels.json and build a lookup: (situation, sentence, verb_lemma) → (tier, source)."""
    data = json.load(open(path))
    lookup = {}
    for sit, tiers in data.items():
        for tier_name, rows in tiers.items():
            for r in rows:
                key = (sit, r["sentence"], r["verb_lemma"])
                lookup[key] = (tier_name, r.get("source", "mechanical"))
    return lookup


def build_verb_candidates(pos_rows: list[dict], out_path: Path) -> dict:
    """Build verb_lemma → set of Situations from pos rows."""
    vmap = defaultdict(set)
    for r in pos_rows:
        vmap[r["verb_lemma"]].add(r["_file_situation"])
    result = {v: sorted(slist) for v, slist in vmap.items()}
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    log.info("Verb candidates: %d verbs → %s", len(result), out_path)

    sizes = [len(v) for v in result.values()]
    size_dist = Counter(sizes)
    log.info("  Average candidate set size: %.2f", np.mean(sizes))
    log.info("  Candidate set size distribution:")
    for sz in sorted(size_dist):
        log.info("    %d candidates: %d verbs", sz, size_dist[sz])
    return result


def build_cluster_map() -> dict:
    """Three-realm cluster taxonomy for computing neg-row difficulty tiers."""
    C = {
        "Motion":("Physical","Motion"),"Vehicular_Motion":("Physical","Motion"),
        "Carrying":("Physical","Motion"),"Sending":("Physical","Motion"),
        "Pick_Up_and_Drop_Off":("Physical","Motion"),"Location":("Physical","Motion"),
        "Throwing":("Physical","Motion"),"Pursuit":("Physical","Motion"),
        "Change_of_State":("Physical","Change_of_State"),
        "Cause_Change_of_State":("Physical","Change_of_State"),
        "Hurt":("Physical","Change_of_State"),
        "Contact":("Physical","Force"),"Manipulation":("Physical","Force"),
        "Constrain":("Physical","Force"),"Capacity":("Physical","Force"),
        "Incremental":("Physical","Incremental"),"Cause_Incremental":("Physical","Incremental"),
        "Concealment":("Physical","Incremental"),
        "Ingestion":("Physical","Ingestion"),"Feeding":("Physical","Ingestion"),
        "Cause_Creation":("Physical","Creation"),"Image_Creation":("Physical","Creation"),
        "Form":("Physical","Creation"),"Emission":("Physical","Creation"),
        "Existence":("Physical","Existence"),
        "Perception_(exp._subj.)":("Mental","Perception"),
        "Perception_(stim._subj.)":("Mental","Perception"),
        "Emotion_(exp. subj.)":("Mental","Emotion"),
        "Emotion_(stim. subj.)":("Mental","Emotion"),
        "Desire":("Mental","Intention"),"Intention":("Mental","Intention"),
        "Learning":("Mental","Cognition"),"Discovery":("Mental","Cognition"),
        "Evaluation":("Mental","Evaluation"),"Counting":("Mental","Evaluation"),
        "Measurement":("Mental","Evaluation"),
        "Cause_and_Effect":("Mental","Causation"),
        "Possession":("Social","Possession"),"Dynamic_Possession":("Social","Possession"),
        "Transfer_of_Possession":("Social","Possession"),"Buying":("Social","Possession"),
        "Selling":("Social","Possession"),"Payment":("Social","Possession"),
        "Future_Having":("Social","Possession"),"Charge":("Social","Possession"),
        "Communicate":("Social","Communication"),"Statement":("Social","Communication"),
        "Joint_Statement":("Social","Communication"),"Request":("Social","Communication"),
        "Response":("Social","Communication"),
        "Membership":("Social","Affiliation"),"Cause_Membership":("Social","Affiliation"),
        "Participation":("Social","Affiliation"),"Cause_Participation":("Social","Affiliation"),
        "Collective":("Social","Affiliation"),
        "Enforcement":("Social","Control"),"Limitation":("Social","Control"),
        "Induction":("Social","Control"),
        "Aggression":("Social","Aggression"),"Protection":("Social","Aggression"),
        "Reciprocal":("Social","Reciprocal"),"Replacement":("Social","Reciprocal"),
    }
    return C


def norm_sit(s: str) -> str:
    """Normalize Situation names: spaces→underscores, fix Emotion naming."""
    s = s.replace(" ", "_")
    for kind in ("exp.", "stim."):
        s = s.replace(f"Emotion_({kind}_subj.)", f"Emotion_({kind} subj.)")
    return s


def neg_tier(target: str, donor: str, cluster_map: dict) -> str:
    """Compute difficulty tier for a neg row: T1=same cluster, T2=same realm, T3=diff realm."""
    t_norm = norm_sit(target)
    d_norm = norm_sit(donor)
    if t_norm not in cluster_map or d_norm not in cluster_map:
        return ""
    tr, tc = cluster_map[t_norm]
    dr, dc = cluster_map[d_norm]
    if dc == tc:
        return "T1"
    if dr == tr:
        return "T2"
    return "T3"


def construct_pairs(
    pos_rows: list[dict],
    neg_rows: list[dict],
    definitions: dict,
    tier_lookup: dict,
) -> list[dict]:
    """Build cross-encoder pairs with tier metadata.

    Pos rows: tier/source from tier_labels.json (boundary-adjacent vs prototypical vs peripheral).
    Neg rows: tier computed from donor-vs-target cluster relationship (T1 hard / T2 medium / T3 easy).
    """
    pairs = []
    missing_defs = set()
    cluster_map = build_cluster_map()

    for r in pos_rows:
        sit = r["_file_situation"]
        if sit not in definitions:
            missing_defs.add(sit)
            continue
        tier_key = (sit, r["sentence"], r.get("verb_lemma", ""))
        tier_info = tier_lookup.get(tier_key, ("", ""))
        pairs.append({
            "sentence": r["sentence"],
            "asc_definition": definitions[sit],
            "label": 1,
            "target_situation": sit,
            "donor_situation": sit,
            "tier": tier_info[0],
            "source": tier_info[1],
            "match_path": r.get("match_path", ""),
            "verb_lemma": r.get("verb_lemma", ""),
        })

    for r in neg_rows:
        target = r["_file_situation"]
        donor = r.get("situation", "")
        if target not in definitions:
            missing_defs.add(target)
            continue
        computed_tier = neg_tier(target, donor, cluster_map)
        pairs.append({
            "sentence": r["sentence"],
            "asc_definition": definitions[target],
            "label": 0,
            "target_situation": target,
            "donor_situation": donor,
            "tier": computed_tier,
            "source": "",
            "match_path": r.get("match_path", ""),
            "verb_lemma": r.get("verb_lemma", ""),
        })

    if missing_defs:
        log.warning("Missing definitions for: %s", missing_defs)

    return pairs


def sanity_check_pairs(pairs: list[dict]):
    """Verify no sentence is both pos and neg for the SAME target_situation."""
    by_target = defaultdict(lambda: {"pos": set(), "neg": set()})
    for p in pairs:
        key = (p["sentence"], p["verb_lemma"])
        if p["label"] == 1:
            by_target[p["target_situation"]]["pos"].add(key)
        else:
            by_target[p["target_situation"]]["neg"].add(key)

    violations = 0
    for sit, sets in by_target.items():
        overlap = sets["pos"] & sets["neg"]
        if overlap:
            violations += len(overlap)
            log.error("CONTAMINATION in %s: %d sentences are both pos and neg", sit, len(overlap))
    if violations == 0:
        log.info("Sanity check PASSED: no sentence is both pos and neg for the same target")
    return violations


def do_splits(
    pairs: list[dict],
    folds_dir: Path,
    n_splits: int,
    seed: int,
):
    """Generate stratified 5-fold CV splits with verb-lemma leakage check."""
    strat_labels = [f"{p['target_situation']}_{p['label']}" for p in pairs]
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    indices = np.arange(len(pairs))

    columns = [
        "sentence", "asc_definition", "label", "target_situation",
        "donor_situation", "tier", "source", "match_path", "verb_lemma",
    ]

    for fold_i, (train_dev_idx, test_idx) in enumerate(skf.split(indices, strat_labels)):
        fold_dir = folds_dir / f"fold_{fold_i}"
        fold_dir.mkdir(parents=True, exist_ok=True)

        test_pairs = [pairs[i] for i in test_idx]
        train_dev_pairs = [pairs[i] for i in train_dev_idx]

        # Verb-lemma leakage check
        train_dev_verbs = {p["verb_lemma"] for p in train_dev_pairs if p["verb_lemma"]}
        test_verbs = {p["verb_lemma"] for p in test_pairs if p["verb_lemma"]}
        leaked = test_verbs - train_dev_verbs
        if leaked:
            log.warning("Fold %d: %d test-only verbs found, swapping: %s",
                        fold_i, len(leaked), list(leaked)[:10])
            # Swap leaked test rows into train, replace with same-situation/tier from train
            leaked_indices = [i for i, p in enumerate(test_pairs)
                              if p["verb_lemma"] in leaked]
            for li in leaked_indices:
                leaked_pair = test_pairs[li]
                # Find a replacement in train_dev with same situation, same label, same tier
                for j, candidate in enumerate(train_dev_pairs):
                    if (candidate["target_situation"] == leaked_pair["target_situation"]
                            and candidate["label"] == leaked_pair["label"]
                            and candidate["tier"] == leaked_pair["tier"]
                            and candidate["verb_lemma"] not in leaked
                            and candidate["verb_lemma"] in train_dev_verbs):
                        # Swap
                        test_pairs[li], train_dev_pairs[j] = train_dev_pairs[j], test_pairs[li]
                        break

        # Split train_dev into train (85%) and dev (15%)
        n_dev = max(1, int(len(train_dev_pairs) * 0.15))
        random.shuffle(train_dev_pairs)

        # Stratified dev split
        td_strat = [f"{p['target_situation']}_{p['label']}" for p in train_dev_pairs]
        unique_strats = sorted(set(td_strat))
        dev_pairs = []
        train_pairs = []
        by_strat = defaultdict(list)
        for i, s in enumerate(td_strat):
            by_strat[s].append(i)
        for s, idxs in by_strat.items():
            n_take = max(1, int(len(idxs) * 0.15))
            random.shuffle(idxs)
            for idx in idxs[:n_take]:
                dev_pairs.append(train_dev_pairs[idx])
            for idx in idxs[n_take:]:
                train_pairs.append(train_dev_pairs[idx])

        # Write CSVs
        for name, data in [("train.csv", train_pairs), ("dev.csv", dev_pairs), ("test.csv", test_pairs)]:
            with open(fold_dir / name, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
                w.writeheader()
                w.writerows(data)

        # Stats
        tier_dist = Counter(p["tier"] for p in train_pairs if p["label"] == 0 and p["tier"])
        log.info(
            "Fold %d: train=%d dev=%d test=%d | neg tier dist T1=%d T2=%d T3=%d",
            fold_i, len(train_pairs), len(dev_pairs), len(test_pairs),
            tier_dist.get("T1", 0), tier_dist.get("T2", 0), tier_dist.get("T3", 0),
        )

    log.info("Wrote %d folds to %s", n_splits, folds_dir)


def main():
    parser = argparse.ArgumentParser(description="Prepare cross-encoder training splits")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR,
                        help="Directory holding situation_splits/ and *.json configs "
                             f"(default: {DEFAULT_DATA_DIR})")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    seed_everything(args.seed)
    base = args.data_dir
    pos_dir = base / "situation_splits" / "positives"
    neg_dir = base / "situation_splits" / "negatives"

    # 1a. Load CSVs
    log.info("Loading pos files...")
    pos_rows = load_csvs(pos_dir, label=1, file_suffix="_pos.csv")
    log.info("  %d positive rows", len(pos_rows))

    log.info("Loading neg files...")
    neg_rows = load_csvs(neg_dir, label=0, file_suffix="_neg.csv")
    log.info("  %d negative rows", len(neg_rows))

    # 1b. Definitions
    definitions = extract_definitions(
        DEFAULT_DOCS_DIR / "situation_scope_map_inductive.md",
        base / "asc_definitions.json",
    )
    log.info("  %d ASC definitions", len(definitions))

    # 1c. Construct pairs
    tier_lookup = load_tier_labels(base / "tier_labels.json")
    pairs = construct_pairs(pos_rows, neg_rows, definitions, tier_lookup)
    log.info("Total pairs: %d (pos=%d, neg=%d)",
             len(pairs),
             sum(1 for p in pairs if p["label"] == 1),
             sum(1 for p in pairs if p["label"] == 0))

    # Sanity check
    sanity_check_pairs(pairs)

    # 1e. 5-fold splits
    folds_dir = base / "folds"
    do_splits(pairs, folds_dir, n_splits=5, seed=args.seed)

    # 1f. Verb candidates
    build_verb_candidates(pos_rows, base / "verb_candidates.json")

    log.info("Done.")


if __name__ == "__main__":
    main()
