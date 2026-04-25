# Verb Coverage Audit

How well does the hand-curated verb-to-construction lexicon ([data/mappings_final_clean.csv](../data/mappings_final_clean.csv)) cover the most frequently used English verbs?

## Method

1. **Identify genuine verbs.** From the Brown corpus (POS-tagged, ~1M words), keep every lemma with at least 10 verb-tagged tokens. This filters out particles and adverbs that WordNet flags as having minor verb senses but are rarely used that way (`up`, `out`, `still`, `right`, etc.).
2. **Rank by frequency.** Walk the top 100,000 most-frequent surface forms in `wordfreq`'s `best` wordlist (meta-corpus of Wikipedia, OpenSubtitles, Twitter, news, books). Lemmatize and dedupe; keep only lemmas confirmed as verbs in step 1.
3. **Compare.** Check membership against `mappings_final_clean.csv`.

**Mapping size:** 3,258 unique verbs.

**Brown-confirmed verb lemmas (>= 10 tagged hits):** 1,424.

**Frequency-ranked verb pool (Brown ∩ wordfreq):** 1,413 lemmas.

## Coverage at cutoffs

| Top-N most frequent | Covered by mapping | Coverage |
|---:|---:|---:|
| 50 | 43 | 86.0% |
| 100 | 87 | 87.0% |
| 250 | 202 | 80.8% |
| 500 | 397 | 79.4% |
| 1,000 | 769 | 76.9% |
| 1,413 | 1,054 | 74.6% |

## Cross-check: Brown-only ranking (top 50)

If we rank by Brown's POS-tagged verb counts directly (no wordfreq), the mapping covers **39/50 (78%)** of the 50 most-frequent Brown verbs. Brown is genre-narrow (1961 written American English), so this is a sanity check, not the headline number.

## Top high-frequency verbs absent from the mapping

These are the highest-frequency verbs (by the combined Brown+wordfreq method above) that are not in `mappings_final_clean.csv`. Adding them would yield the largest coverage gain per row.

| Pool rank | Verb | Zipf freq | Brown count |
|---:|---|---:|---:|
| 6 | do | 6.35 | 3,368 |
| 7 | time | 6.29 | 16 |
| 23 | man | 5.82 | 18 |
| 31 | help | 5.75 | 352 |
| 36 | end | 5.68 | 140 |
| 39 | keep | 5.66 | 523 |
| 42 | free | 5.63 | 28 |
| 56 | point | 5.54 | 143 |
| 61 | include | 5.21 | 260 |
| 82 | single | 5.41 | 13 |
| 83 | become | 5.40 | 763 |
| 86 | lose | 5.08 | 274 |
| 88 | matter | 5.38 | 35 |
| 111 | further | 5.31 | 13 |
| 116 | market | 5.29 | 41 |
| 117 | near | 5.29 | 19 |
| 119 | list | 5.28 | 59 |
| 124 | program | 5.27 | 21 |
| 127 | process | 5.26 | 34 |
| 134 | seem | 5.08 | 831 |
| 141 | space | 5.23 | 11 |
| 149 | account | 5.21 | 49 |
| 156 | share | 5.20 | 105 |
| 157 | center | 5.19 | 34 |
| 158 | couple | 5.19 | 21 |
| 165 | present | 5.18 | 158 |
| 174 | average | 5.16 | 26 |
| 184 | evidence | 5.14 | 14 |
| 190 | amount | 5.13 | 56 |
| 194 | felt | 5.13 | 356 |
| 195 | match | 5.13 | 77 |
| 196 | step | 5.13 | 71 |
| 198 | range | 5.12 | 63 |
| 200 | trade | 5.12 | 47 |
| 206 | complete | 5.10 | 106 |
| 209 | title | 5.10 | 12 |
| 210 | attack | 5.09 | 63 |
| 212 | damn | 5.09 | 30 |
| 213 | decide | 4.78 | 205 |
| 215 | release | 5.09 | 39 |
| 220 | increase | 5.08 | 332 |
| 225 | begin | 4.84 | 583 |
| 226 | figure | 5.07 | 48 |
| 228 | forget | 5.06 | 117 |
| 236 | risk | 5.05 | 17 |
| 241 | allow | 5.01 | 208 |
| 242 | fan | 4.92 | 13 |
| 248 | effect | 5.02 | 31 |
| 256 | campaign | 5.00 | 12 |
| 258 | credit | 5.00 | 16 |
