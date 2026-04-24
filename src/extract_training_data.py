#!/usr/bin/env python3
"""
Extract training sentences from OntoNotes 5.0 and map them to Situation ASCs.

Pipeline:
  1. Parse sense inventory XMLs → (lemma, ON_sense) → WN synsets + VN classes
  2. Load mappings CSV → (verb, VN_class) → Situation ASC
  3. Walk .sense files → (file, sentence_idx, token_idx, lemma, ON_sense)
  4. Resolve each to Situation(s) via both VN and WN paths
  5. Extract sentence from .parse file by flattening the tree

Output: CSV with columns:
  sentence, verb_lemma, verb_token_idx, on_sense, wn_synsets, vn_class,
  situation, source_file, sentence_idx

Usage:
  python extract_training_data.py \
    --ontonotes /path/to/ontonotes-release-5.0/data/files/data \
    --mappings /path/to/mappings_final_clean.csv \
    --output training_data.csv
"""

import argparse
import csv
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict


# ── Step 1: Parse sense inventory XMLs ──────────────────────────────────────

def parse_sense_inventories(inventory_dir):
    """
    Build lookup: (lemma, on_sense_number) → {wn_synsets: [...], vn_classes: [...]}

    Only processes verb inventories (*-v.xml).
    WN sense numbers like "1,3" for lemma "ache" become ["ache.v.01", "ache.v.03"].
    """
    lookup = {}
    inventory_path = Path(inventory_dir)

    if not inventory_path.exists():
        print(f"WARNING: Sense inventory directory not found: {inventory_dir}")
        return lookup

    for xml_file in inventory_path.glob("*-v.xml"):
        # Extract lemma from filename: "ache-v.xml" → "ache"
        lemma = xml_file.stem.replace("-v", "")

        try:
            tree = ET.parse(xml_file)
        except ET.ParseError as e:
            print(f"WARNING: Could not parse {xml_file}: {e}")
            continue

        root = tree.getroot()

        for sense_elem in root.findall(".//sense"):
            sense_n = sense_elem.get("n")
            if sense_n is None:
                continue

            # Parse WN synsets
            wn_synsets = []
            wn_elem = sense_elem.find(".//mappings/wn[@version='3.0']")
            if wn_elem is None:
                # Try without version
                wn_elem = sense_elem.find(".//mappings/wn")
            if wn_elem is not None and wn_elem.text and wn_elem.text.strip():
                for num in wn_elem.text.strip().split(","):
                    num = num.strip()
                    if num:
                        # Convert "1" → "ache.v.01"
                        wn_synsets.append(f"{lemma}.v.{int(num):02d}")

            # Parse VN classes
            vn_classes = []
            vn_elem = sense_elem.find(".//mappings/vn")
            if vn_elem is not None and vn_elem.text and vn_elem.text.strip():
                for vn in vn_elem.text.strip().split(","):
                    vn = vn.strip()
                    if vn:
                        vn_classes.append(vn)

            lookup[(lemma, sense_n)] = {
                "wn_synsets": wn_synsets,
                "vn_classes": vn_classes,
            }

    print(f"Loaded {len(lookup)} sense entries from {inventory_path}")
    return lookup


# ── Step 2: Load mappings CSV ───────────────────────────────────────────────

def load_mappings(mappings_path):
    """
    Build two lookups from the mappings CSV:
      vn_lookup: (verb_lemma, vn_class) → [Situation, ...]
      wn_lookup: (verb_lemma, wn_synset) → [(vn_class, Situation), ...]
    """
    vn_lookup = defaultdict(list)
    wn_lookup = defaultdict(list)

    with open(mappings_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            verb = row["Verb"].strip().lower()
            vn_class = row["VerbNet Class"].strip()
            situation = row["Situation"].strip()

            vn_lookup[(verb, vn_class)].append(situation)

            # Map each WN synset column to this situation
            for i in range(1, 11):
                col = f"WN_Synset_{i:02d}"
                if col in row and row[col] and row[col].strip():
                    synset = row[col].strip()
                    wn_lookup[(verb, synset)].append((vn_class, situation))

    print(f"Loaded VN mappings for {len(vn_lookup)} (verb, class) pairs")
    print(f"Loaded WN mappings for {len(wn_lookup)} (verb, synset) pairs")
    return vn_lookup, wn_lookup


# ── Step 3: Parse .sense files ──────────────────────────────────────────────

def parse_sense_file(sense_path):
    """
    Parse a .sense file. Each line:
      filepath sent_idx token_idx lemma-POS [?,?] sense_number

    Returns list of dicts with: sentence_idx, token_idx, lemma, pos, on_sense
    """
    entries = []
    with open(sense_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            # Format: filepath sent_idx token_idx lemma-pos [?,?] sense_num
            # The ?,? field is optional
            if len(parts) < 5:
                continue

            sent_idx = int(parts[1])
            token_idx = int(parts[2])
            lemma_pos = parts[3]

            # Split lemma-pos: "lead-v" → ("lead", "v")
            # Handle cases like "break-v" but also potential edge cases
            pos_match = re.match(r"^(.+)-(v|n|adj|adv)$", lemma_pos)
            if not pos_match:
                continue
            lemma = pos_match.group(1)
            pos = pos_match.group(2)

            # Only process verbs
            if pos != "v":
                continue

            # Sense number is the last field
            on_sense = parts[-1]

            entries.append({
                "sentence_idx": sent_idx,
                "token_idx": token_idx,
                "lemma": lemma,
                "on_sense": on_sense,
            })
    return entries


# ── Step 4: Extract sentence from .parse file ──────────────────────────────

def extract_sentences_from_parse(parse_path):
    """
    Read a .parse file and return a list of (sentence_index, plain_text).
    Sentences are separated by blank lines. Each sentence is a bracketed tree.
    We flatten by extracting terminal nodes, skipping traces/empty categories.
    """
    sentences = []
    current_tree = []

    with open(parse_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped == "":
                if current_tree:
                    tree_str = " ".join(current_tree)
                    text = flatten_tree(tree_str)
                    sentences.append(text)
                    current_tree = []
            else:
                current_tree.append(stripped)

        # Handle last tree if file doesn't end with blank line
        if current_tree:
            tree_str = " ".join(current_tree)
            text = flatten_tree(tree_str)
            sentences.append(text)

    return sentences


def flatten_tree(tree_str):
    """
    Extract terminal words from a Penn Treebank bracketed tree string.
    Skip trace/empty elements: -NONE-, *T*, *PRO*, *-N, *U*, *?*, etc.
    """
    # Find all (POS word) terminal pairs
    terminals = re.findall(r"\(([^\s()]+)\s+([^\s()]+)\)", tree_str)

    words = []
    for pos, word in terminals:
        # Skip empty categories
        if pos == "-NONE-":
            continue
        # Skip trace elements
        if word.startswith("*") or word == "0":
            continue
        words.append(word)

    # Clean up spacing around punctuation
    text = " ".join(words)
    # Remove space before punctuation
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)
    # Handle quotes
    text = text.replace("`` ", '"').replace(" ''", '"')
    text = text.replace("``", '"').replace("''", '"')
    text = text.replace("-LRB-", "(").replace("-RRB-", ")")

    return text


# ── Step 5: Main extraction pipeline ───────────────────────────────────────

def find_annotation_files(data_dir, lang="english"):
    """
    Walk the OntoNotes annotation directory and yield (sense_path, parse_path)
    pairs for each document that has both files.
    """
    annotations_dir = Path(data_dir) / lang / "annotations"
    if not annotations_dir.exists():
        print(f"WARNING: Annotations directory not found: {annotations_dir}")
        return

    count = 0
    for sense_file in annotations_dir.rglob("*.sense"):
        parse_file = sense_file.with_suffix(".parse")
        if parse_file.exists():
            count += 1
            yield str(sense_file), str(parse_file)

    print(f"Found {count} document pairs with .sense + .parse files")


def extract_training_data(data_dir, mappings_path, output_path):
    """Main pipeline: extract sentences and map to Situations."""

    # Step 1: Load sense inventories
    inventory_dir = Path(data_dir) / "english" / "metadata" / "sense-inventories"
    sense_inventory = parse_sense_inventories(inventory_dir)

    # Step 2: Load mappings
    vn_lookup, wn_lookup = load_mappings(mappings_path)

    # Collect all results
    results = []
    matched = 0
    unmatched_verbs = defaultdict(int)
    unmatched_senses = defaultdict(int)

    for sense_path, parse_path in find_annotation_files(data_dir):
        # Parse the sense annotations
        sense_entries = parse_sense_file(sense_path)
        if not sense_entries:
            continue

        # Extract sentences from parse file
        sentences = extract_sentences_from_parse(parse_path)

        for entry in sense_entries:
            sent_idx = entry["sentence_idx"]
            lemma = entry["lemma"]
            on_sense = entry["on_sense"]

            # Get sentence text
            if sent_idx >= len(sentences):
                continue
            sentence_text = sentences[sent_idx]

            # Look up ON sense → WN synsets + VN classes
            inv_key = (lemma, on_sense)
            inv_data = sense_inventory.get(inv_key)

            if inv_data is None:
                unmatched_senses[(lemma, on_sense)] += 1
                continue

            wn_synsets = inv_data["wn_synsets"]
            vn_classes = inv_data["vn_classes"]

            # Try VN path first: (lemma, vn_class) → Situation
            situations_found = []

            for vn_class in vn_classes:
                # VN class in inventory may include subclass: "tingle-40.8.2"
                # Mappings CSV may have just the class name
                vn_key = (lemma, vn_class)
                if vn_key in vn_lookup:
                    for sit in vn_lookup[vn_key]:
                        situations_found.append({
                            "situation": sit,
                            "match_path": "VN",
                            "vn_class": vn_class,
                            "wn_synsets": ";".join(wn_synsets),
                        })

            # Try WN path: (lemma, wn_synset) → Situation
            for synset in wn_synsets:
                wn_key = (lemma, synset)
                if wn_key in wn_lookup:
                    for vn_class, sit in wn_lookup[wn_key]:
                        # Avoid duplicates
                        if not any(
                            s["situation"] == sit and s["vn_class"] == vn_class
                            for s in situations_found
                        ):
                            situations_found.append({
                                "situation": sit,
                                "match_path": "WN",
                                "vn_class": vn_class,
                                "wn_synsets": ";".join(wn_synsets),
                            })

            if not situations_found:
                unmatched_verbs[lemma] += 1
                continue

            matched += 1
            for sit_info in situations_found:
                results.append({
                    "sentence": sentence_text,
                    "verb_lemma": lemma,
                    "verb_token_idx": entry["token_idx"],
                    "on_sense": on_sense,
                    "wn_synsets": sit_info["wn_synsets"],
                    "vn_class": sit_info["vn_class"],
                    "situation": sit_info["situation"],
                    "match_path": sit_info["match_path"],
                    "source_file": os.path.relpath(sense_path),
                    "sentence_idx": sent_idx,
                })

    # Write output
    if results:
        fieldnames = [
            "sentence", "verb_lemma", "verb_token_idx", "on_sense",
            "wn_synsets", "vn_class", "situation", "match_path",
            "source_file", "sentence_idx",
        ]
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    # Report
    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Total verb sense annotations matched to Situations: {matched}")
    print(f"Total training rows written (including multi-Situation): {len(results)}")
    print(f"Unique Situations covered: {len(set(r['situation'] for r in results))}")
    print(f"Unique verbs matched: {len(set(r['verb_lemma'] for r in results))}")
    print(f"\nVerbs with no mapping (top 20):")
    for verb, count in sorted(unmatched_verbs.items(), key=lambda x: -x[1])[:20]:
        print(f"  {verb}: {count} instances")
    print(f"\nSenses with no inventory entry (top 20):")
    for key, count in sorted(unmatched_senses.items(), key=lambda x: -x[1])[:20]:
        print(f"  {key[0]} sense {key[1]}: {count} instances")
    print(f"\nOutput written to: {output_path}")

    # Situation coverage report
    print(f"\n{'='*60}")
    print(f"SITUATION COVERAGE")
    print(f"{'='*60}")
    sit_counts = defaultdict(int)
    for r in results:
        sit_counts[r["situation"]] += 1
    for sit, count in sorted(sit_counts.items(), key=lambda x: -x[1]):
        print(f"  {sit}: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract OntoNotes training sentences mapped to Situation ASCs"
    )
    parser.add_argument(
        "--ontonotes",
        required=True,
        help="Path to OntoNotes data dir (e.g. .../data/files/data)",
    )
    parser.add_argument(
        "--mappings",
        required=True,
        help="Path to mappings_final_clean.csv",
    )
    parser.add_argument(
        "--output",
        default="training_data.csv",
        help="Output CSV path (default: training_data.csv)",
    )
    args = parser.parse_args()

    extract_training_data(args.ontonotes, args.mappings, args.output)