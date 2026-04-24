# TODO — Next Round

## Wire the curated verb-lemma lexicon into the pipeline

### What happened this round

The candidate-pool constraint in the inference pipeline was built from whichever verb lemmas appeared in the curated positive training files (546 verbs), rather than from the hand-curated `mappings_final_clean.csv` lexicon (3,258 verbs, 4,605 verb→Situation pairs) that was intended to drive candidate retrieval.

As a result, 84% of the curated verb coverage is dormant at inference. Out-of-training-vocabulary verbs fall back to scoring against all 62 Situations instead of being constrained to their lexicographically-motivated candidate set.

### Evidence

- `mappings_final_clean.csv` is referenced only by `extract_training_data.py` (the abandoned Phase I OntoNotes extractor) and documentation files. `grep -rn mappings_final` against `inference.py`, `prepare_splits.py`, `train_cross_encoder.py`, `evaluate.py`, and `demo_server.py` returns zero hits.
- `prepare_splits.build_verb_candidates` generates `verb_candidates.json` directly from training pos rows via `verb_lemma → file_situation`.

### Comparison

| | Intended (`mappings_final_clean.csv`) | Actually used (`verb_candidates.json`) |
|---|---:|---:|
| Unique verbs | 3,258 | 546 |
| verb→Situation pairs | 4,605 | ~606 |
| Avg candidates / verb | 1.34 | 1.11 |
| Multi-candidate verbs | 848 (26%) | 51 (9%) |
| Unique Situation labels | 68 | 62 |

532 of the 546 used verbs are in the intended map (near-total overlap on the narrow side). 2,726 verbs in the intended map are unreachable at inference. Only 14 verbs are in the training vocabulary but missing from the map.

### Action plan

1. **Reconcile Situation taxonomy.** The mapping uses an earlier 68-Situation labeling (e.g., "Attack", "Basic Motion", "Dynamic Possession"); training uses 62 (e.g., "Aggression", "Motion", "Dynamic_Possession"). Only 32 Situation names match exactly. Build a `situation_name_aliases.json` that translates the map's labels into the current taxonomy. Flag any map-side Situations that no longer exist so they can be dropped or remapped.

2. **Replace `verb_candidates.json` in the loaders.** Swap the lookup source in `inference.py`, `evaluate.py`, and `demo_server.py` to read from the reconciled `mappings_final_clean.csv`. Keep the same key format (`verb_lemma → [Situation, …]`) to minimize downstream change.

3. **Audit long-tail behavior.** 2,726 map-only verbs have no positive training examples. Constraining these verbs to their map candidates may hurt precision if the model has not been exposed to the relevant sense/construction pair. Sample a few hundred, run through the classifier under both regimes (constrained vs. unconstrained), and measure. Decide whether to: (a) apply the constraint globally, (b) apply it only to verbs with ≥1 training example, (c) mix via a confidence threshold.

4. **Report metrics on the contested band.** Currently the 96.7% constrained accuracy is inflated by the 91% of verbs with only one candidate. Report macro-F1 and constrained accuracy *within the multi-candidate subset* separately, so the classifier's discrimination work is visible on its own.

### Expected impact

- Constrained candidate sets for roughly 5× more verbs
- Multi-candidate regime (where the cross-encoder's work is real) grows from ~51 verbs to ~848
- Average candidate set size rises from 1.11 to 1.34 — the model gets exercised on a meaningfully larger share of inputs

### Related presentation artifacts

- Pipeline slide in `Final Project Presentation Slides.html` labels the Verb Lemma stage as "NLTK / WordNet"; the actual code uses spaCy for both parsing and lemmatization. Update if the deck is revised.

---

## Balance positive examples to ~150 per Situation

### What happened this round

Positive examples were built to a target of 50/Situation (`tier_config.json`), later exceeded in some cases via Phase III/IV synthetic generation. Negatives were built to a flat 150/Situation. Final counts:

| | Total | Per-Situation (avg) | Per-Situation (range) |
|---|---:|---:|---:|
| Positives | 3,886 | 63 | 50–177 |
| Negatives | 9,300 | 150 | 150–150 |

Negative:positive ratio ≈ **2.39:1**. 61 of 62 Situations are below 150 positives. Scaling positives to match negatives at 150/Situation requires **~5,441 additional positive examples** across the 61 under-filled Situations.

### Rationale

The class imbalance biases the classifier toward the negative label and inflates constrained-accuracy headroom for Situations with thin positive support. A balanced 150/150 positive/negative ratio per Situation gives the cross-encoder equal exposure to in-scope and out-of-scope instances at the boundary, improving discrimination especially on the contested multi-candidate verbs that the lexicon wiring (above) will expose more often.

### Action plan

1. **Reuse the Phase III tiered synthetic-generation method**, scaled. Per-Situation target 150 pos, split 75 T1 / 45 T2 / 30 T3 (keeping the 50/30/20 ratio). Use the existing `situation_scope_map_inductive.md` boundary rules and scope-map-close neighbor list to drive T1 generation; expand T2/T3 diversity via the shared-verb and cluster-sibling inventories.

2. **Prioritize Situations with the largest pos gap.** Current gaps (150 − current count) are largest for Aggression, Buying, Capacity, and other Situations sitting near 50. Generate in tranches and re-run `tier_census.md` after each tranche to track progress and re-prioritize.

3. **Re-run the T1 audit on each tranche.** Phase III's 95.9% pass rate was measured at much smaller scale; a 5,441-row expansion needs periodic audits (sample ~200 T1 rows per tranche) to catch any drift in generator quality or scope-map interpretation.

4. **Rebuild folds and negatives** after each tranche. `prepare_splits.py` must be rerun so the 5-fold splits reflect the new positive pool. Negatives were balanced to the previous positive set; the negative sampler should not need regeneration unless the pos-row → neg-row ratio changes the per-batch sampling math.

5. **Retrain** once positives hit 150/Situation and re-run `evaluate.py`. Compare to current metrics (94.4% macro F1, 96.7% constrained accuracy) to quantify the gain from balanced exposure — particularly on the multi-candidate subset.

### Expected impact

- Per-Situation positive support rises from 63 (avg) → 150
- Total positives: 3,886 → ~9,300 (parity with negatives)
- Pos:neg ratio: 1:2.39 → 1:1
- Predicted: meaningful lift on Situations currently below 60 positives (where the classifier is thinnest)
