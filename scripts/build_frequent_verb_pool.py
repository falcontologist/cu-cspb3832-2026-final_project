"""Build a top-5000 frequent English verb pool and audit the workbook against it.

Hybrid POS filter (a lemma enters the pool if any one source confirms it as
a verb at meaningful rates):

  1. Local VerbNet 3.4 membership (canonical)
  2. WordNet primary-POS rule: verb synsets are >= 30% of all synsets for the
     lemma. Catches verbs like 'do', 'help', 'include', 'become' that Brown's
     strict threshold drops; rejects 'up', 'still', 'right' whose verb senses
     are minor.
  3. Brown corpus verb-tagged hits >= 3 (loosened from 10)

This grows the verb pool beyond Brown-only's ~1,400 confirmed-verb cap so we
can audit at the top-5000 cutoff.

Outputs:
  data/top_5000_verbs.csv       — rank, lemma, zipf_freq, evidence, in_workbook
  results/top_5000_coverage.md  — coverage report + actionable "verbs to add
                                  to reach 80%" list
"""

import argparse
import csv
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import nltk
from nltk.corpus import brown, wordnet as wn
from nltk.stem import WordNetLemmatizer
from wordfreq import top_n_list, zipf_frequency

# --- Settings ---
WORDFREQ_TOP_N      = 100_000   # surface forms to consult from wordfreq
MIN_BROWN_VERB_HITS = 3         # loosened threshold for Brown-only confirmation
MIN_WN_VERB_SHARE   = 0.30      # WordNet primary-POS threshold
TARGET_POOL_SIZE    = 5_000     # top-N verbs to keep
COVERAGE_TARGET_PCT = 80.0      # the 80% goal

REPO        = Path(__file__).resolve().parents[1]
DEFAULT_CSV = REPO / "data" / "situation_shapes_workbook.csv"
DEFAULT_VN  = Path("/Users/joshfalconer/Documents/Linguistic data/verbnet/verbnet3.4")
DEFAULT_OUT_CSV = REPO / "data" / "top_5000_verbs.csv"
DEFAULT_OUT_MD  = REPO / "results" / "top_5000_coverage.md"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--csv", type=Path, default=DEFAULT_CSV,
                    help=f"Workbook to audit (default: {DEFAULT_CSV.name})")
parser.add_argument("--verb-col", default="Verb",
                    help="Verb column name in the workbook (default: 'Verb')")
parser.add_argument("--vn-dir", type=Path, default=DEFAULT_VN,
                    help=f"Local VerbNet 3.4 XML directory (default: {DEFAULT_VN})")
parser.add_argument("--out-csv", type=Path, default=DEFAULT_OUT_CSV,
                    help=f"Pool CSV output (default: {DEFAULT_OUT_CSV})")
parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD,
                    help=f"Report Markdown output (default: {DEFAULT_OUT_MD})")
args = parser.parse_args()


def norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s)


# --- Ensure NLTK data ---
for resource, path in [
    ("wordnet",  "corpora/wordnet"),
    ("omw-1.4",  "corpora/omw-1.4"),
    ("brown",    "corpora/brown"),
]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource, quiet=True)

# Modal/auxiliary blacklist. These get Brown VB tags in some edge cases or
# WordNet noun-but-also-verb senses, but they are never the head predicate of
# a verbal clause construction.
MODAL_AUX_BLACKLIST = {
    "will", "would", "shall", "should", "may", "might", "must", "can",
    "could", "ought", "ai", "wo", "sha", "ca",
}


# --- 1. Load workbook verbs (NFKC-normalized) ---
mapped: set[str] = set()
with open(args.csv) as f:
    for row in csv.DictReader(f):
        v = norm((row.get(args.verb_col) or "").strip().lower())
        if v:
            mapped.add(v)
print(f"Workbook verbs: {len(mapped):,}")


# --- 2. Build POS-evidence sources ---
# A) VerbNet 3.4 membership
vn_lemmas: set[str] = set()
for xml_file in args.vn_dir.glob("*.xml"):
    try:
        tree = ET.parse(xml_file)
    except ET.ParseError:
        continue
    for member in tree.getroot().iter("MEMBER"):
        name = norm((member.get("name") or "").strip().lower())
        if name and "_" not in name:  # exclude multi-word verbs
            vn_lemmas.add(name)
print(f"VerbNet 3.4 single-word lemmas: {len(vn_lemmas):,}")

# B) Brown verb-tagged counts (native tagset, VB* only — excludes MD modals)
lem = WordNetLemmatizer()
brown_counts: Counter[str] = Counter()
for word, tag in brown.tagged_words():
    # Native Brown verb tags begin with "VB" (VB, VBD, VBG, VBN, VBP, VBZ).
    # Modal "MD", noun "NN*", etc. are excluded.
    if not tag.startswith("VB"):
        continue
    if not word.isalpha():
        continue
    brown_counts[lem.lemmatize(word.lower(), pos="v")] += 1
print(f"Brown VB*-tagged unique lemmas: {len(brown_counts):,}")

# C) WordNet primary-POS — computed lazily inside the filter


def is_verb(lemma: str) -> list[str]:
    """Return list of POS-evidence sources that confirm the lemma as a verb,
    or [] if the lemma should not enter the pool. Modals/auxiliaries are
    excluded outright since they are never the head predicate."""
    if lemma in MODAL_AUX_BLACKLIST:
        return []
    evidence: list[str] = []
    if lemma in vn_lemmas:
        evidence.append("verbnet")
    if brown_counts.get(lemma, 0) >= MIN_BROWN_VERB_HITS:
        evidence.append("brown")
    syns = wn.synsets(lemma)
    if syns:
        verb_count = sum(1 for s in syns if s.pos() == "v")
        if verb_count and verb_count / len(syns) >= MIN_WN_VERB_SHARE:
            evidence.append("wn-primary")
    return evidence


# --- 3. Build frequency-ranked verb pool ---
seen: set[str] = set()
ranked: list[tuple[str, float, list[str]]] = []
for word in top_n_list("en", WORDFREQ_TOP_N, wordlist="best"):
    if not word.isalpha():
        continue
    lemma = norm(lem.lemmatize(word.lower(), pos="v"))
    if lemma in seen:
        continue
    evidence = is_verb(lemma)
    if not evidence:
        continue
    seen.add(lemma)
    ranked.append((lemma, zipf_frequency(lemma, "en"), evidence))
print(f"Verb pool built: {len(ranked):,} lemmas (target was top {TARGET_POOL_SIZE:,})")

pool = ranked[:TARGET_POOL_SIZE]
pool_size = len(pool)


# --- 4. Coverage analysis ---
covered_in_pool = [(rank + 1, l, f, ev) for rank, (l, f, ev) in enumerate(pool)
                   if l in mapped]
missing_in_pool = [(rank + 1, l, f, ev) for rank, (l, f, ev) in enumerate(pool)
                   if l not in mapped]
covered_n = len(covered_in_pool)
coverage_pct = 100 * covered_n / pool_size if pool_size else 0.0

cutoffs = [50, 100, 250, 500, 1000, 2500, 5000]
cutoffs = [c for c in cutoffs if c <= pool_size]
coverage_at_cutoff = []
for c in cutoffs:
    in_top_c = sum(1 for r, *_ in covered_in_pool if r <= c)
    coverage_at_cutoff.append((c, in_top_c, 100 * in_top_c / c))


# --- 5. Gap to 80%: how many verbs need to be added, and which? ---
target_n = int(COVERAGE_TARGET_PCT / 100 * pool_size)
needed_to_add = max(0, target_n - covered_n)
# The first `needed_to_add` highest-frequency missing verbs are the ones to add.
prioritized_adds = missing_in_pool[:needed_to_add]


# --- 6. Write the pool CSV ---
args.out_csv.parent.mkdir(parents=True, exist_ok=True)
with open(args.out_csv, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["rank", "lemma", "zipf_freq", "evidence", "in_workbook"])
    for rank, (lemma, freq, ev) in enumerate(pool, start=1):
        w.writerow([rank, lemma, f"{freq:.3f}", "+".join(ev),
                    "yes" if lemma in mapped else "no"])
print(f"Wrote {args.out_csv}")


# --- 7. Write the Markdown report ---
args.out_md.parent.mkdir(parents=True, exist_ok=True)
with open(args.out_md, "w") as f:
    f.write("# Top-5,000 Frequent English Verb Coverage\n\n")
    f.write(
        "How well does the v2.0 lexicon "
        "([data/situation_shapes_workbook.csv](../data/situation_shapes_workbook.csv)) "
        f"cover the top {pool_size:,} most-frequent English verbs?\n\n"
    )
    f.write("## Method\n\n")
    f.write(
        "The verb pool is built with a hybrid POS filter so the ranking is "
        "not capped by any single corpus. A lemma enters the pool if any one "
        "of these sources confirms it as a verb:\n\n"
        "1. **VerbNet 3.4 membership.** Authoritative — VerbNet only lists verbs.\n"
        f"2. **WordNet primary-POS rule.** verb synsets are at least "
        f"{int(MIN_WN_VERB_SHARE * 100)}% of all synsets for the lemma. Catches "
        "verbs like `do`, `keep`, `help`, `become` that Brown's strict threshold "
        "drops; rejects `up`, `still`, `right` whose verb senses are minor.\n"
        f"3. **Brown corpus** verb-tagged hits >= {MIN_BROWN_VERB_HITS} "
        "(loosened from the previous threshold of 10).\n\n"
        "Lemmas are ranked by `wordfreq` Zipf frequency (a meta-corpus combining "
        "Wikipedia, OpenSubtitles, Twitter, news, books). NFKC normalization is "
        "applied throughout.\n\n"
    )

    f.write(f"**Workbook size:** {len(mapped):,} unique verbs.\n\n")
    f.write(f"**Verb pool built (raw):** {len(ranked):,} lemmas\n")
    f.write(f"**Top-{pool_size:,} pool used for coverage:** {pool_size:,} lemmas\n\n")

    f.write("## Coverage at cutoffs\n\n")
    f.write("| Top-N most frequent | Covered by workbook | Coverage |\n|---:|---:|---:|\n")
    for c, n, pct in coverage_at_cutoff:
        f.write(f"| {c:,} | {n:,} | {pct:.1f}% |\n")
    f.write("\n")

    f.write(f"## Gap to {COVERAGE_TARGET_PCT:.0f}% coverage at top-{pool_size:,}\n\n")
    f.write(f"- **Current coverage:** {covered_n:,} / {pool_size:,} = "
            f"**{coverage_pct:.1f}%**\n")
    f.write(f"- **Target ({COVERAGE_TARGET_PCT:.0f}%):** "
            f"{target_n:,} / {pool_size:,}\n")
    if needed_to_add == 0:
        f.write(f"- **Verbs to add:** 0 — already at or above target.\n\n")
    else:
        f.write(f"- **Verbs to add:** {needed_to_add:,} "
                f"({100 * needed_to_add / pool_size:.1f}% of the pool)\n\n")
        f.write(
            f"Adding the **{needed_to_add:,} highest-frequency missing verbs** "
            "below would lift coverage to the 80% threshold. They are sorted "
            "by frequency-rank in the pool (most frequent first).\n\n"
        )

    if prioritized_adds:
        f.write("## Prioritized verbs to add (top of the gap)\n\n")
        f.write("| Pool rank | Verb | Zipf freq | Evidence |\n|---:|---|---:|---|\n")
        for rank, lemma, freq, ev in prioritized_adds[:200]:
            f.write(f"| {rank:,} | {lemma} | {freq:.2f} | {'+'.join(ev)} |\n")
        if len(prioritized_adds) > 200:
            f.write(f"\n_(Showing top 200 of {len(prioritized_adds):,} verbs to add. "
                    "Full list in `data/top_5000_verbs.csv` — filter `in_workbook=no` "
                    f"and take the top {needed_to_add:,} by rank.)_\n\n")
        else:
            f.write("\n")

    # Top 50 missing verbs regardless of how many are needed to hit 80%
    f.write("## Top 50 missing verbs (highest frequency, absent from workbook)\n\n")
    f.write("These are the highest-frequency verbs in the top-5,000 pool that are "
            "not in the workbook. They are the most-leveraged additions per row, "
            "even if you decide to stop short of the 80% target.\n\n")
    f.write("| Pool rank | Verb | Zipf freq | Evidence |\n|---:|---|---:|---|\n")
    for rank, lemma, freq, ev in missing_in_pool[:50]:
        f.write(f"| {rank:,} | {lemma} | {freq:.2f} | {'+'.join(ev)} |\n")

print(f"Wrote {args.out_md}")


# --- 8. Console summary ---
print()
print(f"Pool size:                {pool_size:,}")
print(f"Workbook size:            {len(mapped):,}")
print()
print("Coverage at cutoffs:")
for c, n, pct in coverage_at_cutoff:
    print(f"  top-{c:>5,}: {n:>5,} / {c:,}  ({pct:5.1f}%)")
print()
print(f"Top-{pool_size:,} coverage: {covered_n:,} / {pool_size:,} = {coverage_pct:.1f}%")
print(f"To hit {COVERAGE_TARGET_PCT:.0f}%: add {needed_to_add:,} more verbs "
      f"(target {target_n:,})")
if prioritized_adds:
    print(f"\nFirst 10 verbs to add (highest frequency):")
    for rank, lemma, freq, ev in prioritized_adds[:10]:
        print(f"  rank={rank:>5,}  zipf={freq:.2f}  evidence={'+'.join(ev):<25}  {lemma}")
