# Gold Dataset Build — Journey Summary

Reference document for the cross-encoder ASC (argument structure construction) sentence classifier training. Summarizes how the current pos/neg datasets were constructed, which design decisions shape them, and where to find each artifact.

---

## 0. Project Context

### What this classifier does
The cross-encoder is Stage 1 of a knowledge graph construction pipeline. Given a sentence, it identifies which of 62 Situation ASCs best captures the sentence's argument structure. Situations are constructional patterns pairing a form (predicate + arguments) with a meaning (force-dynamic event structure), grounded in Croft (2012; 2021) and Kalm (2022).

### End-to-end pipeline
1. **Dependency parse** (spaCy `en_core_web_sm`): identify the main verb via ROOT dependency.
2. **Lemmatize + lookup** (NLTK): retrieve WordNet synsets for the lemma, map to VerbNet classes via SemLink.
3. **Candidate retrieval**: VerbNet classes → candidate Situation ASCs via `mappings_final_clean.csv` (4,605 verb-to-Situation mappings across 3,258 unique verbs, 62 Situations).
4. **Cross-encoder scoring**: for each candidate, concatenate `[sentence] [SEP] [ASC definition]` and score with the fine-tuned model. Select highest-scoring Situation.
5. **Downstream**: the winning Situation's constructional pattern specifies participant roles, producing structured event representations for KG triples.

### Model architecture
- **Backbone**: DeBERTa-v3-base (`microsoft/deberta-v3-base`). Outperforms BERT and RoBERTa on sentence-pair tasks; handles fine-grained token interactions needed for ASC definition matching.
- **Initialization**: NLI-pretrained weights (structural parallel: NLI determines whether sentence A's semantics align with sentence B's claim; ASC classification determines whether sentence A's argument structure aligns with ASC definition B).
- **Input format**: `[CLS] sentence [SEP] ASC_definition [SEP]` → classification head on `[CLS]` representation.
- **Training hardware**: Apple M4 Mac Mini, 24GB unified memory, MPS backend. Batch size constrained by memory; 5-fold stratified cross-validation planned.
- **Evaluation**: precision, recall, F1 per Situation; benchmarked against random selection among the verb's candidate ASCs.

### Why this dataset matters
The candidate set retrieved by VerbNet lookup is small (typically 2-6 Situations per verb), but the candidates are semantically close by construction (they share VN classes). The classifier must learn the fine boundaries between structurally similar event types. The dataset's tier structure (T1 boundary-adjacent, T2 prototypical, T3 peripheral) directly trains this discrimination.

---

## 1. Final Dataset Shape

**62 Situations** across three realms (Physical / Mental / Social), **15,283 labeled rows total**:

| Artifact | Path | Rows |
|---|---|---|
| Positives | `situation_splits/positives/{Situation}_pos.csv` | **5,983** across 62 files |
| Negatives | `situation_splits/negatives/{Situation}_neg.csv` | **9,300** across 62 files |

Schema (both pos and neg):
```
sentence, verb_lemma, verb_token_idx, on_sense, wn_synsets, vn_class,
situation, match_path, source_file, sentence_idx, situation_count, needs_review
```

Provenance column `match_path`:
- Corpus-attested rows: `WN`, `ontonotes`, `COCA via Croft et al 2021`, `framenet`, etc.
- Synthetic rows (generated in Phase 1): `synthetic`
- Neg-recovered pos rows (if any): `neg_recovery`

---

## 2. Supporting Artifacts

| File | Purpose |
|---|---|
| [situation_scope_map_inductive.md](situation_scope_map_inductive.md) | Per-Situation scope: event type, verb inventory with ON senses, VN classes, boundary tests. 62 entries + 39 shared-verb boundary rules + 7 flagged ambiguities. |
| [tier_config.json](tier_config.json) | Tier ratios (T1=50%, T2=30%, T3=20%), target=50/Situation, 15% verb cap. |
| [tier_labels.json](tier_labels.json) | Every pos row labeled T1/T2/T3 with `source` field (`override` for synthetic, `mechanical` for corpus). |
| [tier_census.md](tier_census.md) | Per-Situation tier counts vs targets. All 62 Situations balanced. |
| [synthetic_tier_overrides.json](synthetic_tier_overrides.json) | 776 synthetic rows mapped to their intended T1/T2/T3 + `near_neighbor`. Keyed by `{situation}\|\|{verb_lemma}\|\|{sentence}`. |
| [Croft_Kalm_excerpts/](Croft_Kalm_excerpts/) | 62 PDFs (Croft §4 & Kalm 2022), consulted for 7 shared-verb boundaries where examples alone didn't disambiguate. |

---

## 3. The Three-Realm Cluster Taxonomy

Tier structure is cluster-relative. A negative from the same cluster as the target is T1 (hard); same realm, different cluster is T2 (medium); different realm is T3 (easy). Clusters (final form):

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

**Solo-cluster & small-cluster Situations** (Existence, Cause_and_Effect, plus 1-sibling clusters like Ingestion/Feeding) are given scope-map-close donors as honorary T1 to reach the 35% hard-negative threshold. These extensions are listed in the rebalance script (`SCOPE_MAP_CLOSE` dict).

---

## 4. Build Journey

### Phase I — Initial Negative Fill (per-Situation, pre-scope-map)

Built negatives for each Situation under an older cluster map. Method:
- Donor pool = all other Situations' pos files.
- T1 (hard) weighted by closest-neighbor share (~35%), remaining spread across cluster siblings.
- T2 (medium) from adjacent clusters with shared lexical cues.
- T3 (easy) spread widely across distant Situations.
- Caps: verb ≤15%, donor ≤20%, dedupe on `(sentence, verb_lemma)`, never donate a row from target's own pos.

Output: 51 of 62 neg files rebuilt at this stage (11 legacy files untouched until Phase IV).

### Phase II — Inductive Scope Map

Read all 62 pos files (5,211 corpus-attested rows at the time). For each Situation, induced:
- **Event type** — concrete causal-chain description
- **Subject role** — consistent participant role across examples
- **Verb senses** — ON sense annotations per verb
- **VN classes** — Levin/VerbNet syntactic class
- **Boundaries** — what the Situation is NOT, referencing neighbors

Cross-Situation analysis identified **190 shared verb lemmas** across ≥2 Situations. Discriminating tests written for the top ~30 shared-verb boundaries. 7 pairs genuinely ambiguous and flagged for Josh's review (e.g., `hope` Desire vs. Intention; `learn` Learning vs. Discovery; `goad` Aggression vs. Induction; `cost` Measurement vs. Charge).

**Scope map corrections** (applied mid-build):
- Narrowed **Pursuit** to physical co-motion OR directed search toward unreached target
- Added 6 new boundary rules: Pursuit vs. Motion; Pursuit vs. Desire; Limitation vs. Enforcement; Concealment vs. Incremental; Constrain vs. Capacity; Aggression vs. Induction
- **Existence** reframed as Croft §4.8 "Internal" (physical entity in undirected process — shiver, flutter, swarm — not abstract existence)
- **Perception_(stim._subj.) vs. Emission**: implicit-perceiver test added (`reek of corruption` + quality predication → PSS; bare emission → Emission)

Artifact: [situation_scope_map_inductive.md](situation_scope_map_inductive.md).

### Phase III — Synthetic Positive Generation

Target: 50 pos rows/Situation, split 25/15/10 (T1/T2/T3). Existing corpus rows classified mechanically: T1 if verb appears in ≥2 Situations' pos files (shared); else T2 if top-3 frequent for this Situation; else T3.

**731 synthetic positives generated** across 49 gap-Situations. T1 generations used shared verbs in the target's sense OR the Situation's canonical verb in a boundary-adjacent frame (per scope-map discriminating tests). T2 generations prototypical with dominant unshared verbs. T3 peripheral.

**Override mechanism**: the mechanical classifier marked many synthetic T1 rows as T2 (because Payment=`pay`, Constrain=`wear`, etc. are single-Situation monoculture verbs — no sharing possible). An override pass uses `synthetic_tier_overrides.json` to respect intended tiers during re-classification. `source` field in `tier_labels.json` is `override` vs. `mechanical` for traceability.

**Audit** (196 sampled T1 synthetic rows evaluated against scope map):
- PASS: 95.9%
- WRONG (boundary test assigns to neighbor): 1.0%
- UNNATURAL (tense/figurative issues): 1.0%
- AMBIGUOUS: 2.0%

4 flagged rows removed and replaced with clean equivalents.

### Phase IV — Small T2/T3 Top-up

45 additional rows added to close residual T2/T3 gaps that emerged post-Phase III. Final: **all 62 Situations meet or exceed T1≥25, T2≥15, T3≥10**.

### Phase V — Negative Audit & Rebalance

Under the new three-realm taxonomy, the old cluster map was misaligned. Audit findings:
- **11 neg files were still legacy** (never rebuilt in Phase I) — 100% self-contaminated (every row's donor label = the target itself)
- **40 Situations had T1 < 35%** under new taxonomy (some prior T1 donors moved to different clusters)
- **21 Situations had T3 > 35%**
- **20 Situations had closest-neighbor share < 10%**
- **~167 rows across 41 files used legacy donor labels** (Know, Judge, Look, Search, Inducive, Role) that don't map to any current Situation

Contamination check on rebuilt files: **0% contamination in 130 sampled rows**.

**Rebalance execution** (4 priorities, all completed):
1. Rebuilt 11 legacy neg files from scratch under new taxonomy
2. Rebalanced 40 T1-low Situations by boosting cluster siblings + scope-map-close donors
3. Cleaned ~167 unknown-donor rows
4. Boosted closest-neighbor share to ≥10% in 20 Situations (Selling landed at exactly 10% via targeted swap)

**Final**: 9,300 neg rows. 62/62 at T1≥35%, T3≤35%. 61/62 at closest≥10%.

---

## 5. Key Design Decisions

### Why 50/30/20 tier ratios?
Half of negatives should be hard (T1 — same cluster) so the classifier learns the fine boundary. 30% medium to cover shared-vocabulary confusability. 20% easy to confirm baseline discriminability.

### Why weight T1 by closest-neighbor share?
The hardest negative for any Situation is its structural-opposite neighbor (Selling ↔ Buying, Cause_Change_of_State ↔ Change_of_State, Emotion_(exp.) ↔ Emotion_(stim.)). Giving ~35% of T1 rows to the closest neighbor concentrates training signal on the most-confusable boundary per the scope map.

### Why `match_path=synthetic`?
So downstream filtering can distinguish corpus-attested rows (high confidence in naturalness) from generated rows (high confidence in boundary coverage but occasional wooden register). Useful if you want to train on corpus-only first then add synthetic, or upweight/downweight by source.

### Why keep both overrides and mechanical labels?
Mechanical classifier: uses `verb appears in ≥2 Situations' pos files` as the T1 test. Good for corpus rows; inadequate for single-verb Situations. Overrides record the generator's intended tier (from scope map semantics, not verb sharing). Use the `source` field to weight losses differently if needed.

### Why the scope map is the authority?
The curated pos examples define the Situations. Clusters in the prompt originally were coarser-grained; the scope map's induced event types + shared-verb boundaries are the ground truth for what each Situation contains. Clusters are retrieval-organization, not semantic ground truth.

---

## 6. Known Limitations

1. **Verb monoculture in some pos files**: Payment `pay` is 100%; Possession `own` ~82%; Constrain `wear` ~89%; Enforcement `control` ~61%. The 15% verb cap applies to neg files, not pos. If the classifier overfits to surface verb → Situation, consider augmenting pos files with paraphrased synonyms.

2. **Small-cluster Situations** (Existence, Cause_and_Effect solo; Ingestion/Feeding, Emotion pair, Perception pair, Cognition pair = 1 cluster sibling each): hard-negative capacity is bounded by the donor cap × sibling count. Scope-map-close extensions compensate but the T1 rows are partly cross-cluster.

3. **Single-source bias**: Many corpus-attested rows come from OntoNotes (news/conversation/web). Croft-2021 and framenet add limited diversity. Cross-encoder may need register-balance checks.

4. **Classifier label for new rows**: `tier_labels.json` regenerates from scratch each run. If you add new pos rows, regenerate via `tier_label_v2.py` (the override-aware version).

5. **7 scope-map ambiguities remain unresolved** (see the scope map's Flagged Ambiguities section). If the trained classifier struggles on specific verb/Situation pairs, those flags are the first place to look.

6. **Verb-shared rows in tiny counts**: The mechanical T1 detector requires ≥2 Situations' pos files to share a verb lemma. A few shared-verb relations are represented by 1-row instances and are not robust T1 signals.

---

## 7. Recommended Training Considerations

### Input pair construction
The cross-encoder input is `[CLS] sentence [SEP] ASC_definition [SEP]`. The ASC definition is the string description of the Situation (event type, participant roles). Each pos row generates one positive pair. For negatives, draw N neg rows from the target Situation's neg file per positive, maintaining the 50/30/20 T1/T2/T3 sampling ratio within each batch (not uniform across the neg file, which would skew toward whatever tier is largest).

### Candidate-set-aware negative sampling
At inference, the classifier only scores against candidate ASCs retrieved via the VerbNet lookup. Training should reflect this constraint: for each sentence, the negative ASC definitions should come primarily from Situations that share VerbNet classes with the gold Situation (i.e., Situations that would appear in the candidate set for the same verb). The neg files already encode this through the cluster-based T1 structure, but explicit candidate-set filtering during batch construction would further improve realism.

### Hard-negative mining
After initial training, re-sample T1 negatives per Situation based on the `near_neighbor` field to build focused hard-negative batches for fine-boundary epochs. The scope map's shared-verb boundaries identify exactly which pairs need the most training signal.

### Per-Situation evaluation
Report F1 per Situation on a held-out split. Expect lower F1 on:
- Solo-cluster Situations (Existence, Cause_and_Effect) with limited hard-negative diversity
- Pairs with flagged scope-map ambiguities (Desire/Intention, Learning/Discovery, Aggression/Induction)
- Verb-monoculture Situations (Payment, Constrain, Possession) where the classifier may learn verb identity rather than event structure

### Boundary-test evaluation
For each shared-verb boundary in the scope map, construct a balanced test set of N pos + N neg pairs using that shared verb. Measure per-boundary accuracy. This directly scores the classifier's fine-grained discrimination and reveals which boundaries need more training data.

### Corpus vs. synthetic weighting
The `match_path` field distinguishes corpus-attested rows (high naturalness confidence) from synthetic rows (high boundary-coverage confidence but occasionally wooden register). Options:
- Train on corpus-only first, then fine-tune with synthetic added (curriculum)
- Train jointly but downweight synthetic rows' loss contribution (e.g., 0.7x)
- Train jointly at equal weight (simplest; the 95.9% audit pass rate suggests quality is adequate)

### Override-aware loss weighting
Synthetic T1 rows from `synthetic_tier_overrides.json` are boundary-adjacent by design. If training plateaus on boundary discrimination, increase their loss weight specifically.

### Stratified splitting
When creating train/dev/test splits, stratify by Situation AND by tier. Ensure each split has T1/T2/T3 representation per Situation. Also ensure no verb lemma appears in test that doesn't appear in train (to prevent unseen-verb test failures from confounding ASC discrimination evaluation).

### ASC definition sensitivity
The string ASC definitions paired with sentences are the second half of the cross-encoder input. Their wording directly affects what the model learns. If two ASC definitions are too similar in surface form, the model may struggle to distinguish them even with good training data. Consider testing with both terse definitions (event type only) and rich definitions (event type + participant roles + example verb) to find the optimal granularity.

---

## 8. File Inventory for Training

```
Scripts/
├── situation_splits/
│   ├── positives/*.csv                    # 62 pos files, 5,983 rows total
│   └── negatives/*.csv                    # 62 neg files, 9,300 rows total
├── mappings_final_clean.csv               # 4,605 verb→Situation mappings (VN/WN bridge)
├── situation_scope_map_inductive.md       # scope definitions + boundary rules
├── tier_config.json                       # ratios + target + verb cap
├── tier_labels.json                       # all pos rows labeled T1/T2/T3
├── tier_census.md                         # per-Situation tier counts
├── synthetic_tier_overrides.json          # intended-tier map for synthetic rows
├── extract_training_data.py               # OntoNotes extraction script (Phase I source)
└── Croft_Kalm_excerpts/*.pdf              # reference material, 62 excerpts
```

---

## 9. Theoretical Lineage

The Situation inventory and its mapping infrastructure draw on a specific intellectual lineage that shapes the dataset's structure:

- **Croft (2012)** *Verbs: Aspect and Causal Structure*: the force-dynamic event model that defines each Situation's causal chain. Every Situation corresponds to a distinct configuration of force, path, and participant relations.
- **Croft et al. (2021)** *Morphosyntax*: the cross-linguistic constructional analysis providing the verb class inventories for physical, motion, creation, and mental-event domains. The Physical and Mental realm Situations derive primarily from this work.
- **Kalm (2022)** PhD dissertation: extends Croft's model to social and communicative verbs. The Social realm Situations (commercial transactions, speech acts, social structure, control) derive from this work.
- **Levin (1993)** *English Verb Classes and Alternations*: the syntactic alternation analysis underlying VerbNet's class structure. VerbNet classes group verbs by shared alternation behavior, which correlates with (but does not determine) event structure.
- **VerbNet/WordNet/FrameNet/PropBank** via SemLink: the resource infrastructure bridging verb lemmas → synsets → VN classes → Situations. The mapping chain: lemma → WordNet synsets (NLTK) → VerbNet classes (SemLink) → Situation ASCs (mappings_final_clean.csv).
- **OntoNotes 5.0**: the primary source of corpus-attested training sentences. Sense annotations in `.sense` files disambiguate verb polysemy; parse trees in `.parse` files provide the sentence text and syntactic structure.

The key insight from this lineage: VerbNet classes encode *syntactic* behavior (alternation patterns), while Situations encode *semantic* event structure (force-dynamic causal chains). These overlap substantially but not perfectly. Two verbs in the same VN class may instantiate different causal chains (the bill-54.5 problem: `charge` vs. `bet`). Two verbs in different VN classes may instantiate the same causal chain. The classifier must learn the semantic distinction, not the syntactic grouping.
