# Fine-Tuning a Bidirectional Cross-Encoder for Verbal Clause Construction Classification

Final project for CSPB 3832 Natural Language Processing, Spring 2026 (Prof. Curry Guinn), by Josh Falconer.

> This project fine-tunes a DeBERTa-v3-base cross-encoder to classify verbal clauses by their argument structure construction, identifying which of 62 event structures best captures a sentence's meaning. The 62 constructions derive from Croft's force-dynamic event model and Kalm's extension to social verbs, each corresponding to a distinct causal chain configuration. The training dataset of 13,186 labeled sentence-definition pairs was built from manually curated examples drawn from OntoNotes, VerbNet, and FrameNet, supplemented by synthetic generation, and grounded in inductively defined scope maps. Both positive and negative examples were tiered by difficulty, with half targeting the hardest boundary cases between neighboring constructions. The classifier achieves 94.4% macro F1 and 96.7% constrained accuracy under pipeline-realistic conditions. The tiered training data design proved to be the decisive factor in discriminating among closely related constructions.

**Research question.** Can a fine-tuned cross-encoder reliably learn to disambiguate between closely related verbal clause constructions?

**Headline results.** Macro F1 94.4%, accuracy 95.3%, and constrained accuracy 96.7% (+5.9 percentage points over the random baseline). Per-tier accuracy: T1 (same-cluster hard) 94.4%, T2 (same-realm) 97.4%, T3 (cross-realm) 93.0%. The full per-construction breakdown is in [results/evaluation_report.md](results/evaluation_report.md).

**Primary document.** [Final Project Report.pdf](Final%20Project%20Report.pdf) is the submitted write-up. This README is a navigation and reproduction guide for the code and data behind it.

---

## Repository layout

```
.
├── README.md
├── Final Project Report.pdf               The 9-page submitted report.
├── LARGE_FILES.md                         Artifacts excluded from git (weights, logs, intermediates).
├── requirements.txt                       Python dependencies.
│
├── src/                                   Pipeline code.
│   ├── prepare_splits.py                    Build pairs, verb_candidates, and 5-fold CV splits.
│   ├── train_cross_encoder.py               Fine-tune DeBERTa-v3-base.
│   ├── evaluate.py                          Metrics, constrained accuracy, per-construction F1.
│   ├── inference.py                         CLI sentence classification.
│   ├── demo_server.py                       FastAPI server for the demo UI.
│   ├── demo.html                            Demo frontend served by demo_server.
│   └── extract_training_data.py             Phase-I OntoNotes extractor (kept for provenance).
│
├── data/                                   Training data and lexical resources.
│   ├── situation_splits/
│   │   ├── positives/                       62 *_pos.csv files, 3,886 rows.
│   │   └── negatives/                       62 *_neg.csv files, 9,300 rows.
│   ├── asc_definitions.json                 62 constructions with natural-language definitions.
│   ├── situation_definitions.json           Short labels for the demo UI.
│   ├── verb_candidates.json                 verb_lemma to candidate constructions (inference lookup).
│   ├── tier_config.json                     T1/T2/T3 ratios (50/30/20), target 50 per construction.
│   ├── tier_labels.json                     Per-positive-row tier and source labels.
│   ├── synthetic_tier_overrides.json        Intended-tier map for synthetic positives.
│   └── mappings_final_clean.csv             Hand-curated verb-to-construction lexicon (3,258 verbs).
│
├── docs/                                   Deeper documentation.
│   ├── DATASET_BUILD_JOURNEY.md             Full narrative: phases, decisions, and rationale.
│   ├── situation_scope_map_inductive.md     62 scope entries and 39 shared-verb boundary rules.
│   ├── cross_encoder_implementation_prompt.md
│   ├── tier_census.md                       Per-construction tier counts against targets.
│   └── TODO_NEXT_ROUND.md                   Post-mortem and next-round backlog.
│
├── results/                                Evaluation artifacts.
│   ├── evaluation_report.md                 Overall metrics, per-construction F1, per-tier accuracy, corpus vs. synthetic.
│   ├── cv_summary.json                      Per-fold dev F1 and training arguments.
│   └── checkpoints/                         Trained model weights (not tracked). See LARGE_FILES.md.
│
└── presentation/                            Final deck and PDF builder.
    ├── Final Project Presentation Slides.pdf
    ├── Final Project Presentation Slides.html   Reveal.js source.
    ├── build_pdf.py                             Native-PDF generator (ReportLab).
    └── fonts/                                   Source Serif 4 and Source Sans 3 for build_pdf.py.
```

## How the report maps onto this repository

Each section of the report is grounded in specific artifacts in this repo. The table below points from a report section to the files that back it.

| Report section | Where to look |
|---|---|
| Abstract and Introduction (thesis and motivation) | [Final Project Report.pdf](Final%20Project%20Report.pdf); overview in [docs/DATASET_BUILD_JOURNEY.md](docs/DATASET_BUILD_JOURNEY.md) |
| Related Work (Croft, Kalm, Levin, Das et al., Devlin et al.) | Bibliography in the report; primary citations are also listed at the bottom of this README |
| Data (13,186 pairs and tiered design) | [data/situation_splits/](data/situation_splits/) (positives and negatives); [data/tier_config.json](data/tier_config.json); [data/tier_labels.json](data/tier_labels.json); summary in [docs/tier_census.md](docs/tier_census.md) |
| Data (inductively defined scope maps) | [docs/situation_scope_map_inductive.md](docs/situation_scope_map_inductive.md): 62 scope entries, 39 shared-verb boundary rules, 7 flagged ambiguities |
| Methodology (pipeline stages) | [src/inference.py](src/inference.py) for spaCy, lemma lookup, candidate retrieval, and cross-encoder scoring; [src/prepare_splits.py](src/prepare_splits.py) for stratified folds; [src/train_cross_encoder.py](src/train_cross_encoder.py) for AdamW, loss weighting, and early stopping |
| Methodology (three experimental phases) | [docs/DATASET_BUILD_JOURNEY.md](docs/DATASET_BUILD_JOURNEY.md), Phases I through V |
| Results (headline metrics and per-tier accuracy) | [results/evaluation_report.md](results/evaluation_report.md); per-fold metrics and training arguments in [results/cv_summary.json](results/cv_summary.json) |
| Results (demo examples for "hold" and "look") | [src/demo_server.py](src/demo_server.py); [src/demo.html](src/demo.html); slides in [presentation/Final Project Presentation Slides.pdf](presentation/Final%20Project%20Presentation%20Slides.pdf) |
| Discussion (Emotion pair and causative/inchoative weaknesses) | [results/evaluation_report.md](results/evaluation_report.md), per-construction section; training-data gap documented in [docs/tier_census.md](docs/tier_census.md), T1 columns for Emotion_(exp. subj.) and Emotion_(stim. subj.) |
| Future Work (reconcile candidate lookup with full lexicon) | [data/mappings_final_clean.csv](data/mappings_final_clean.csv) with 3,258 verbs; plan in [docs/TODO_NEXT_ROUND.md](docs/TODO_NEXT_ROUND.md) |

---

## Prerequisites

The committed repo is self-contained for the core pipeline, but a few pieces are not tracked and must be supplied before running. They are listed in the order you will encounter them.

### 1. Python environment and the spaCy English model

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Python 3.10 or later. Every script in the pipeline depends on this environment. If you train on a GPU or on Apple MPS, install a `torch` build that matches your hardware. CPU training is possible but impractical at this data scale for a DeBERTa cross-encoder.

### 2. Fold splits

`data/folds/` is auto-generated and not tracked. Regenerate it once with:

```bash
python src/prepare_splits.py
```

This reads `data/situation_splits/`, `docs/situation_scope_map_inductive.md`, and `data/tier_labels.json`, then writes `data/folds/` and refreshes `data/verb_candidates.json`. It completes in seconds.

### 3. Trained model weights

The five fine-tuned DeBERTa-v3-base checkpoints (about 3.56 GB total) are not in the repo. `evaluate.py`, `inference.py`, and `demo_server.py` all need them.

There are two ways to obtain them.

Train from scratch, which takes roughly 17 hours on an Apple M4 Mac Mini with MPS, or proportionally on a GPU:

```bash
python src/train_cross_encoder.py
```

This writes `results/checkpoints/fold_0/` through `fold_4/` and `results/cv_summary.json`.

Or download a hosted copy. A link will be added to [LARGE_FILES.md](LARGE_FILES.md) once the weights are uploaded. Until then, training from scratch is the only path.

Without checkpoints, only `prepare_splits.py` and `presentation/build_pdf.py` can run.

### 4. OntoNotes 5.0

[src/extract_training_data.py](src/extract_training_data.py) requires the OntoNotes 5.0 corpus (LDC2013T19). OntoNotes is licensed and cannot be redistributed, so it is not in the repo. Obtain it from the Linguistic Data Consortium.

This is only required for reproducing the Phase-I experiment described in the report's Methodology and Discussion sections. The final training data is already curated and committed in [data/situation_splits/](data/situation_splits/), so the core pipeline does not need OntoNotes. The extractor is kept for provenance.

### 5. Intermediate curation CSVs

About 110 MB of intermediate-stage CSVs (auto_resolved.csv, edge_cases.csv, review_sample.csv, training_data_flagged.csv, and others) document the human-in-the-loop curation that built `data/situation_splits/`. They are not tracked and they are not reproducible from code. They are the trail of a judgment-driven process, and their absence does not block anything. The authoritative final dataset is already in the repo. For the narrative, see [LARGE_FILES.md](LARGE_FILES.md) and [docs/DATASET_BUILD_JOURNEY.md](docs/DATASET_BUILD_JOURNEY.md).

---

## Reproducing the pipeline end to end

Once the prerequisites above are in place:

```bash
python src/prepare_splits.py       # writes data/folds/ and data/verb_candidates.json
python src/train_cross_encoder.py  # writes results/checkpoints/fold_*/ and results/cv_summary.json (about 17 h)
python src/evaluate.py             # writes results/evaluation_report.md
```

Every script takes `--data-dir` and, where applicable, `--results-dir` flags. The defaults resolve relative to the repo root via `Path(__file__)`, so no absolute paths are hardcoded.

## Running inference on a single sentence

```bash
python src/inference.py --sentence "The old barn holds about forty head of cattle."
```

Expected output: `hold` classified as Capacity with a score of 0.994, followed by the full candidate ranking.

## Running the interactive demo

```bash
python src/demo_server.py
```

Then open http://localhost:8000/ in a browser.

## Rebuilding the presentation PDF

```bash
python presentation/build_pdf.py
```

This writes `presentation/Final Project Presentation Slides.pdf`, 16 pages at 1920×1080.

---

## Where to start reading

1. [Final Project Report.pdf](Final%20Project%20Report.pdf). The 9-page submitted report.
2. [docs/DATASET_BUILD_JOURNEY.md](docs/DATASET_BUILD_JOURNEY.md). The full build narrative, including what went wrong, what got pivoted, and what the final artifacts are.
3. [docs/situation_scope_map_inductive.md](docs/situation_scope_map_inductive.md). The 62 construction definitions and the boundary rules that govern the training data.
4. [results/evaluation_report.md](results/evaluation_report.md). Headline numbers and per-construction F1.
5. [presentation/Final Project Presentation Slides.pdf](presentation/Final%20Project%20Presentation%20Slides.pdf). The submitted deck.

## Primary citations

- Croft, W. (2012). *Verbs: Aspect and Causal Structure*. Oxford University Press.
- Croft, W., Kalm, P., Regan, M., Vigus, M., Lee, S., & Peverada, C. (2021). *Developing language-independent event representations that are inferable from linguistic expressions in large text corpora* (Final Technical Report). Defense Threat Reduction Agency, University of New Mexico.
- Croft, W. (2022). *Morphosyntax: Constructions of the World's Languages*. Cambridge University Press.
- Kalm, P. (2022). *Social Verbs: A Force-Dynamic Analysis* [Doctoral dissertation, University of New Mexico].
- Goldberg, A. E. (1995). *Constructions: A Construction Grammar Approach to Argument Structure*. University of Chicago Press.
- Levin, B. (1993). *English Verb Classes and Alternations*. University of Chicago Press.
- Das, D., Chen, D., Martins, A. F. T., Schneider, N., & Smith, N. A. (2014). Frame-semantic parsing. *Computational Linguistics*, 40(1), 9–56.
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. *NAACL-HLT 2019*.
- Bowman, S. R., Angeli, G., Potts, C., & Manning, C. D. (2015). A large annotated corpus for learning natural language inference. *EMNLP 2015*.

The complete bibliography is in the report.
