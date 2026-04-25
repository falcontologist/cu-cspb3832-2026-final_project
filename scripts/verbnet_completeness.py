"""VerbNet completeness check for the verb-to-construction workbook.

Compares the workbook's verb-class assignments against NLTK's VerbNet 3.x to
identify:
- VerbNet classes absent from the workbook
- VerbNet verbs absent from the workbook (per class and overall)
- Workbook classes/verbs that don't exist in NLTK VerbNet (data hygiene check)

Usage:
    python verbnet_completeness.py [--csv PATH] [--verb-col COL] [--class-col COL] [--out PATH]

Defaults to auditing the Situation Shapes Workbook in ~/Downloads.
"""

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import nltk
from nltk.corpus import verbnet

# --- Settings ---
REPO        = Path(__file__).resolve().parents[1]
DEFAULT_CSV = Path("/Users/joshfalconer/Downloads/"
                   "Situation Shapes Workbook - VN Verb Mappings.csv")
DEFAULT_OUT = REPO / "results" / "verbnet_completeness.md"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--csv", type=Path, default=DEFAULT_CSV,
                    help=f"Workbook CSV (default: {DEFAULT_CSV})")
parser.add_argument("--verb-col", default="verb",
                    help="Verb column name (default: 'verb')")
parser.add_argument("--class-col", default="verbnet_class",
                    help="VerbNet class column name (default: 'verbnet_class')")
parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help=f"Output Markdown report (default: {DEFAULT_OUT})")
args = parser.parse_args()

# --- Ensure VerbNet is downloaded ---
try:
    nltk.data.find("corpora/verbnet")
except LookupError:
    nltk.download("verbnet", quiet=True)


def top_level(class_id: str) -> str:
    """Reduce a VerbNet class ID to its top-level form.

    'leave-51.2'    -> 'leave-51.2'
    'leave-51.2-1'  -> 'leave-51.2'
    """
    parts = class_id.split("-")
    if len(parts) >= 2:
        return f"{parts[0]}-{parts[1]}"
    return class_id


# --- 1. Load workbook ---
workbook_class_to_verbs: dict[str, set[str]] = defaultdict(set)
all_workbook_verbs: set[str] = set()
with open(args.csv) as f:
    for row in csv.DictReader(f):
        v = (row.get(args.verb_col) or "").strip().lower()
        c = (row.get(args.class_col) or "").strip()
        if v and c:
            workbook_class_to_verbs[c].add(v)
            all_workbook_verbs.add(v)
workbook_classes = set(workbook_class_to_verbs.keys())

# --- 2. Load NLTK VerbNet, aggregating subclass lemmas under top-level keys ---
nltk_class_to_verbs: dict[str, set[str]] = defaultdict(set)
for class_id in verbnet.classids():
    top = top_level(class_id)
    for lemma in verbnet.lemmas(class_id):
        nltk_class_to_verbs[top].add(lemma.lower())
nltk_top_classes = set(nltk_class_to_verbs.keys())
all_nltk_verbs: set[str] = set()
for verbs in nltk_class_to_verbs.values():
    all_nltk_verbs.update(verbs)

# --- 3. Class-level analysis ---
classes_in_both          = workbook_classes & nltk_top_classes
classes_missing_workbook = nltk_top_classes - workbook_classes
classes_extra_workbook   = workbook_classes - nltk_top_classes

# --- 4. Verb-level analysis (across all classes) ---
verbs_in_both          = all_nltk_verbs & all_workbook_verbs
verbs_missing_workbook = all_nltk_verbs - all_workbook_verbs
verbs_extra_workbook   = all_workbook_verbs - all_nltk_verbs

# --- 5. Per-class verb coverage ---
per_class = []
for cls in sorted(classes_in_both):
    nltk_verbs = nltk_class_to_verbs[cls]
    wb_verbs   = workbook_class_to_verbs[cls]
    covered    = nltk_verbs & wb_verbs
    missing    = nltk_verbs - wb_verbs
    extra      = wb_verbs - nltk_verbs
    pct        = 100 * len(covered) / max(len(nltk_verbs), 1)
    per_class.append({
        "class": cls,
        "nltk_n": len(nltk_verbs),
        "covered": len(covered),
        "missing": sorted(missing),
        "extra":   sorted(extra),
        "pct": pct,
    })
# Worst-covered classes first
per_class.sort(key=lambda r: (r["pct"], -r["nltk_n"]))

# --- 6. Write report ---
args.out.parent.mkdir(parents=True, exist_ok=True)
with open(args.out, "w") as f:
    f.write("# VerbNet Completeness Audit\n\n")
    f.write(f"Workbook: `{args.csv.name}`  \n")
    f.write("Reference: NLTK VerbNet 3.x.\n\n")
    f.write("## Summary\n\n")
    f.write("### Class-level coverage\n\n")
    f.write(f"- NLTK VerbNet top-level classes: **{len(nltk_top_classes):,}**\n")
    f.write(f"- Workbook VN classes: **{len(workbook_classes):,}**\n")
    f.write(f"- Classes covered in both: **{len(classes_in_both):,}** "
            f"({100 * len(classes_in_both) / max(len(nltk_top_classes), 1):.1f}% of NLTK)\n")
    f.write(f"- Classes in NLTK but missing from workbook: **{len(classes_missing_workbook):,}**\n")
    f.write(f"- Classes in workbook but not in NLTK: **{len(classes_extra_workbook):,}**\n\n")
    f.write("### Verb-level coverage\n\n")
    f.write(f"- NLTK VerbNet verbs (across all classes): **{len(all_nltk_verbs):,}**\n")
    f.write(f"- Workbook verbs: **{len(all_workbook_verbs):,}**\n")
    f.write(f"- VerbNet verbs covered: **{len(verbs_in_both):,}** "
            f"({100 * len(verbs_in_both) / max(len(all_nltk_verbs), 1):.1f}% of VerbNet)\n")
    f.write(f"- VerbNet verbs missing from workbook: **{len(verbs_missing_workbook):,}**\n")
    f.write(f"- Workbook verbs not in any NLTK VerbNet class: **{len(verbs_extra_workbook):,}** "
            "(possibly added from other sources, paraphrases, or typos)\n\n")

    if classes_missing_workbook:
        f.write("## Classes in NLTK VerbNet but missing from the workbook\n\n")
        for cls in sorted(classes_missing_workbook):
            verbs = sorted(nltk_class_to_verbs[cls])
            sample = ", ".join(verbs[:10])
            if len(verbs) > 10:
                sample += f" ... ({len(verbs)} total)"
            f.write(f"- **{cls}** ({len(verbs)} verbs): {sample}\n")
        f.write("\n")

    if classes_extra_workbook:
        f.write("## Classes in the workbook but not in NLTK VerbNet\n\n")
        f.write("(Possible typos, deprecated class IDs, or custom extensions.)\n\n")
        for cls in sorted(classes_extra_workbook):
            wb_verbs = sorted(workbook_class_to_verbs[cls])
            sample = ", ".join(wb_verbs[:10])
            if len(wb_verbs) > 10:
                sample += f" ... ({len(wb_verbs)} total)"
            f.write(f"- **{cls}** ({len(wb_verbs)} verbs): {sample}\n")
        f.write("\n")

    # Per-class verb-coverage table (only classes with at least one missing verb)
    incomplete_classes = [r for r in per_class if r["missing"]]
    f.write("## Per-class verb coverage (classes with missing verbs)\n\n")
    f.write("Sorted worst-covered first. Classes with all NLTK verbs already in the workbook are omitted.\n\n")
    f.write("| VN Class | NLTK verbs | Covered | Missing | Coverage |\n|---|---:|---:|---:|---:|\n")
    for r in incomplete_classes:
        f.write(f"| {r['class']} | {r['nltk_n']} | {r['covered']} | "
                f"{len(r['missing'])} | {r['pct']:.0f}% |\n")
    f.write(f"\n({len(incomplete_classes)} classes have at least one missing verb; "
            f"{len(classes_in_both) - len(incomplete_classes)} are fully covered.)\n\n")

    f.write("## Missing VerbNet verbs by class (full lists)\n\n")
    for r in incomplete_classes:
        f.write(f"### {r['class']} — {r['covered']}/{r['nltk_n']} ({r['pct']:.0f}%)\n\n")
        f.write(", ".join(f"`{v}`" for v in r["missing"]))
        f.write("\n\n")

    if verbs_extra_workbook:
        f.write(f"## Workbook verbs not in any NLTK VerbNet class ({len(verbs_extra_workbook)})\n\n")
        f.write("These verbs appear in the workbook but NLTK VerbNet has no entry for them. "
                "Likely added from other lexical sources (FrameNet, Croft/Kalm), or possibly typos.\n\n")
        f.write("```\n")
        for v in sorted(verbs_extra_workbook):
            f.write(f"{v}\n")
        f.write("```\n")

# --- 7. Console summary ---
print(f"Wrote {args.out}")
print()
print(f"NLTK VerbNet top-level classes: {len(nltk_top_classes)}")
print(f"Workbook classes:               {len(workbook_classes)}")
print(f"  in both:       {len(classes_in_both)}")
print(f"  missing in WB: {len(classes_missing_workbook)}")
print(f"  extra in WB:   {len(classes_extra_workbook)}")
print()
print(f"NLTK VerbNet verbs:     {len(all_nltk_verbs):,}")
print(f"Workbook verbs:         {len(all_workbook_verbs):,}")
print(f"  VerbNet covered:      {len(verbs_in_both):,} "
      f"({100 * len(verbs_in_both) / max(len(all_nltk_verbs), 1):.1f}% of VerbNet)")
print(f"  VerbNet missing:      {len(verbs_missing_workbook):,}")
print(f"  WB verbs not in VN:   {len(verbs_extra_workbook):,}")
