# Large Files (set aside; not tracked in git)

This repository excludes a handful of artifacts that exceed GitHub's practical size limits. Paths below are relative to the repo root.

## Trained model checkpoints — ~3.56 GB

Five fine-tuned DeBERTa-v3-base checkpoints, one per cross-validation fold, each ~712 MB:

```
results/checkpoints/fold_0/deberta_asc_best/
results/checkpoints/fold_1/deberta_asc_best/
results/checkpoints/fold_2/deberta_asc_best/
results/checkpoints/fold_3/deberta_asc_best/
results/checkpoints/fold_4/deberta_asc_best/
```

Each directory contains the standard Hugging Face artifacts (`config.json`, `model.safetensors`, `tokenizer.json`, etc.).

Per-fold metrics and training arguments are recorded in [results/cv_summary.json](results/cv_summary.json), which *is* tracked.

**To regenerate** (Apple M4 Mac Mini, 24 GB, MPS — ~17 hours for all five folds):

```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python src/prepare_splits.py        # writes data/folds/ + data/verb_candidates.json
python src/train_cross_encoder.py   # writes results/checkpoints/fold_*/
python src/evaluate.py              # writes results/evaluation_report.md
```

A hosted copy of the checkpoints will be linked here when uploaded.

## Auto-generated fold splits — ~20 MB

`data/folds/` (train.csv, dev.csv, test.csv per fold) is deterministically regenerable from `data/situation_splits/` via `src/prepare_splits.py` (seed fixed in the script). Not tracked; regenerate as above.

## Raw training logs — ~4.8 MB

The full fold-by-fold training trace (4.7 MB) and the evaluation run trace (89 KB) are not tracked. Headline metrics are distilled in [results/evaluation_report.md](results/evaluation_report.md) and [results/cv_summary.json](results/cv_summary.json).

## Intermediate curation artifacts — ~110 MB combined

CSVs that document intermediate stages of the data-curation workflow (auto-resolved extractions, flagged multi-Situation rows, review samples, etc.) are not tracked. The authoritative final training data is in [data/situation_splits/](data/situation_splits/); the intermediate trail is summarized in [docs/DATASET_BUILD_JOURNEY.md](docs/DATASET_BUILD_JOURNEY.md).

## Reference PDFs — ~30 MB

Copyrighted Croft (2012, 2021) and Kalm (2022) PDF excerpts consulted during scope-map induction are not tracked. Citations are in [docs/DATASET_BUILD_JOURNEY.md](docs/DATASET_BUILD_JOURNEY.md).
