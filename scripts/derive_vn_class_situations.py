"""Workstream 1, task 1.2 — create the 81 new Situations from missing VN classes.

For each VN 3.4 top-level class absent from the workbook, this script:

  1. Parses the local VerbNet 3.4 XML to extract member verbs, themroles,
     and an example sentence (when present).
  2. Generates a v1.0-style Situation name (Title_Case_With_Underscores)
     and a one-sentence definition that mirrors the prose style of the
     existing data/asc_definitions.json entries.
  3. Writes:
       a) Updated data/asc_definitions.json (62 -> 143 keys).
       b) data/vn_class_derived_lexicon.csv — a parallel
          (Verb, VerbNet Class, Situation Domain, Situation, Polysemy) file
          analogous to data/situation_shapes_workbook.csv but for the 81
          new Situations. The loader concatenates this with the workbook.
       c) Empty _pos.csv and _neg.csv stubs in data/situation_splits/.
       d) data/vn_class_derived_situations.json — full metadata
          (themroles, frames, vn_class_id) for editorial review.

NFKC normalization applied throughout. Per the v2.0 plan, scope-map
entries for these 81 are deferred to task 1.6.

Usage:
    python scripts/derive_vn_class_situations.py [--dry-run]
"""

import argparse
import csv
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

REPO         = Path(__file__).resolve().parents[1]
WORKBOOK_CSV = REPO / "data" / "situation_shapes_workbook.csv"
VN_DIR       = Path("/Users/joshfalconer/Documents/Linguistic data/verbnet/verbnet3.4")
ASC_JSON     = REPO / "data" / "asc_definitions.json"
LEXICON_CSV  = REPO / "data" / "vn_class_derived_lexicon.csv"
META_JSON    = REPO / "data" / "vn_class_derived_situations.json"
POS_DIR      = REPO / "data" / "situation_splits" / "positives"
NEG_DIR      = REPO / "data" / "situation_splits" / "negatives"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--dry-run", action="store_true",
                    help="Print what would be written without modifying files.")
args = parser.parse_args()


def norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s)


def top_level(class_id: str) -> str:
    parts = class_id.split("-")
    return f"{parts[0]}-{parts[1]}" if len(parts) >= 2 else class_id


def situation_name_from_class(class_id: str) -> str:
    """leave-51.2 -> 'Leave'; calibratable_cos-45.6.1 -> 'Calibratable_Cos';
    body_internal_motion-49 -> 'Body_Internal_Motion'.
    """
    root = class_id.split("-")[0]
    parts = root.split("_")
    return "_".join(p.capitalize() for p in parts)


def themrole_summary(themroles: list[str]) -> tuple[str, str]:
    """Given the list of themrole types for the class (top-level + subclasses
    aggregated), return (subject_role_phrase, definition_lead)."""
    role_set = set(themroles)
    # Pick a primary subject role with a simple heuristic preference order.
    preferred = ["Agent", "Causer", "Experiencer", "Theme", "Patient",
                 "Stimulus", "Source", "Goal", "Pivot", "Recipient",
                 "Beneficiary", "Instrument", "Location", "Topic"]
    primary = next((r for r in preferred if r in role_set), None)
    if not primary and themroles:
        primary = themroles[0]

    others = [r for r in themroles if r != primary]
    if primary and others:
        lead = f"{primary} acts upon {', '.join(others[:3])}"
    elif primary:
        lead = f"{primary} engages in the named event"
    else:
        lead = "Participant engages in the named event"
    subject_phrase = primary.lower() if primary else "primary participant"
    return subject_phrase, lead


def first_example(root: ET.Element) -> str | None:
    """Return the first FRAME EXAMPLE text encountered anywhere in the class."""
    for ex in root.iter("EXAMPLE"):
        text = (ex.text or "").strip()
        if text:
            return text
    return None


def parse_class_xml(xml_path: Path) -> dict:
    """Extract metadata for one VerbNet XML file (top-level class).
    Aggregates members and themroles across all subclasses."""
    tree = ET.parse(xml_path)
    root = tree.getroot()
    class_id = norm(root.get("ID", "").strip())
    members: list[str] = []
    seen = set()
    for m in root.iter("MEMBER"):
        n = norm((m.get("name") or "").strip().lower())
        if n and n not in seen:
            seen.add(n)
            members.append(n)
    themroles: list[str] = []
    seen_roles = set()
    for tr in root.iter("THEMROLE"):
        t = (tr.get("type") or "").strip()
        if t and t not in seen_roles:
            seen_roles.add(t)
            themroles.append(t)
    example = first_example(root)
    return {
        "class_id": class_id,
        "members": members,
        "themroles": themroles,
        "example": example,
    }


# --- 1. Load workbook to identify which classes are NOT missing ---
workbook_classes: set[str] = set()
workbook_class_to_domain: dict[str, str] = {}
with open(WORKBOOK_CSV) as f:
    for row in csv.DictReader(f):
        c = norm((row.get("VerbNet Class") or "").strip())
        d = (row.get("Situation Domain") or "").strip()
        if c:
            workbook_classes.add(c)
            if d:
                workbook_class_to_domain[c] = d

# --- 2. Parse all VN 3.4 XMLs, group by top-level class ---
class_data: dict[str, dict] = {}
for xml_file in sorted(VN_DIR.glob("*.xml")):
    try:
        meta = parse_class_xml(xml_file)
    except ET.ParseError:
        continue
    if not meta["class_id"]:
        continue
    top = top_level(meta["class_id"])
    if top in class_data:
        # Merge subclass-only XMLs into top-level (rare but possible)
        existing = class_data[top]
        for m in meta["members"]:
            if m not in existing["members"]:
                existing["members"].append(m)
        for tr in meta["themroles"]:
            if tr not in existing["themroles"]:
                existing["themroles"].append(tr)
        if not existing.get("example") and meta["example"]:
            existing["example"] = meta["example"]
    else:
        class_data[top] = meta

# --- 3. Identify the 81 missing classes ---
missing = sorted(set(class_data.keys()) - workbook_classes)
print(f"Workbook classes:      {len(workbook_classes):,}")
print(f"VN 3.4 top-level classes: {len(class_data):,}")
print(f"Missing from workbook: {len(missing):,}")

# --- 4. Generate Situation names + check for collisions with v1.0 ---
with open(ASC_JSON) as f:
    asc_defs: dict[str, str] = json.load(f)
v1_names_lower = {k.lower() for k in asc_defs.keys()}

new_situations: dict[str, dict] = {}
collisions: list[tuple[str, str]] = []
for class_id in missing:
    name = situation_name_from_class(class_id)
    # Suffix the class number if there's a collision
    if name.lower() in v1_names_lower or name in new_situations:
        # Append the dotted number from the class id, replacing dots with underscores
        suffix = class_id.split("-", 1)[1].replace(".", "_") if "-" in class_id else ""
        candidate = f"{name}_{suffix}" if suffix else f"{name}_{len(new_situations)}"
        collisions.append((class_id, name + " -> " + candidate))
        name = candidate
    new_situations[name] = {
        "vn_class": class_id,
        "members": class_data[class_id]["members"],
        "themroles": class_data[class_id]["themroles"],
        "example": class_data[class_id]["example"],
    }

if collisions:
    print(f"\nName collisions resolved by appending VN class number ({len(collisions)}):")
    for cid, msg in collisions:
        print(f"  {cid}: {msg}")

# --- 5. Domain assignment by VN-class-number neighborhood ---
def vn_main_number(class_id: str) -> float | None:
    """leave-51.2 -> 51.2; non_agentive-50.1 -> 50.1"""
    m = re.search(r"-(\d+(?:\.\d+)?)", class_id)
    return float(m.group(1)) if m else None

# Bucket workbook classes by main number; for each missing class, take the
# Domain of the closest workbook class.
workbook_by_num: list[tuple[float, str, str]] = []  # (num, class_id, domain)
for c, d in workbook_class_to_domain.items():
    num = vn_main_number(c)
    if num is not None:
        workbook_by_num.append((num, c, d))
workbook_by_num.sort()

def assign_domain(class_id: str) -> tuple[str, str]:
    target = vn_main_number(class_id)
    if target is None or not workbook_by_num:
        return ("Unassigned", "no class number; manual review")
    nearest = min(workbook_by_num, key=lambda r: abs(r[0] - target))
    return (nearest[2], f"by-adjacency to {nearest[1]} (num {nearest[0]})")

for name, info in new_situations.items():
    domain, dom_evidence = assign_domain(info["vn_class"])
    info["situation_domain"] = domain
    info["domain_evidence"] = dom_evidence

# --- 6. Generate one-sentence definitions ---
def make_definition(info: dict) -> str:
    members = info["members"][:5]  # up to 5 sample verbs
    sample = ", ".join(members) if members else "various verbs"
    subject_phrase, lead = themrole_summary(info["themroles"])
    example = info.get("example")
    base = f"{lead} ({sample}). The grammatical subject is the {subject_phrase}."
    if example:
        # Strip any HTML/markup
        ex_clean = re.sub(r"\s+", " ", example).strip()
        if len(ex_clean) > 140:
            ex_clean = ex_clean[:137] + "..."
        base = f"{base} Example: \"{ex_clean}\"."
    return base

for name, info in new_situations.items():
    info["definition"] = make_definition(info)

# --- 7. Output preview ---
print(f"\nCreated {len(new_situations)} new Situation entries. Sample:\n")
for name in list(new_situations.keys())[:5]:
    info = new_situations[name]
    print(f"  {name}  ({info['vn_class']}, domain: {info['situation_domain']})")
    print(f"    members: {info['members'][:5]}")
    print(f"    def: {info['definition']}")
    print()

if args.dry_run:
    print("DRY RUN — no files written.")
    raise SystemExit(0)

# --- 8. Write outputs ---
# 8a. asc_definitions.json
for name, info in new_situations.items():
    asc_defs[name] = info["definition"]
ASC_JSON.write_text(json.dumps(asc_defs, indent=2, ensure_ascii=False) + "\n")
print(f"Wrote {ASC_JSON} ({len(asc_defs)} keys)")

# 8b. vn_class_derived_lexicon.csv (parallel to workbook)
LEXICON_CSV.parent.mkdir(parents=True, exist_ok=True)
with open(LEXICON_CSV, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Verb", "VerbNet Class", "Situation Domain", "Situation", "Polysemy"])
    for name, info in new_situations.items():
        for v in info["members"]:
            w.writerow([v, info["vn_class"], info["situation_domain"], name, ""])
print(f"Wrote {LEXICON_CSV}")

# 8c. Empty pos/neg stubs
header = ("sentence,verb_lemma,verb_token_idx,on_sense,wn_synsets,vn_class,"
          "situation,match_path,source_file,sentence_idx,situation_count,needs_review\n")
POS_DIR.mkdir(parents=True, exist_ok=True)
NEG_DIR.mkdir(parents=True, exist_ok=True)
stub_count = 0
for name in new_situations:
    pos_path = POS_DIR / f"{name}_pos.csv"
    neg_path = NEG_DIR / f"{name}_neg.csv"
    if not pos_path.exists():
        pos_path.write_text(header)
        stub_count += 1
    if not neg_path.exists():
        neg_path.write_text(header)
print(f"Created {stub_count} pos/neg stubs (one each per Situation, where missing)")

# 8d. Metadata JSON for editorial review
META_JSON.write_text(
    json.dumps(new_situations, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
)
print(f"Wrote {META_JSON}")

print(f"\nDone. v2.0 inventory: {len(asc_defs)} Situations "
      f"(62 v1.0 + {len(new_situations)} VN-derived)")
