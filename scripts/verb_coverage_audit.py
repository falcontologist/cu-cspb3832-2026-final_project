"""Audit mappings_final_clean.csv coverage against frequency-ranked English verbs.

Two-corpus methodology:
1. Use the Brown corpus (POS-tagged, ~1M words) to identify lemmas that are
   genuinely used as verbs at meaningful rates. This filters out particles
   and adverbs ("up", "down", "still", "right") that WordNet flags as having
   verb senses but are rarely used that way.
2. Use wordfreq's `best` wordlist (a meta-corpus of Wikipedia, OpenSubtitles,
   Twitter, news, and books) for the broader frequency ranking.

A lemma enters the verb-frequency-ranked pool only if it passes both checks:
- Brown gives it >= MIN_BROWN_VERB_HITS verb-tagged tokens.
- wordfreq returns a non-zero frequency.

Output: results/verb_coverage_audit.md
"""

import csv
from collections import Counter
from pathlib import Path

import nltk
from nltk.corpus import brown, wordnet as wn
from nltk.stem import WordNetLemmatizer
from wordfreq import top_n_list, zipf_frequency

# --- Settings ---
MIN_BROWN_VERB_HITS = 10            # require this many verb-tagged tokens in Brown
WORDFREQ_TOP_N      = 100_000       # surface forms to consult from wordfreq

REPO         = Path(__file__).resolve().parents[1]
MAPPINGS_CSV = REPO / "data" / "mappings_final_clean.csv"
OUT          = REPO / "results" / "verb_coverage_audit.md"

# --- Ensure NLTK data ---
for resource, path in [
    ("wordnet",          "corpora/wordnet"),
    ("omw-1.4",          "corpora/omw-1.4"),
    ("brown",            "corpora/brown"),
    ("universal_tagset", "taggers/universal_tagset"),
]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource, quiet=True)

# --- 1. Load mapped verbs ---
mapped = set()
with open(MAPPINGS_CSV) as f:
    for row in csv.DictReader(f):
        mapped.add(row["Verb"].strip().lower())

# --- 2. Build the Brown verb-frequency table ---
lem = WordNetLemmatizer()
brown_verb_counts = Counter()
for word, tag in brown.tagged_words(tagset="universal"):
    if tag != "VERB":
        continue
    if not word.isalpha():
        continue
    lemma = lem.lemmatize(word.lower(), pos="v")
    brown_verb_counts[lemma] += 1

confirmed_verbs = {v for v, c in brown_verb_counts.items() if c >= MIN_BROWN_VERB_HITS}

# --- 3. Build a frequency-ranked list of confirmed verb lemmas via wordfreq ---
seen = set()
ranked_verbs = []
for word in top_n_list("en", WORDFREQ_TOP_N, wordlist="best"):
    if not word.isalpha():
        continue
    lemma = lem.lemmatize(word.lower(), pos="v")
    if lemma in seen:
        continue
    if lemma not in confirmed_verbs:
        continue
    if not wn.synsets(lemma, pos="v"):
        continue
    seen.add(lemma)
    ranked_verbs.append((lemma, zipf_frequency(lemma, "en")))

# --- 4. Coverage at cutoffs ---
cutoffs_raw = [50, 100, 250, 500, 1000, 1500, 2000, 3000, 5000, len(ranked_verbs)]
cutoffs = []
for n in cutoffs_raw:
    n = min(n, len(ranked_verbs))
    if n not in cutoffs:
        cutoffs.append(n)

rows = []
for n in cutoffs:
    top_n = {v for v, _ in ranked_verbs[:n]}
    covered = top_n & mapped
    rows.append((n, len(covered), 100 * len(covered) / n))

# --- 5. Gap list: top high-frequency verbs absent from the mapping ---
rank_in_pool = {v: i + 1 for i, (v, _) in enumerate(ranked_verbs)}
missing = [(v, f) for v, f in ranked_verbs if v not in mapped][:50]

# --- 6. Brown-only ranking, for cross-check (top 50) ---
brown_top = sorted(brown_verb_counts.items(), key=lambda x: -x[1])
brown_top_50 = [v for v, _ in brown_top[:50]]
brown_top_50_covered = sum(1 for v in brown_top_50 if v in mapped)

# --- 7. Write the report ---
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w") as f:
    f.write("# Verb Coverage Audit\n\n")
    f.write(
        "How well does the hand-curated verb-to-construction lexicon "
        "([data/mappings_final_clean.csv](../data/mappings_final_clean.csv)) "
        "cover the most frequently used English verbs?\n\n"
    )
    f.write("## Method\n\n")
    f.write(
        "1. **Identify genuine verbs.** From the Brown corpus (POS-tagged, "
        "~1M words), keep every lemma with at least "
        f"{MIN_BROWN_VERB_HITS} verb-tagged tokens. This filters out particles "
        "and adverbs that WordNet flags as having minor verb senses but are "
        "rarely used that way (`up`, `out`, `still`, `right`, etc.).\n"
        "2. **Rank by frequency.** Walk the top "
        f"{WORDFREQ_TOP_N:,} most-frequent surface forms in `wordfreq`'s "
        "`best` wordlist (meta-corpus of Wikipedia, OpenSubtitles, Twitter, "
        "news, books). Lemmatize and dedupe; keep only lemmas confirmed as "
        "verbs in step 1.\n"
        "3. **Compare.** Check membership against `mappings_final_clean.csv`.\n\n"
    )
    f.write(f"**Mapping size:** {len(mapped):,} unique verbs.\n\n")
    f.write(f"**Brown-confirmed verb lemmas (>= {MIN_BROWN_VERB_HITS} tagged hits):** "
            f"{len(confirmed_verbs):,}.\n\n")
    f.write(f"**Frequency-ranked verb pool (Brown ∩ wordfreq):** "
            f"{len(ranked_verbs):,} lemmas.\n\n")
    f.write("## Coverage at cutoffs\n\n")
    f.write("| Top-N most frequent | Covered by mapping | Coverage |\n")
    f.write("|---:|---:|---:|\n")
    for n, c, pct in rows:
        f.write(f"| {n:,} | {c:,} | {pct:.1f}% |\n")
    f.write("\n")
    f.write("## Cross-check: Brown-only ranking (top 50)\n\n")
    f.write(
        "If we rank by Brown's POS-tagged verb counts directly (no wordfreq), "
        f"the mapping covers **{brown_top_50_covered}/50 ({100*brown_top_50_covered/50:.0f}%)** "
        "of the 50 most-frequent Brown verbs. Brown is genre-narrow (1961 written "
        "American English), so this is a sanity check, not the headline number.\n\n"
    )
    f.write(
        "## Top high-frequency verbs absent from the mapping\n\n"
        "These are the highest-frequency verbs (by the combined Brown+wordfreq "
        "method above) that are not in `mappings_final_clean.csv`. Adding them "
        "would yield the largest coverage gain per row.\n\n"
    )
    f.write("| Pool rank | Verb | Zipf freq | Brown count |\n|---:|---|---:|---:|\n")
    for v, fr in missing:
        f.write(f"| {rank_in_pool[v]:,} | {v} | {fr:.2f} | {brown_verb_counts[v]:,} |\n")

# --- 8. Console summary ---
print(f"Wrote {OUT}")
print(f"Mapping size: {len(mapped):,} unique verbs")
print(f"Brown-confirmed verb lemmas: {len(confirmed_verbs):,}")
print(f"Frequency-ranked verb pool:  {len(ranked_verbs):,}")
print()
print("Coverage at cutoffs:")
for n, c, pct in rows:
    print(f"  top-{n:>6,}: {c:>5,} / {n:,}  ({pct:5.1f}%)")
print()
print(f"Brown-only top 50: {brown_top_50_covered}/50 covered")
print()
print("Top 10 missing high-frequency verbs (combined ranking):")
for v, fr in missing[:10]:
    print(f"  pool_rank={rank_in_pool[v]:>5,}  zipf={fr:.2f}  brown_n={brown_verb_counts[v]:>4,}  {v}")
