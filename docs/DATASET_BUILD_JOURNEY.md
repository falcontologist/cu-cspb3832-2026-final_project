# Dataset Build Journey

Companion document to [Final Project Report.pdf](../Final%20Project%20Report.pdf). The report covers the what and the results. This file covers the how: the phases that produced the training data, which design decisions shape it, and where to find each artifact in the repo.

Paths below are relative to the repo root unless otherwise noted.

---

## 0. Project Context

### What the classifier does

The cross-encoder is the first stage of a knowledge graph construction pipeline. Given a sentence, it identifies which of 62 verbal clause constructions best captures the sentence's argument structure. Each construction pairs a syntactic form (predicate plus arguments) with a force-dynamic event structure, grounded in Croft (2012, 2021, 2022) and Kalm (2022). The constructions are also called Situations in the artifacts below (the original term used in code and filenames).

### End-to-end pipeline, as deployed

1. **Dependency parse** (spaCy `en_core_web_sm`): identify the main verb via the ROOT dependency.
2. **Lemmatize** (spaCy `token.lemma_`): take the main verb's lemma.
3. **Candidate retrieval**: look up the lemma in [data/verb_candidates.json](../data/verb_candidates.json) to get the candidate constructions (those where the lemma appears in at least one positive training example).
4. **Cross-encoder scoring**: for each candidate construction, tokenize the pair `[CLS] sentence [SEP] construction definition [SEP]` and score with the fine-tuned DeBERTa-v3-base. Average softmax scores across all five fold checkpoints and pick the highest.
5. **Downstream**: the winning construction's participant roles map to knowledge graph relations, producing structured event triples.

### What the pipeline was originally going to be

The candidate retrieval stage was designed to use a richer lexicon: lemma → WordNet synsets → VerbNet classes via SemLink → candidate constructions via [data/mappings_final_clean.csv](../data/mappings_final_clean.csv) (3,258 unique verbs, 4,605 verb-to-construction pairs). That design never got wired in. The deployed lookup, built from `verb_candidates.json`, covers only the 546 verbs that happened to appear in positive training examples, with an average of 1.11 candidates per verb (against 1.34 in the hand-curated lexicon). The consequence: 91% of known verbs have a single-candidate set and random selection is trivially correct for them, which is why the constrained-accuracy baseline is 90.8%. See the report's Discussion and Future Work sections and [docs/TODO_NEXT_ROUND.md](TODO_NEXT_ROUND.md) for the plan to close this gap.

### Model and training

- **Backbone**: DeBERTa-v3-base.
- **Initialization**: NLI-pretrained weights (`cross-encoder/nli-deberta-v3-base`). The parallel is structural: NLI asks whether sentence A's semantics entail sentence B's claim; construction classification asks whether sentence A's argument structure entails construction B's definition.
- **Input format**: `[CLS] sentence [SEP] construction definition [SEP]`; classification head on the CLS token's final hidden state; two labels.
- **Training**: 5-fold stratified cross-validation; AdamW with learning rate 2e-5 and weight decay 0.01; linear warmup over 10% of steps; effective batch size 32 (batch 8 with gradient accumulation 4); max sequence length 384; loss weighting 0.7 on synthetic rows and 1.5 on T1-override rows; early stopping on dev F1 with patience 2.
- **Hardware**: Apple M4 Mac Mini, 24 GB unified memory, MPS backend. About 17 hours total wall time across the five folds (per-fold metrics in [results/cv_summary.json](../results/cv_summary.json)).
- **Evaluation**: overall accuracy, macro F1, and per-construction F1; candidate-constrained accuracy against the random baseline; per-tier accuracy; corpus vs. synthetic F1. Full output in [results/evaluation_report.md](../results/evaluation_report.md).

### Why the dataset shape matters

The candidate set at inference is small (1–4 constructions for most verbs), but the candidates are semantically close by construction. The classifier's job is to learn fine boundaries between structurally similar event types. The dataset's tier structure (T1 boundary-adjacent, T2 prototypical, T3 peripheral) directly trains this discrimination, which the results back up: the weakest pairs are exactly the ones with the thinnest T1 support (the Emotion pair) or with irreducible causative/inchoative overlap (the Change-of-State cluster).

---

## 1. Final Dataset Shape

**62 constructions** across three realms (Physical / Mental / Social). **13,186 labeled sentence-definition pairs**:

| | Rows | Corpus-attested | Synthetic |
|---|---:|---:|---:|
| Positives | 3,886 | 3,078 | 808 |
| Negatives | 9,300 | 8,594 | 706 |
| **Total** | **13,186** | **11,672** | **1,514** |

The per-construction pos and neg files live at [data/situation_splits/positives/](../data/situation_splits/positives/) and [data/situation_splits/negatives/](../data/situation_splits/negatives/).

Schema (both pos and neg):

```
sentence, verb_lemma, verb_token_idx, on_sense, wn_synsets, vn_class,
situation, match_path, source_file, sentence_idx, situation_count, needs_review
```

Provenance column `match_path`:
- Corpus-attested rows: `WN`, `ontonotes`, `COCA via Croft et al 2021`, `framenet`, etc.
- Synthetic rows: `synthetic`.
- Neg-recovered pos rows (rare): `neg_recovery`.

---

## 2. Supporting Artifacts

| File | Purpose |
|---|---|
| [docs/situation_scope_map_inductive.md](situation_scope_map_inductive.md) | Per-construction scope: event type, verb inventory with ON senses, VN classes, boundary tests. 62 entries plus 39 shared-verb boundary rules plus 7 flagged ambiguities. |
| [data/tier_config.json](../data/tier_config.json) | Tier ratios (T1=50%, T2=30%, T3=20%), target 50 per construction, 15% verb cap. |
| [data/tier_labels.json](../data/tier_labels.json) | Every pos row labeled T1/T2/T3 with a `source` field (`override` for synthetic, `mechanical` for corpus). |
| [docs/tier_census.md](tier_census.md) | Per-construction tier counts against targets. All 62 constructions meet or exceed T1≥25, T2≥15, T3≥10. |
| [data/synthetic_tier_overrides.json](../data/synthetic_tier_overrides.json) | Intended-tier labels for synthetic rows. Keyed by `{situation}\|\|{verb_lemma}\|\|{sentence}`. |
| [data/asc_definitions.json](../data/asc_definitions.json) | The 62 construction definitions paired with each sentence at training and inference time. |
| Croft and Kalm reference PDFs | 62 excerpts consulted for scope-map induction, especially for the 7 boundary ambiguities. Not tracked in the repo because the PDFs are copyrighted; see [LARGE_FILES.md](../LARGE_FILES.md). |

---

## 3. The Three-Realm Cluster Taxonomy

Tier structure is cluster-relative. A negative from the same cluster as the target is T1 (hard); same realm, different cluster is T2 (medium); different realm is T3 (easy). Final clusters:

### PHYSICAL

| Cluster | Members |
|---|---|
| Motion | Motion, Vehicular_Motion, Carrying, Sending, Pick_Up_and_Drop_Off, Location, Throwing, Pursuit |
| Change_of_State | Change_of_State, Cause_Change_of_State, Hurt |
| Force | Contact, Manipulation, Constrain, Capacity |
| Incremental | Incremental, Cause_Incremental, Concealment |
| Ingestion | Ingestion, Feeding |
| Creation | Cause_Creation, Image_Creation, Form, Emission |
| Existence | Existence (solo) |

### MENTAL

| Cluster | Members |
|---|---|
| Perception | Perception_(exp._subj.), Perception_(stim._subj.) |
| Emotion | Emotion_(exp. subj.), Emotion_(stim. subj.) |
| Intention | Desire, Intention |
| Cognition | Learning, Discovery |
| Evaluation | Evaluation, Counting, Measurement |
| Causation | Cause_and_Effect (solo) |

### SOCIAL

| Cluster | Members |
|---|---|
| Possession | Possession, Dynamic_Possession, Transfer_of_Possession, Buying, Selling, Payment, Future_Having, Charge |
| Communication | Communicate, Statement, Joint_Statement, Request, Response |
| Affiliation | Membership, Cause_Membership, Participation, Cause_Participation, Collective |
| Control | Enforcement, Limitation, Induction |
| Aggression | Aggression, Protection |
| Reciprocal | Reciprocal, Replacement |

**Solo-cluster and small-cluster constructions** (Existence, Cause_and_Effect, plus one-sibling clusters such as Ingestion/Feeding) are given scope-map-close donors as honorary T1 to reach the 35% hard-negative threshold.

---

## 4. Build Journey

### Phase I: Automated extraction from OntoNotes via VerbNet class mappings

The original plan was to bulk-extract training sentences from OntoNotes 5.0, using `mappings_final_clean.csv` to map each verb's VerbNet class to candidate constructions. The result was cross-construction label bleed. VerbNet classes encode syntactic alternation behavior (Levin, 1993), not force-dynamic event structure. Verbs sharing a VerbNet class (e.g., the bill-54.5 class contains both `charge` and `bet`) were being mapped to the same candidate construction despite instantiating different event structures. Sense-level polysemy compounded this, but the root cause was the taxonomic mismatch. The extracted training data was unusable as-is.

The artifact from this phase, [src/extract_training_data.py](../src/extract_training_data.py), is kept for provenance.

### Phase II: Inductive scope map

Read all 62 positive files (5,211 corpus-attested rows at the time) and induced, for each construction:

- **Event type**: concrete causal-chain description.
- **Subject role**: consistent participant role across examples.
- **Verb senses**: ON sense annotations per verb.
- **VN classes**: Levin/VerbNet syntactic class.
- **Boundaries**: what the construction is NOT, referencing its neighbors.

Cross-construction analysis identified **190 shared verb lemmas** across two or more constructions. Discriminating tests were written for the top 30 or so shared-verb boundaries. 7 pairs remained genuinely ambiguous and were flagged for manual review (e.g., `hope` Desire vs. Intention; `learn` Learning vs. Discovery; `goad` Aggression vs. Induction; `cost` Measurement vs. Charge).

Mid-build scope-map corrections applied:

- Narrowed **Pursuit** to physical co-motion OR directed search toward an unreached target.
- Added six new boundary rules: Pursuit vs. Motion; Pursuit vs. Desire; Limitation vs. Enforcement; Concealment vs. Incremental; Constrain vs. Capacity; Aggression vs. Induction.
- Reframed **Existence** as Croft §4.8 "Internal" (physical entity in undirected process: `shiver`, `flutter`, `swarm`; not abstract existence).
- Added an implicit-perceiver test for **Perception_(stim._subj.) vs. Emission** (`reek of corruption` plus quality predication = PSS; bare emission = Emission).

Artifact: [docs/situation_scope_map_inductive.md](situation_scope_map_inductive.md).

### Phase III: Synthetic positive generation

Target: 50 pos rows per construction, split 25/15/10 (T1/T2/T3). Existing corpus rows were classified mechanically: T1 if the verb appears in at least two constructions' pos files (shared verb); otherwise T2 if the verb is top-3 frequent for this construction; otherwise T3.

Synthetic positives were generated across gap-constructions to fill T1 and T2 deficits. T1 generations used shared verbs in the target's sense OR the construction's canonical verb in a boundary-adjacent frame (per the scope map's discriminating tests). T2 generations used dominant unshared verbs in prototypical frames. T3 generations were peripheral.

**Override mechanism**: the mechanical classifier marked many synthetic T1 rows as T2 because single-construction verbs (Payment=`pay`, Constrain=`wear`) cannot by definition be "shared." An override pass applies `synthetic_tier_overrides.json` during re-classification so intended tiers are respected. The `source` field in `tier_labels.json` is `override` or `mechanical` for traceability.

**Audit** (196 sampled T1 synthetic rows evaluated against the scope map):

- PASS: 95.9%
- WRONG (boundary test assigns to neighbor): 1.0%
- UNNATURAL (tense or figurative issues): 1.0%
- AMBIGUOUS: 2.0%

Four flagged rows were removed and replaced with clean equivalents.

### Phase IV: T2/T3 top-up

Additional rows were added to close residual T2/T3 gaps that emerged after Phase III. Final: all 62 constructions meet or exceed T1≥25, T2≥15, T3≥10 in the positive splits.

### Phase V: Negative audit and rebalance

Under the new three-realm taxonomy, the old cluster map was misaligned. Audit findings:

- **11 neg files were legacy** (never rebuilt in Phase I): 100% self-contaminated (every row's donor label = the target itself).
- **40 constructions had T1 < 35%** under the new taxonomy (some prior T1 donors moved to different clusters).
- **21 constructions had T3 > 35%**.
- **20 constructions had closest-neighbor share < 10%**.
- **About 167 rows across 41 files used legacy donor labels** (Know, Judge, Look, Search, Inducive, Role) that do not map to any current construction.

Contamination check on rebuilt files: 0% contamination in 130 sampled rows.

Rebalance execution:

1. Rebuilt 11 legacy neg files from scratch under the new taxonomy.
2. Rebalanced 40 T1-low constructions by boosting cluster siblings and scope-map-close donors.
3. Cleaned about 167 unknown-donor rows.
4. Boosted closest-neighbor share to ≥10% in 20 constructions (Selling landed at exactly 10% via a targeted swap).

**Final**: 9,300 neg rows; 62/62 at T1≥35% and T3≤35%; 61/62 at closest-neighbor share ≥10%.

---

## 5. Key Design Decisions

### Why 50/30/20 tier ratios?

Half of the negatives should be hard (T1, same cluster) so the classifier learns the fine boundary. 30% medium covers shared-vocabulary confusability. 20% easy confirms baseline discriminability.

### Why weight T1 by closest-neighbor share?

The hardest negative for any construction is its structural-opposite neighbor (Selling ↔ Buying, Cause_Change_of_State ↔ Change_of_State, Emotion_(exp.) ↔ Emotion_(stim.)). Giving ~35% of T1 rows to the closest neighbor concentrates training signal on the most-confusable boundary identified in the scope map.

### Why `match_path=synthetic` as a traceable field?

So downstream filtering can distinguish corpus-attested rows (high confidence in naturalness) from generated rows (high confidence in boundary coverage but occasionally wooden register). In the final training run, synthetic rows were weighted 0.7 and T1-override rows were weighted 1.5.

### Why keep both override and mechanical tier labels?

The mechanical classifier uses "verb appears in ≥2 constructions' pos files" as the T1 test. That works for corpus rows but fails for single-verb constructions. Overrides record the generator's intended tier (from scope map semantics, not verb sharing). The `source` field preserves traceability and could be used to weight losses differently if the training were repeated.

### Why is the scope map the authority?

The curated pos examples define what each construction is. Clusters in the original prompt were coarser-grained; the scope map's induced event types and shared-verb boundaries are the ground truth for what each construction contains. Clusters are retrieval-organization, not semantic ground truth.

---

## 6. Known Limitations

1. **Candidate-lookup gap**: The deployed `verb_candidates.json` covers 546 verbs; the hand-curated `mappings_final_clean.csv` covers 3,258 but was never wired in. This inflates the 90.8% random baseline and narrows the classifier's evaluable work to 51 multi-candidate verbs. See [docs/TODO_NEXT_ROUND.md](TODO_NEXT_ROUND.md).

2. **Verb monoculture in some pos files**: Payment `pay` is 100%; Possession `own` is ~82%; Constrain `wear` is ~89%; Enforcement `control` is ~61%. The 15% verb cap applies to neg files, not pos. The classifier may be leaning on surface verb identity for these constructions rather than event structure.

3. **Emotion pair underperformance**: F1 is 0.71 (stim-subj) and 0.78 (exp-subj), the two weakest constructions in the deck. The structurally analogous Perception pair scores 0.97/0.93. The gap traces to thin boundary-adjacent training data: the Emotion pair met less than half its T1 target on each side. See [docs/tier_census.md](tier_census.md).

4. **Causative/inchoative cluster underperformance**: Change_of_State (0.80), Cause_Change_of_State (0.85), Cause_Creation (0.80), Incremental (0.78). Change_of_State and Cause_Change_of_State both met their T1 targets, so this is not purely a data gap. The cross-encoder appears to struggle with the labile strategy (same verb form for both causative and inchoative senses; Croft 2022, p. 201f).

5. **Small-cluster constructions** (Existence, Cause_and_Effect solo; Ingestion/Feeding, Emotion pair, Perception pair, Cognition pair each with one sibling): hard-negative capacity is bounded by the donor cap times the sibling count. Scope-map-close extensions compensate, but the T1 rows are partly cross-cluster.

6. **Single-source bias**: Many corpus-attested rows come from OntoNotes (news/conversation/web). Croft 2021 and FrameNet add limited genre diversity.

7. **7 scope-map ambiguities remain unresolved** (see the scope map's "Flagged Ambiguities" section). If the classifier struggles on specific verb/construction pairs, those flags are the first place to look.

---

## 7. Training Details

The values below were used in the final run; they are also recorded in [results/cv_summary.json](../results/cv_summary.json) under `args`.

| Parameter | Value |
|---|---|
| Backbone | DeBERTa-v3-base (`cross-encoder/nli-deberta-v3-base`) |
| Input format | `[CLS] sentence [SEP] construction_definition [SEP]` |
| Head | 2-way classification on CLS token hidden state |
| Loss | Cross-entropy with per-sample weighting |
| Optimizer | AdamW (lr=2e-5, weight_decay=0.01) |
| Schedule | Linear warmup over 10% of steps |
| Effective batch size | 32 (per-step batch 8 × grad_accum 4) |
| Max sequence length | 384 |
| Synthetic-row weight | 0.7 |
| T1-override-row weight | 1.5 |
| Epochs | 5 (cap), with early stopping on dev F1 (patience=2) |
| CV | 5-fold stratified on `{construction}_{label}`, verb-lemma leakage checked per fold |
| Hardware | Apple M4 Mac Mini, 24 GB, MPS |
| Wall time | ~17 hours total (about 200 minutes per fold) |

### Split construction

`src/prepare_splits.py` builds one pair per positive row (sentence + gold construction definition, label=1) and one pair per negative row (sentence + donor construction definition, label=0). Pairs are stratified into 5 folds on `{target_situation}_{label}`. A leakage check enforces that every test-set verb lemma also appears in the train or dev set; any test-only verb is swapped into train/dev in exchange for a same-construction, same-label, same-tier replacement. Inside each fold, train/dev split is 85/15, also stratified.

### Inference

Scoring averages softmax probabilities across all five fold checkpoints and returns the highest-scoring construction from the candidate set. Unknown verbs (none in the test set, but possible in production) fall back to scoring against all 62 constructions.

---

## 8. File Inventory

```
.
├── Final Project Report.pdf                   The submitted report.
├── README.md                                  Navigation and reproduction guide.
├── LARGE_FILES.md                             What's excluded and why.
├── requirements.txt
│
├── src/
│   ├── prepare_splits.py                        Fold splits + verb_candidates.
│   ├── train_cross_encoder.py                   Training loop.
│   ├── evaluate.py                              Metrics + constrained accuracy.
│   ├── inference.py                             CLI inference pipeline.
│   ├── demo_server.py                           FastAPI demo server.
│   ├── demo.html                                Demo UI.
│   └── extract_training_data.py                 Abandoned Phase I OntoNotes extractor.
│
├── data/
│   ├── situation_splits/
│   │   ├── positives/                           62 *_pos.csv files, 3,886 rows.
│   │   └── negatives/                           62 *_neg.csv files, 9,300 rows.
│   ├── asc_definitions.json                     62 construction definitions.
│   ├── situation_definitions.json               Short labels for the demo UI.
│   ├── verb_candidates.json                     verb_lemma → candidate constructions (deployed lookup, 546 verbs).
│   ├── mappings_final_clean.csv                 Hand-curated Verb → VN class → construction lexicon (3,258 verbs, not wired in).
│   ├── tier_config.json
│   ├── tier_labels.json
│   └── synthetic_tier_overrides.json
│
├── docs/
│   ├── DATASET_BUILD_JOURNEY.md                 This file.
│   ├── situation_scope_map_inductive.md         62 scope entries + 39 boundary rules + 7 flagged ambiguities.
│   ├── cross_encoder_implementation_prompt.md
│   ├── tier_census.md                           Per-construction tier counts vs. targets.
│   └── TODO_NEXT_ROUND.md                       Post-mortem + next-round plan.
│
├── results/
│   ├── evaluation_report.md                     Full metrics including per-construction F1.
│   ├── cv_summary.json                          Per-fold dev F1 + training args.
│   └── checkpoints/                             Trained model weights (not tracked; see LARGE_FILES.md).
│
└── presentation/
    ├── Final Project Presentation Slides.pdf
    └── Final Project Presentation Slides.html
```

---

## 9. Theoretical Lineage

The construction inventory and its mapping infrastructure draw on a specific intellectual lineage that shapes the dataset's structure:

- **Croft (2012)** *Verbs: Aspect and Causal Structure*: the force-dynamic event model that defines each construction's causal chain. Every construction corresponds to a distinct configuration of force, path, and participant relations.
- **Croft et al. (2021)** *Developing Language-Independent Event Representations*: the cross-linguistic constructional analysis providing the verb class inventories for physical, motion, creation, and mental-event domains. The Physical and Mental realm constructions derive primarily from this work.
- **Croft (2022)** *Morphosyntax: Constructions of the World's Languages*: the broader constructional framework, defining constructions by semantic and information-packaging functions and morphosyntactic forms. The causative-strategy analysis in §5 informs the limitations discussion for the Change-of-State cluster.
- **Kalm (2022)** *Social Verbs: A Force-Dynamic Analysis*: extends Croft's model to social and communicative verbs. The Social realm constructions (commercial transactions, speech acts, social structure, control) derive from this work.
- **Levin (1993)** *English Verb Classes and Alternations*: the syntactic-alternation analysis underlying VerbNet's class structure. VerbNet classes group verbs by shared alternation behavior, which correlates with but does not determine event structure.
- **VerbNet / WordNet / FrameNet / PropBank via SemLink**: the resource infrastructure that `mappings_final_clean.csv` bridges (lemma → WordNet synsets → VerbNet classes → constructions). The deployed pipeline does not use this chain.
- **OntoNotes 5.0**: the primary source of corpus-attested training sentences. Sense annotations in `.sense` files disambiguate verb polysemy; parse trees in `.parse` files provide the sentence text and syntactic structure.

The key insight from this lineage: VerbNet classes encode *syntactic* behavior (alternation patterns), while constructions encode *semantic* event structure (force-dynamic causal chains). These overlap substantially but not perfectly. Two verbs in the same VN class may instantiate different causal chains (the bill-54.5 problem: `charge` vs. `bet`). Two verbs in different VN classes may instantiate the same causal chain. The classifier must learn the semantic distinction, not the syntactic grouping. That constraint drove the Phase I pivot from automated VN-class mapping to the inductively defined scope map in Phase II.
