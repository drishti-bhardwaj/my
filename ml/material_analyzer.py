"""
Material Intelligence AI/NLP Similarity Analyzer & Grouping Service

Provides robust, multi-factor, specification-aware similarity scoring
and material entry grouping for OCR-extracted legacy CPSE text streams.
"""

import re
import difflib
from typing import Any, Dict, List, Optional, Tuple, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .unit_normalizer import parse_length, are_lengths_equivalent
from .document_extractor import is_binary_garbage


DEFAULT_WEIGHTS = {
    "name": 0.30,
    "token": 0.30,
    "spec": 0.25,
    "fuzzy": 0.08,
    "semantic": 0.07,
}

DEFAULT_THRESHOLDS = {
    "very_high": 95.0,
    "high": 85.0,
    "review": 70.0,
}


def clean_and_normalize_text(text: str) -> str:
    """Normalize casing, punctuation, hyphens, unit spacing, and whitespace."""
    if not text:
        return ""
    text = text.replace("\xa0", " ").replace("\t", " ")
    # Replace hyphens/underscores in names with space for token matching
    text = re.sub(r"[-_]+", " ", text)
    # Normalize unit spacing (e.g. '8 mm' -> '8mm', '8 MM' -> '8mm', '80 GSM' -> '80gsm', '10 kVA' -> '10kva')
    text = re.sub(r"(\d+(?:\.\d+)?)\s*(mm|cm|m|inch|in|kg|kgs|bags|mtr|nos|pcs|gsm|kva|psi|bar|v|w|hp)\b", r"\1\2", text, flags=re.IGNORECASE)
    # Remove special characters except digits, letters, dots, and spaces
    text = re.sub(r"[^\w\s\.]", "", text)
    # Collapse multiple spaces
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def extract_specifications(text: str) -> Dict[str, Any]:
    """
    Extract engineering dimensions, grades, ratings, quantities, and units from text.
    Handles OCR variations like '8mm', '8 mm', '8 MM', '2 inch', 'OPC 43'.
    """
    specs: Dict[str, Any] = {
        "dimensions": [],
        "grades": [],
        "quantity": None,
        "unit": None,
        "raw_specs": [],
    }

    upper_text = text.upper()

    # 1. Dimension Extraction (e.g., 8mm, 10mm, 50mm, 2 inch, M10, 50.0 mm)
    dim_matches = re.findall(r"\b(\d+(?:\.\d+)?)\s*(MM|CM|M|INCH|IN|\"|METER|METRE)\b", upper_text)
    for num, unit_str in dim_matches:
        parsed_length = parse_length(f"{num} {unit_str}")
        if parsed_length is not None:
            specs["dimensions"].append({
                "value": parsed_length,
                "raw": f"{num}{unit_str}",
            })
            specs["raw_specs"].append(f"{num}{unit_str.lower()}")

    # Metric thread notation (e.g. M10, M12)
    metric_dia = re.findall(r"\bM\s*(\d+(?:\.\d+)?)\b", upper_text)
    for m_val in metric_dia:
        specs["dimensions"].append({
            "value": float(m_val),
            "raw": f"M{m_val}",
        })
        specs["raw_specs"].append(f"m{m_val}")

    # 2. Material Grade / Type Extraction (e.g. SS304, SS316, OPC 43, OPC 53, CF8M)
    grade_match = re.search(r"\b(SS\s*304|SS\s*316|SS304|SS316|CF8M|OPC\s*43|OPC\s*53|GRADE\s*\d+)\b", upper_text)
    if grade_match:
        grade_str = grade_match.group(1).replace(" ", "")
        specs["grades"].append(grade_str)
        specs["raw_specs"].append(grade_str.lower())

    # 3. Quantity and Unit Extraction (e.g. 100 KG, 20 Bags, 2500 NOS, 50 MTR)
    qty_match = re.search(r"\b(\d+(?:,\d+)?(?:\.\d+)?)\s*(KG|KGS|BAGS|BAG|NOS|NO|MTR|METERS|PCS|PIECES|REAMS|REAM)\b", upper_text)
    if qty_match:
        qty_num = float(qty_match.group(1).replace(",", ""))
        unit_token = qty_match.group(2).rstrip("S")
        if unit_token in {"NO", "PC", "PIECE"}:
            unit_token = "NOS"
        elif unit_token == "BAG":
            unit_token = "BAGS"
        elif unit_token == "METER":
            unit_token = "MTR"
        elif unit_token == "REAM":
            unit_token = "REAMS"

        specs["quantity"] = qty_num
        specs["unit"] = unit_token

    return specs


def parse_material_entry(raw_line: str) -> Optional[Dict[str, Any]]:
    """
    Parse an OCR text line into structured material attributes.
    """
    line = raw_line.strip()
    if not line or len(line) < 3 or is_binary_garbage(line):
        return None

    # Filter out header noise / document title lines that are not material items
    upper = line.upper()
    if any(header_kw in upper for header_kw in ["PURCHASE ORDER", "DATE:", "VENDOR:", "HEADER", "PLANT_CODE", "DEPARTMENT"]):
        return None
    if upper.strip() in {"OFFICE & DESK CONSUMABLES", "IT & ENTERPRISE TECHNOLOGY", "OFFICE DESK CONSUMABLES", "IT ENTERPRISE TECHNOLOGY"}:
        return None

    # Clean raw text
    clean = clean_and_normalize_text(line)

    # Extract specs, qty, unit
    specs = extract_specifications(line)

    # Extract canonical material name (strip quantities, units, explicit specs, description tails, and parenthetical brand notes)
    canonical = line
    # Strip feature/description details after ' - ' or ' – '
    if " - " in canonical:
        canonical = canonical.split(" - ", 1)[0].strip()
    elif " – " in canonical:
        canonical = canonical.split(" – ", 1)[0].strip()

    # Remove quantity pattern
    canonical = re.sub(r"\b\d+(?:,\d+)?(?:\.\d+)?\s*(KG|KGS|BAGS|BAG|NOS|NO|MTR|METERS|PCS|PIECES|REAMS|REAM)\b", "", canonical, flags=re.IGNORECASE)
    # Remove bullet/item prefixes like "ITEM 001:", "- ", or "o "
    canonical = re.sub(r"^(?:ITEM\s*\d+:|[-*•o\d\.]+\s*)", "", canonical, flags=re.IGNORECASE)
    # Remove parenthetical brand notes like (JK Papers), (Godrej Interio), (HP / Dell)
    canonical = re.sub(r"\([^)]*\)", "", canonical).strip()

    # Extract primary material keywords
    material_keywords = []
    tokens = clean_and_normalize_text(canonical).split()
    for tok in tokens:
        if not tok.isdigit() and tok not in {"mm", "kg", "mtr", "bags", "nos", "pcs", "cm", "inch", "reams"}:
            tok_fixed = tok.replace("steei", "steel").replace("stee1", "steel")
            material_keywords.append(tok_fixed)

    canonical_name = " ".join(material_keywords).title() if material_keywords else canonical

    # Format specification string summary
    spec_summary = ", ".join(specs["raw_specs"]) if specs["raw_specs"] else ""
    if not spec_summary and specs["dimensions"]:
        spec_summary = f"{specs['dimensions'][0]['value']}mm"

    return {
        "original_text": line,
        "clean_text": clean,
        "canonical_name": canonical_name or line,
        "specification": spec_summary,
        "spec_details": specs,
        "quantity": specs["quantity"],
        "unit": specs["unit"],
    }


def extract_material_entries(raw_ocr_text: str) -> List[Dict[str, Any]]:
    """
    Separate raw OCR text into candidate material entries.
    Handles multi-line text as well as single-paragraph streams delimited by
    periods, semicolons, bullets, or item tags.
    """
    if not raw_ocr_text:
        return []

    text_blocks = raw_ocr_text.splitlines()
    candidate_lines = []

    for block in text_blocks:
        block = block.strip()
        if not block:
            continue
        # Split block by period, semicolon, bullet " o ", " • ", or "ITEM "
        sub_lines = re.split(r"(?<=\.)\s+|\s*;\s*|\s+o\s+|\s+•\s+|\s*(?=ITEM\s*\d+:)", block)
        for s in sub_lines:
            s_clean = s.strip()
            if s_clean and len(s_clean) >= 3:
                candidate_lines.append(s_clean)

    entries = []
    seen_texts = set()

    for line in candidate_lines:
        entry = parse_material_entry(line)
        if entry and entry["original_text"] not in seen_texts:
            seen_texts.add(entry["original_text"])
            entries.append(entry)

    if not entries:
        entry = parse_material_entry(raw_ocr_text)
        if entry:
            entries.append(entry)

    return entries


def calculate_material_similarity(
    item_a: Dict[str, Any],
    item_b: Dict[str, Any],
    weights: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Compute multi-factor similarity score (0.0 to 100.0%) between two material entries.
    Considers normalized name, word-order-independent tokens, specification precision,
    fuzzy ratio (for OCR typos), and TF-IDF semantic similarity.
    """
    w = weights or DEFAULT_WEIGHTS

    text_a = item_a["clean_text"]
    text_b = item_b["clean_text"]

    # 1. Normalized Material Name Similarity
    name_a = clean_and_normalize_text(item_a.get("canonical_name", text_a))
    name_b = clean_and_normalize_text(item_b.get("canonical_name", text_b))
    name_score = difflib.SequenceMatcher(None, name_a, name_b).ratio()

    # 2. Word-Order-Independent Token Overlap Score (Jaccard + Core Subset Overlap)
    tokens_a = set(name_a.split())
    tokens_b = set(name_b.split())

    ignore_tokens = {"size", "white", "black", "yellow", "blue", "red", "green", "color", "colour", "brand", "make", "type", "set", "sets"}
    core_a = tokens_a - ignore_tokens
    core_b = tokens_b - ignore_tokens

    if core_a and core_b:
        intersection = core_a.intersection(core_b)
        union = core_a.union(core_b)
        jaccard = len(intersection) / float(len(union))
        min_len = min(len(core_a), len(core_b))
        subset_ratio = len(intersection) / float(min_len) if min_len > 0 else 0
        token_score = max(jaccard, subset_ratio * 0.95)
    elif tokens_a or tokens_b:
        intersection = tokens_a.intersection(tokens_b)
        union = tokens_a.union(tokens_b)
        token_score = len(intersection) / float(len(union))
    else:
        token_score = 1.0

    # 3. Specification Precision Check (Dimensions & Grades)
    specs_a = item_a.get("spec_details", {})
    specs_b = item_b.get("spec_details", {})

    dims_a = specs_a.get("dimensions", [])
    dims_b = specs_b.get("dimensions", [])
    grades_a = specs_a.get("grades", [])
    grades_b = specs_b.get("grades", [])

    spec_score = 1.0
    explicit_spec_mismatch = False

    # Dimension comparison
    if dims_a and dims_b:
        val_a = dims_a[0]["value"]
        val_b = dims_b[0]["value"]
        if are_lengths_equivalent(val_a, val_b, tolerance_mm=0.5):
            spec_score = 1.0
        else:
            spec_score = 0.0
            explicit_spec_mismatch = True
    elif (dims_a and not dims_b) or (not dims_a and dims_b):
        spec_score = 0.5

    # Grade comparison
    if grades_a and grades_b:
        if grades_a[0] == grades_b[0]:
            spec_score = min(spec_score, 1.0)
        else:
            spec_score = 0.0
            explicit_spec_mismatch = True

    # 4. Fuzzy Similarity (handles OCR typos like SteeI vs Steel)
    fuzzy_score = difflib.SequenceMatcher(None, text_a, text_b).ratio()

    # 5. Semantic TF-IDF Cosine Similarity
    try:
        vectorizer = TfidfVectorizer(analyzer="char_ngram", ngram_range=(2, 4))
        tfidf_matrix = vectorizer.fit_transform([text_a, text_b])
        semantic_score = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
    except Exception:
        semantic_score = fuzzy_score

    # Calculate weighted combined score
    combined_score = (
        name_score * w["name"]
        + token_score * w["token"]
        + spec_score * w["spec"]
        + fuzzy_score * w["fuzzy"]
        + semantic_score * w["semantic"]
    )

    final_percentage = round(combined_score * 100, 1)

    # CRITICAL PRECISION CAP: If explicit specifications mismatch, cap max similarity at 65.0%
    if explicit_spec_mismatch:
        final_percentage = min(final_percentage, 65.0)

    # If completely different token sets, cap similarity at 30%
    if not tokens_a.intersection(tokens_b) and tokens_a and tokens_b:
        final_percentage = min(final_percentage, 30.0)

    # If items are exact token-equivalent despite word order or formatting
    if tokens_a == tokens_b and not explicit_spec_mismatch and tokens_a:
        final_percentage = max(final_percentage, 98.0)
    elif core_a == core_b and core_a and not explicit_spec_mismatch:
        final_percentage = max(final_percentage, 94.0)

    return {
        "final_similarity": final_percentage,
        "name_score": round(name_score * 100, 1),
        "token_score": round(token_score * 100, 1),
        "spec_score": round(spec_score * 100, 1),
        "fuzzy_score": round(fuzzy_score * 100, 1),
        "semantic_score": round(semantic_score * 100, 1),
        "explicit_spec_mismatch": explicit_spec_mismatch,
    }


def group_similar_materials(
    entries: List[Dict[str, Any]],
    thresholds: Optional[Dict[str, float]] = None,
) -> List[Dict[str, Any]]:
    """
    Cluster material entries into similarity groups using canonical leaders.
    """
    if not entries:
        return []

    t = thresholds or DEFAULT_THRESHOLDS
    groups: List[Dict[str, Any]] = []

    for entry in entries:
        assigned = False

        for group in groups:
            canonical_leader = group["leader"]
            similarity_res = calculate_material_similarity(canonical_leader, entry)
            sim_pct = similarity_res["final_similarity"]

            # Group entries if similarity is >= review threshold (70%) and no spec mismatch
            if sim_pct >= t["review"] and not similarity_res["explicit_spec_mismatch"]:
                status_label = "EXACT MATCH" if sim_pct >= t["very_high"] else ("HIGH SIMILARITY" if sim_pct >= t["high"] else "EQUIVALENT")
                badge_class = "status-approved" if sim_pct >= t["very_high"] else ("status-verified" if sim_pct >= t["high"] else "status-equivalent")

                group["members"].append({
                    **entry,
                    "similarity": sim_pct,
                    "status_label": status_label,
                    "badge_class": badge_class,
                })
                assigned = True
                break

        if not assigned:
            # Create a new material group
            groups.append({
                "canonical_name": entry["canonical_name"],
                "specification": entry["specification"],
                "leader": entry,
                "members": [
                    {
                        **entry,
                        "similarity": 100.0,
                        "status_label": "CANONICAL REFERENCE",
                        "badge_class": "status-verified",
                    }
                ],
            })

    return groups


def analyze_ocr_text(raw_ocr_text: str) -> Dict[str, Any]:
    """
    Primary API entry point: Analyzes raw OCR text, extracts material entries,
    calculates multi-factor similarity matching percentages, and groups similar items.
    """
    entries = extract_material_entries(raw_ocr_text)
    groups = group_similar_materials(entries)

    return {
        "total_entries": len(entries),
        "total_groups": len(groups),
        "entries": entries,
        "groups": groups,
    }
