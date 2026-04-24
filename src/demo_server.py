#!/usr/bin/env python3
"""FastAPI server for live ASC classification demo."""

import json
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

import torch
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent                   # src/
PROJECT_ROOT = HERE.parent                               # repo root
DATA_DIR = PROJECT_ROOT / "data"                         # asc_definitions, verb_candidates
RESULTS_DIR = PROJECT_ROOT / "results"                   # checkpoints, cv_summary

# ---------- globals populated at startup ----------
model = None
tokenizer = None
nlp = None
verb_candidates: dict[str, list[str]] = {}
asc_definitions: dict[str, str] = {}
device = None


def load_resources():
    global model, tokenizer, nlp, verb_candidates, asc_definitions, device
    t0 = time.time()

    # Device
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    log.info("Device: %s", device)

    # spaCy
    import spacy
    nlp = spacy.load("en_core_web_sm")
    log.info("spaCy loaded")

    # Definitions and candidates
    asc_definitions = json.loads((DATA_DIR / "asc_definitions.json").read_text())
    verb_candidates = json.loads((DATA_DIR / "verb_candidates.json").read_text())
    log.info("Loaded %d definitions, %d verb entries", len(asc_definitions), len(verb_candidates))

    # Model — best fold from cv_summary.json
    cv_summary = json.loads((RESULTS_DIR / "cv_summary.json").read_text())
    best_fold = cv_summary.get("best_fold", 4)
    ckpt = RESULTS_DIR / "checkpoints" / f"fold_{best_fold}" / "deberta_asc_best"

    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tokenizer = AutoTokenizer.from_pretrained(ckpt)
    model = AutoModelForSequenceClassification.from_pretrained(ckpt)
    model.to(device)
    model.eval()

    log.info("Model loaded (fold %d) in %.1fs", best_fold, time.time() - t0)


@asynccontextmanager
async def lifespan(app):
    load_resources()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


# ---------- request / response ----------
class ClassifyRequest(BaseModel):
    sentence: str


@app.post("/classify")
def classify(req: ClassifyRequest):
    sentence = req.sentence.strip()
    if not sentence:
        return {"error": "Empty sentence.", "sentence": sentence}

    # 1. Parse verb
    t_parse = time.time()
    doc = nlp(sentence)
    verb_token = None
    for token in doc:
        if token.dep_ == "ROOT" and token.pos_ in ("VERB", "AUX"):
            verb_token = token
            break
    if verb_token is None:
        for token in doc:
            if token.pos_ == "VERB":
                verb_token = token
                break
    if verb_token is None:
        return {"error": "No verb found in sentence.", "sentence": sentence}

    lemma = verb_token.lemma_
    verb_text = verb_token.text
    parse_ms = round((time.time() - t_parse) * 1000, 1)

    # 2. Candidate lookup
    fallback = False
    candidates = verb_candidates.get(lemma)
    if candidates is None:
        candidates = list(asc_definitions.keys())
        fallback = True
    candidates = [c for c in candidates if c in asc_definitions]
    if not candidates:
        candidates = list(asc_definitions.keys())
        fallback = True

    # 3. Score
    t_score = time.time()
    sents = [sentence] * len(candidates)
    defs = [asc_definitions[c] for c in candidates]

    enc = tokenizer(
        sents, defs,
        max_length=384, truncation=True, padding=True,
        return_tensors="pt",
    )
    enc = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        logits = model(**enc).logits
    probs = torch.softmax(logits, dim=-1)[:, 1].cpu().tolist()
    score_ms = round((time.time() - t_score) * 1000, 1)

    # 4. Build response
    results = sorted(
        [
            {
                "situation": sit,
                "score": round(p, 4),
                "definition": asc_definitions[sit],
            }
            for sit, p in zip(candidates, probs)
        ],
        key=lambda x: -x["score"],
    )

    return {
        "sentence": sentence,
        "verb": verb_text,
        "lemma": lemma,
        "candidate_count": len(candidates),
        "fallback": fallback,
        "results": results,
        "parse_time_ms": parse_ms,
        "score_time_ms": score_ms,
    }


@app.get("/")
def index():
    return FileResponse(HERE / "demo.html", media_type="text/html")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
