# Cross-Encoder ASC Classifier: Implementation Prompt

## Context

You are building a cross-encoder classifier that scores `[sentence, ASC_definition]` pairs to identify which of 62 Situation ASCs best captures a sentence's argument structure. This is Stage 1 of a knowledge graph construction pipeline.

The gold dataset (15,283 rows: 5,983 positives across 62 Situations, 9,300 negatives with tiered difficulty) is complete and lives in:

```
Base: /Users/joshfalconer/Documents/Verbs_to_Situations/Scripts/
├── situation_splits/
│   ├── positives/{Situation}_pos.csv    # 62 files, 5,983 rows
│   └── negatives/{Situation}_neg.csv    # 62 files, 9,300 rows
├── mappings_final_clean.csv             # 4,605 verb→Situation mappings
├── situation_scope_map_inductive.md     # scope defs + boundary rules
├── tier_config.json                     # T1=50%, T2=30%, T3=20%
├── tier_labels.json                     # per-row tier + source labels
├── synthetic_tier_overrides.json        # 776 synthetic rows with intended tier + near_neighbor
```

CSV schema (both pos and neg):
```
sentence, verb_lemma, verb_token_idx, on_sense, wn_synsets, vn_class,
situation, match_path, source_file, sentence_idx, situation_count, needs_review
```

Hardware: Apple M4 Mac Mini, 24 GB unified memory, MPS backend.

---

## Task: Build the full training pipeline

Implement the following as modular Python scripts. Use `microsoft/deberta-v3-base` with NLI-pretrained weights. All scripts should be MPS-aware with CPU fallback.

---

### Script 1: `prepare_splits.py` — Data Loading, Pair Construction, and Train/Dev/Test Splitting

**1a. Load and merge all pos/neg CSVs.**

Read all 62 pos files and all 62 neg files. Each row already has a `situation` column. Add a `label` column: 1 for pos, 0 for neg.

**1b. Load or create ASC definition strings.**

You need a mapping from each of the 62 Situation names to a natural-language definition string. This is the second half of the cross-encoder input — its quality matters enormously. Check if a definitions file already exists at `asc_definitions.json`. If not, extract event type descriptions from `situation_scope_map_inductive.md` (each Situation entry has an "Event type" line) and also include the subject role and key participant structure. Write to `asc_definitions.json`. Format: `{"Motion": "An entity moves along a path from a source to a goal. The grammatical subject is the moving entity.", ...}`.

After extraction, print all 62 definitions for Josh's review before proceeding. The definition wording directly affects what the model learns — two Situations with similar-sounding definitions will be harder to discriminate regardless of training data quality.

**1c. Construct cross-encoder pairs.**

For each row, create a pair: `(sentence, asc_definition, label, target_situation)`.

For positive rows: `target_situation` = the row's `situation` column (this IS the gold Situation). `asc_definition` = definition for that Situation. `label = 1`.

For negative rows: `target_situation` = the Situation name extracted from the neg filename (e.g., `Carrying_neg.csv` → `Carrying`). This is the Situation the sentence is a negative FOR. `asc_definition` = definition for this target Situation. `label = 0`. The row's `situation` column is the DONOR (where the sentence originally came from) — preserve it as metadata but do not use it as the target.

**Sanity check**: verify that no sentence appears as both label=1 and label=0 for the SAME target_situation. A sentence can (and should) appear as positive for its own Situation and as negative for other Situations.

**1d. Attach tier metadata.**

Load `tier_labels.json` and join tier labels (T1/T2/T3) and source (mechanical/override) to the neg rows. This metadata is used for tier-stratified sampling and optional loss weighting, not as model input.

**1e. Generate 5-fold stratified cross-validation splits.**

Use `StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)`. Stratify by `(target_situation, label)`. For each fold, further verify tier distribution is roughly preserved (T1/T2/T3 counts per Situation per split should not deviate more than 20% from the expected proportion).

**Verb-lemma leakage check**: for each fold, verify no verb lemma appears in the test fold that doesn't also appear in the train fold. If any verb is test-only, swap that row into train and replace with a same-Situation, same-tier row from train.

Write 5 fold directories: `folds/fold_{0..4}/train.csv`, `folds/fold_{0..4}/dev.csv`, `folds/fold_{0..4}/test.csv`. For each fold, split the non-test portion 85/15 into train/dev. Columns: `sentence, asc_definition, label, target_situation, donor_situation, tier, source, match_path, verb_lemma`.

Print per-fold statistics: total rows, per-Situation counts, tier distribution.

---

### Script 2: `train_cross_encoder.py` — Fine-Tuning

**2a. Model setup.**

Load `microsoft/deberta-v3-base`. Check HuggingFace for `cross-encoder/nli-deberta-v3-base`; if it exists, use it as the initialization (NLI-pretrained weights give a head start on sentence-pair reasoning). Otherwise use the base model. Binary classification head on the `[CLS]` pooled representation.

**2b. Dataset and DataLoader.**

Custom PyTorch Dataset that tokenizes `(sentence, asc_definition)` pairs using the DeBERTa tokenizer with `max_length=384`, `truncation=True`, `padding='max_length'`. Return `input_ids`, `attention_mask`, `token_type_ids`, `label`. Also return `tier`, `source`, `match_path` as metadata tensors/strings for optional loss weighting (not fed to the model).

Verify truncation rate: count how many pairs exceed 384 subword tokens before truncation. If > 5%, consider increasing max_length. Log the count.

DataLoader with batch size 8 (the M4's 24GB unified memory is tight with DeBERTa at 384 tokens; start at 8, try 16 only if memory allows). Tier-aware sampling applies to NEG rows only: when constructing batches, sample negatives maintaining roughly 50/30/20 T1/T2/T3. Positive rows are sampled uniformly. If tier-aware batching is too complex, fall back to uniform random and note this.

**2c. 5-fold training loop.**

For each fold in `folds/fold_{0..4}/`:
- Load `train.csv`, `dev.csv`
- Re-initialize model from the same pretrained checkpoint (do NOT carry weights across folds)
- Train with:
  - Optimizer: AdamW, lr=2e-5, weight_decay=0.01
  - Scheduler: linear warmup over first 10% of steps, linear decay to 0
  - Max epochs: 5, early stopping on dev F1 (patience=2)
  - Gradient accumulation: 4 steps (effective batch size 32)
  - Mixed precision: use `torch.amp` autocast if MPS supports it for DeBERTa ops, otherwise fp32. Log which mode is active.
  - Every epoch: evaluate on dev set, log dev loss + macro F1
- Save best checkpoint per fold: `checkpoints/fold_{n}/deberta_asc_best.pt`
- Save per-epoch metrics: `checkpoints/fold_{n}/training_log.json`

After all 5 folds, print:
```
Fold  Best_epoch  Dev_loss  Dev_F1
0     ...         ...       ...
...
Mean              ...       ...
Std               ...       ...
```

Estimated wall time: ~45-60 min per fold, ~4-5 hours total. Designed to run overnight.

**2d. Optional: loss weighting.**

Accept a `--weight-synthetic` flag (default 0.7). When set, multiply the loss for rows where `match_path=synthetic` by this factor. Accept a `--weight-t1-override` flag (default 1.5). When set, multiply the loss for rows where `source=override` and `tier=T1` by this factor. These are override-tagged boundary-adjacent synthetic sentences; upweighting their loss concentrates training signal on the hardest boundaries.

**2e. Checkpointing.**

Per fold: save to `checkpoints/fold_{n}/deberta_asc_best.pt` with tokenizer. Save training curves to `checkpoints/fold_{n}/training_log.json`.

After all folds: save `checkpoints/cv_summary.json` with per-fold best epoch, dev loss, dev F1, and the mean/std across folds.

---

### Script 3: `evaluate.py` — Evaluation and Error Analysis

**3a. Aggregate across 5 folds.**

For each fold, load the best checkpoint and run on that fold's `test.csv`. Collect predictions across all 5 folds (each test row is scored exactly once since folds are non-overlapping). Report metrics on the combined test predictions.

**3b. Core metrics.**

Report:
- Overall accuracy, precision, recall, F1 (macro and weighted)
- Per-Situation precision, recall, F1, support — with mean and std across folds
- Per-tier accuracy breakdown (T1 vs T2 vs T3 negatives): measures whether the model discriminates hard boundaries
- Confusion patterns: for each Situation, list the top-3 most-confused Situations (where the model scores a negative pair highest)

**3c. Candidate-set-constrained evaluation.**

This is the real operating condition. For each test sentence:
1. Look up the verb lemma in `mappings_final_clean.csv` to get the candidate Situation set.
2. Score the sentence against ONLY those candidate Situations' definitions.
3. The prediction is the highest-scoring candidate.
4. Report constrained accuracy and F1 alongside the unconstrained metrics.

This directly measures pipeline-realistic performance, not theoretical 62-way discrimination.

**3d. Baseline comparison.**

Random baseline: for each test sentence, randomly select among the candidate ASCs for that verb (using `mappings_final_clean.csv`). Report the same constrained metrics. This is the "no classifier" baseline reflecting candidate retrieval alone.

**3e. Boundary-pair evaluation.**

For each shared-verb pair in the scope map, construct a balanced mini-test: all test rows using that shared verb, scored against both Situations' definitions. Report per-boundary accuracy.

Also: for test rows where `source=override` and `tier=T1`, compute accuracy separately. These are synthetic boundary-adjacent sentences with known `near_neighbor` — they directly measure whether the T1 synthetic data improved fine-grained discrimination.

**3f. Corpus vs. synthetic performance.**

Split test results by `match_path`: corpus-attested vs. synthetic. Report F1 for each. If synthetic rows perform significantly worse, flag as register mismatch evidence.

**3g. Error analysis output.**

Write `evaluation_report.md` with all metrics, tables, and a prioritized list of Situations needing attention, based on:
1. Per-Situation F1 < 0.7 (averaged across folds)
2. T1 accuracy < 60%
3. Boundary-pair accuracy < 70%
4. High variance across folds (std F1 > 0.15 for a Situation)
5. Verb-monoculture Situations (Payment, Constrain, Possession) showing verb-identity shortcuts (check if the model scores near 1.0 for ANY pair containing the monoculture verb regardless of definition)

---

### Script 4: `inference.py` — End-to-End Pipeline Demo

**4a. Full pipeline for a single input sentence.**

```
Input:  "The artist carved the cherubim into the iconostasis."
Step 1: spaCy dep parse → ROOT = "carved", lemma = "carve"
Step 2: Look up "carve" in mappings_final_clean.csv → candidate Situations
        (The mappings CSV already encodes the full WN→VN→Situation chain.
         No SemLink lookup needed at inference — just match verb_lemma
         against the mappings to get candidate Situations.)
Step 3: Load ASC definitions for each candidate Situation
Step 4: Score [sentence, ASC_def] for each candidate → select highest
Output: Situation = "Image_Creation", score = 0.94
        Candidates: Image_Creation=0.94, Cause_Creation=0.31, ...
```

Accept sentences from stdin, as a `--sentence` argument, or from a file (`--input-file`). Always print the full candidate set with scores, sorted descending.

**4b. Batch mode.**

Accept a CSV with a `sentence` column. Run the pipeline for each row. Output CSV with columns: `sentence, verb_lemma, predicted_situation, score, candidate_count, all_scores_json`.

**4c. Use the best single fold or an ensemble.**

Accept `--fold N` to use a specific fold's checkpoint, or `--ensemble` to average scores across all 5 folds' checkpoints. Default: use the fold with the highest dev F1 from `cv_summary.json`.

---

## Implementation Notes

- Python 3.11+. Dependencies: `torch`, `transformers`, `tokenizers`, `spacy`, `nltk`, `scikit-learn`, `pandas`, `tqdm`.
- All scripts should accept `--data-dir` to override the base path.
- Use `logging` not `print` for status messages.
- Include a `requirements.txt`.
- Seed everything (torch, numpy, random) with `--seed` (default 42) for reproducibility.
- If MPS causes numerical issues (known with some operations), fall back to CPU for those ops and log a warning.
- The 62 Situations are the label space. They are NOT balanced in the pos files (some have 50+, some have fewer). The neg files are also variable. The model should handle this gracefully; class weighting in the loss is one option but not required if the cross-encoder pair formulation already handles it (each pair is binary: match or not).

## What NOT to Do

- Do not feed synset strings, VN class names, or tier labels as model input. Only `sentence` and `asc_definition` enter the encoder.
- Do not use the `situation` column in neg CSVs as the target Situation. The target Situation is the neg FILE's name. The `situation` column is the donor (where the sentence came from).
- Do not flatten the tiered neg structure into uniform sampling. The whole point of T1/T2/T3 is to control difficulty distribution during training.
- Do not skip the verb-lemma leakage check in the train/test split. If a verb appears only in test, the model has never seen that verb's usage patterns and the evaluation confounds ASC discrimination with unknown-verb generalization.
