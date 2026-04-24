#!/usr/bin/env python3
"""Script 2: Fine-tune DeBERTa-v3-base cross-encoder for ASC classification."""

import argparse
import csv
import json
import logging
import os
import random
import time
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from sklearn.metrics import f1_score
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent                   # src/
PROJECT_ROOT = HERE.parent                               # repo root
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"                 # folds live here
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "results"           # checkpoints + cv_summary go here


def seed_everything(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def get_device():
    if torch.backends.mps.is_available():
        log.info("Using MPS (Apple Silicon) backend")
        return torch.device("mps")
    elif torch.cuda.is_available():
        log.info("Using CUDA backend")
        return torch.device("cuda")
    else:
        log.info("Using CPU backend")
        return torch.device("cpu")


class ASCPairDataset(Dataset):
    """Cross-encoder dataset for (sentence, asc_definition) pairs."""

    def __init__(self, csv_path: Path, tokenizer, max_length: int = 384):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))
        self._check_truncation()

    def _check_truncation(self):
        truncated = 0
        for r in self.rows:
            enc = self.tokenizer(
                r["sentence"], r["asc_definition"],
                add_special_tokens=True, truncation=False,
            )
            if len(enc["input_ids"]) > self.max_length:
                truncated += 1
        pct = 100 * truncated / max(1, len(self.rows))
        if pct > 5:
            log.warning("%.1f%% of pairs (%d/%d) exceed max_length=%d — consider increasing",
                        pct, truncated, len(self.rows), self.max_length)
        else:
            log.info("Truncation rate: %.1f%% (%d/%d exceed %d tokens)",
                     pct, truncated, len(self.rows), self.max_length)

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        r = self.rows[idx]
        enc = self.tokenizer(
            r["sentence"], r["asc_definition"],
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )
        item = {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "label": torch.tensor(int(r["label"]), dtype=torch.long),
        }
        if "token_type_ids" in enc:
            item["token_type_ids"] = enc["token_type_ids"].squeeze(0)

        # Metadata for optional loss weighting (not model input)
        item["match_path"] = r.get("match_path", "")
        item["tier"] = r.get("tier", "")
        item["source"] = r.get("source", "")
        return item


def collate_fn(batch):
    """Custom collate that handles string metadata fields."""
    result = {}
    tensor_keys = ["input_ids", "attention_mask", "label"]
    if "token_type_ids" in batch[0]:
        tensor_keys.append("token_type_ids")
    for k in tensor_keys:
        result[k] = torch.stack([b[k] for b in batch])
    for k in ["match_path", "tier", "source"]:
        result[k] = [b[k] for b in batch]
    return result


def compute_sample_weights(batch, weight_synthetic: float, weight_t1_override: float):
    """Compute per-sample loss weights from metadata."""
    weights = torch.ones(len(batch["label"]), dtype=torch.float32)
    for i in range(len(batch["label"])):
        if batch["match_path"][i] == "synthetic":
            weights[i] *= weight_synthetic
        if batch["source"][i] == "override" and batch["tier"][i] == "T1":
            weights[i] *= weight_t1_override
    return weights


def evaluate(model, dataloader, device, criterion):
    """Evaluate model on a dataset. Returns loss and macro F1."""
    model.eval()
    all_preds = []
    all_labels = []
    total_loss = 0.0
    n_batches = 0

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)
            kwargs = {"input_ids": input_ids, "attention_mask": attention_mask}
            if "token_type_ids" in batch:
                kwargs["token_type_ids"] = batch["token_type_ids"].to(device)

            outputs = model(**kwargs)
            logits = outputs.logits
            loss = criterion(logits, labels)
            total_loss += loss.item()
            n_batches += 1

            preds = torch.argmax(logits, dim=-1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.cpu().numpy())

    avg_loss = total_loss / max(1, n_batches)
    f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
    return avg_loss, f1


def train_fold(
    fold_dir: Path,
    checkpoint_dir: Path,
    model_name: str,
    device: torch.device,
    args,
):
    """Train one fold. Returns best dev F1 and epoch."""
    from transformers import AutoTokenizer, AutoModelForSequenceClassification

    log.info("Loading model: %s", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=2, ignore_mismatched_sizes=True
    )
    log.info("Classification head reinitialized for 2 labels (NLI checkpoint has 3)")
    model.to(device)

    train_ds = ASCPairDataset(fold_dir / "train.csv", tokenizer, args.max_length)
    dev_ds = ASCPairDataset(fold_dir / "dev.csv", tokenizer, args.max_length)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True,
                              collate_fn=collate_fn, num_workers=0)
    dev_loader = DataLoader(dev_ds, batch_size=args.batch_size * 2, shuffle=False,
                            collate_fn=collate_fn, num_workers=0)

    optimizer = AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    total_steps = len(train_loader) * args.epochs // args.grad_accum
    warmup_steps = int(total_steps * 0.1)

    from transformers import get_linear_schedule_with_warmup
    scheduler = get_linear_schedule_with_warmup(optimizer, warmup_steps, total_steps)

    criterion = torch.nn.CrossEntropyLoss(reduction="none")

    # Check MPS float16 support
    use_amp = False
    if device.type == "cuda":
        use_amp = True
        log.info("Using AMP (CUDA float16)")
    else:
        log.info("AMP disabled (MPS/CPU — using fp32)")

    scaler = torch.amp.GradScaler(enabled=use_amp)

    best_f1 = -1.0
    best_epoch = -1
    patience_counter = 0
    training_log = []

    for epoch in range(args.epochs):
        model.train()
        epoch_loss = 0.0
        optimizer.zero_grad()
        step = 0

        pbar = tqdm(train_loader, desc=f"Epoch {epoch}", leave=False)
        for batch_i, batch in enumerate(pbar):
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)
            kwargs = {"input_ids": input_ids, "attention_mask": attention_mask}
            if "token_type_ids" in batch:
                kwargs["token_type_ids"] = batch["token_type_ids"].to(device)

            with torch.amp.autocast(device_type=device.type, enabled=use_amp):
                outputs = model(**kwargs)
                per_sample_loss = criterion(outputs.logits, labels)

                # Apply optional loss weighting
                weights = compute_sample_weights(batch, args.weight_synthetic, args.weight_t1_override)
                weights = weights.to(device)
                loss = (per_sample_loss * weights).mean() / args.grad_accum

            scaler.scale(loss).backward()
            epoch_loss += loss.item() * args.grad_accum

            if (batch_i + 1) % args.grad_accum == 0:
                scaler.step(optimizer)
                scaler.update()
                scheduler.step()
                optimizer.zero_grad()
                step += 1

            pbar.set_postfix(loss=f"{loss.item() * args.grad_accum:.4f}")

        avg_train_loss = epoch_loss / max(1, len(train_loader))

        dev_loss, dev_f1 = evaluate(model, dev_loader, device, torch.nn.CrossEntropyLoss())

        entry = {
            "epoch": epoch,
            "train_loss": round(avg_train_loss, 5),
            "dev_loss": round(dev_loss, 5),
            "dev_f1": round(dev_f1, 5),
        }
        training_log.append(entry)
        log.info("Epoch %d: train_loss=%.4f dev_loss=%.4f dev_F1=%.4f",
                 epoch, avg_train_loss, dev_loss, dev_f1)

        if dev_f1 > best_f1:
            best_f1 = dev_f1
            best_epoch = epoch
            patience_counter = 0
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            model.save_pretrained(checkpoint_dir / "deberta_asc_best")
            tokenizer.save_pretrained(checkpoint_dir / "deberta_asc_best")
            log.info("  Saved best checkpoint (F1=%.4f)", dev_f1)
        else:
            patience_counter += 1
            if patience_counter >= args.patience:
                log.info("  Early stopping at epoch %d (patience=%d)", epoch, args.patience)
                break

    with open(checkpoint_dir / "training_log.json", "w") as f:
        json.dump(training_log, f, indent=2)

    return best_epoch, best_f1, training_log[-1]["dev_loss"]


def main():
    parser = argparse.ArgumentParser(description="Train DeBERTa cross-encoder for ASC classification")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR,
                        help=f"Directory holding folds/ (default: {DEFAULT_DATA_DIR})")
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR,
                        help=f"Directory for checkpoints/ and cv_summary.json "
                             f"(default: {DEFAULT_RESULTS_DIR})")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--weight-decay", type=float, default=0.01)
    parser.add_argument("--grad-accum", type=int, default=4)
    parser.add_argument("--max-length", type=int, default=384)
    parser.add_argument("--patience", type=int, default=2)
    parser.add_argument("--weight-synthetic", type=float, default=0.7)
    parser.add_argument("--weight-t1-override", type=float, default=1.5)
    parser.add_argument("--model-name", type=str, default=None,
                        help="HF model name. Auto-selects NLI-pretrained if available.")
    args = parser.parse_args()

    seed_everything(args.seed)
    device = get_device()

    # Auto-select model: prefer NLI-pretrained
    if args.model_name is None:
        try:
            from transformers import AutoConfig
            AutoConfig.from_pretrained("cross-encoder/nli-deberta-v3-base")
            args.model_name = "cross-encoder/nli-deberta-v3-base"
            log.info("Using NLI-pretrained: %s", args.model_name)
        except Exception:
            args.model_name = "microsoft/deberta-v3-base"
            log.info("NLI-pretrained not available, using base: %s", args.model_name)

    folds_dir = args.data_dir / "folds"
    checkpoints_dir = args.results_dir / "checkpoints"

    fold_results = []
    for fold_i in range(5):
        fold_dir = folds_dir / f"fold_{fold_i}"
        if not fold_dir.exists():
            log.warning("Fold %d not found at %s, skipping", fold_i, fold_dir)
            continue

        log.info("=" * 60)
        log.info("FOLD %d", fold_i)
        log.info("=" * 60)
        ckpt_dir = checkpoints_dir / f"fold_{fold_i}"
        t0 = time.time()
        best_epoch, best_f1, dev_loss = train_fold(fold_dir, ckpt_dir, args.model_name, device, args)
        elapsed = time.time() - t0
        fold_results.append({
            "fold": fold_i,
            "best_epoch": best_epoch,
            "dev_loss": round(dev_loss, 5),
            "dev_f1": round(best_f1, 5),
            "wall_time_min": round(elapsed / 60, 1),
        })
        log.info("Fold %d complete: best_epoch=%d dev_F1=%.4f (%.1f min)",
                 fold_i, best_epoch, best_f1, elapsed / 60)

    # Summary
    print("\n" + "=" * 60)
    print(f"{'Fold':>4}  {'Best_epoch':>10}  {'Dev_loss':>8}  {'Dev_F1':>8}  {'Time':>8}")
    for r in fold_results:
        print(f"{r['fold']:>4}  {r['best_epoch']:>10}  {r['dev_loss']:>8.4f}  {r['dev_f1']:>8.4f}  {r['wall_time_min']:>6.1f}m")
    if fold_results:
        f1s = [r["dev_f1"] for r in fold_results]
        losses = [r["dev_loss"] for r in fold_results]
        print(f"{'Mean':>4}  {'':>10}  {np.mean(losses):>8.4f}  {np.mean(f1s):>8.4f}")
        print(f"{'Std':>4}  {'':>10}  {np.std(losses):>8.4f}  {np.std(f1s):>8.4f}")

    # Save CV summary
    cv_summary = {
        "folds": fold_results,
        "mean_dev_f1": round(float(np.mean(f1s)), 5) if fold_results else 0,
        "std_dev_f1": round(float(np.std(f1s)), 5) if fold_results else 0,
        "best_fold": int(np.argmax(f1s)) if fold_results else 0,
        "args": {k: str(v) for k, v in vars(args).items()},
    }
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    cv_summary_path = args.results_dir / "cv_summary.json"
    args.results_dir.mkdir(parents=True, exist_ok=True)
    with open(cv_summary_path, "w") as f:
        json.dump(cv_summary, f, indent=2)
    log.info("CV summary saved to %s", cv_summary_path)


if __name__ == "__main__":
    main()
