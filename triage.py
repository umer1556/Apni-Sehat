# triage.py  –  Apni Sehat v1.2
# Clinical safety routing logic.
# Returns GREEN / AMBER / RED based on user health data.
# Your doctor teammate can adjust thresholds in config.py without touching this file.
#
# ── Reference sources ────────────────────────────────────────────────────────
# BP:          Pakistan Hypertension League (PHL) Guidelines 2023
#              ESC/ESH 2018 — adopted by Pakistan Society of Cardiology
# A1c:         ADA Standards of Care 2024, Section 6 (Glycaemic Targets)
#              Pakistan Endocrine Society (PES) Clinical Practice Guidelines
#              Note: PES accepts up to 8.0% for elderly/complex patients,
#              hence 8.0% caution vs 7.0% goal distinction.
# Glucose:     ADA 2024 — Level 1 hypo <70, urgent action ≥250 (IDF-DAR)
# Cholesterol: Pakistan Society of Cardiology / NCEP ATP III
# Variability: International Consensus on Time in Range (Battelino 2019)
# ─────────────────────────────────────────────────────────────────────────────

import math
from typing import List, Optional, Tuple
from config import TRIAGE


def _to_num(x):
    """Safely convert to float, else return None."""
    try:
        if x is None or x == "":
            return None
        return float(x)
    except (TypeError, ValueError):
        return None


def _mean(xs: List[float]) -> float:
    return sum(xs) / max(len(xs), 1)


def _std(xs: List[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(var)


def triage_profile(
    diabetes_type: str,
    has_hypertension: bool,
    has_high_cholesterol: bool,
    bp_sys: Optional[float],
    bp_dia: Optional[float],
    a1c: Optional[float],
    fasting_readings: List[float],
    total_cholesterol: Optional[float],
    other_major_conditions: bool,
) -> Tuple[str, List[str]]:
    """
    Returns:
        level: "GREEN" | "AMBER" | "RED"
        flags: list of human-readable notes shown to the user

    Triage logic summary:
        GREEN  — all values within target, no flags
        AMBER  — one or more values above goal or condition flagged;
                 user can access the app with appropriate warnings
        RED    — critical value present; user is blocked and directed
                 to seek clinical care before using the app

    RED triggers (any one is sufficient):
        • Other major conditions selected
        • BP ≥ 180/120 (hypertensive crisis — PHL 2023)
        • A1c ≥ 9.0% (ADA 2024 — high complication risk)
        • Any fasting reading ≥ 250 mg/dL (IDF-DAR urgent threshold)
        • Fasting glucose range ≥ 120 mg/dL or SD ≥ 45 mg/dL

    AMBER triggers (any one is sufficient):
        • BP ≥ 140/90 (PHL Stage 2) or hypertension ticked without values
        • A1c > 7.0% (above ADA/PES goal — any elevation warrants follow-up)
        • A1c ≥ 8.0% raises a stronger clinical note
        • Any fasting reading < 70 mg/dL (hypoglycaemia — ADA Level 1)
        • Fasting glucose SD ≥ 25 or any reading > 130 mg/dL
        • Total cholesterol ≥ 200 mg/dL
        • High cholesterol ticked without values
        • No clinical data provided at all (conservative default)
    """

    # Normalize inputs
    diabetes_type         = (diabetes_type or "")
    has_hypertension      = bool(has_hypertension)
    has_high_cholesterol  = bool(has_high_cholesterol)
    other_major_conditions = bool(other_major_conditions)

    bp_sys            = _to_num(bp_sys)
    bp_dia            = _to_num(bp_dia)
    a1c               = _to_num(a1c)
    total_cholesterol = _to_num(total_cholesterol)

    raw_fasting = fasting_readings or []
    fasting_readings = [_to_num(x) for x in raw_fasting if _to_num(x) is not None]

    flags: List[str] = []
    level = "GREEN"

    # ── Immediate RED: other major conditions ─────────────────────────────────
    if other_major_conditions:
        return "RED", [
            "Other major conditions selected. "
            "Please consult a clinician before using this app for dietary changes."
        ]

    # ── Diabetes type note ────────────────────────────────────────────────────
    if diabetes_type.strip().lower() == "type 1":
        flags.append(
            "Type 1 diabetes: this app provides dietary support only — "
            "never adjust insulin or medication based on this app."
        )

    # ── Blood pressure ────────────────────────────────────────────────────────
    # PHL 2023 / ESC-ESH 2018:
    #   Crisis  ≥ 180/120 → immediate RED (emergency referral)
    #   Stage 2 ≥ 140/90  → AMBER (clinician follow-up recommended)
    if has_hypertension or (bp_sys is not None and bp_dia is not None):
        if bp_sys is not None and bp_dia is not None:
            if bp_sys > TRIAGE["bp_crisis_sys"] or bp_dia > TRIAGE["bp_crisis_dia"]:
                return "RED", [
                    "Blood pressure is in a severe range. Please seek urgent medical care."
                ]
            if bp_sys >= TRIAGE["bp_stage2_sys"] or bp_dia >= TRIAGE["bp_stage2_dia"]:
                level = "AMBER"
                flags.append("Blood pressure is elevated. Clinician follow-up recommended.")
        else:
            # Hypertension ticked but no values — conservative AMBER
            level = "AMBER"
            flags.append("Hypertension selected but BP values not provided — proceed with care.")

    # ── Cholesterol ───────────────────────────────────────────────────────────
    # Pakistan Society of Cardiology / NCEP ATP III:
    #   ≥ 240 mg/dL → high (AMBER + strong recommendation)
    #   ≥ 200 mg/dL → borderline (heart-healthy plan applied, AMBER)
    if has_high_cholesterol or (total_cholesterol is not None and total_cholesterol > 0):
        if total_cholesterol is not None and total_cholesterol > 0:
            if total_cholesterol >= TRIAGE["tc_high"]:
                level = "AMBER"
                flags.append(
                    "Total cholesterol is high — a heart-healthy plan is recommended. "
                    "Please follow up with your doctor."
                )
            elif total_cholesterol >= TRIAGE["tc_borderline"]:
                level = "AMBER"
                flags.append("Total cholesterol is borderline high — heart-healthy plan applied.")
        else:
            level = "AMBER"
            flags.append("High cholesterol selected but value not provided — proceed with care.")

    # ── Glycaemic control: A1c preferred, fasting readings as fallback ────────
    if a1c is not None and a1c > 0:
        # ADA 2024 — goal < 7.0% for most non-elderly adults
        # PES: goal < 7.0%; accepts up to 8.0% for elderly/complex patients
        if a1c >= TRIAGE["a1c_red"]:
            # ≥ 9.0% → RED — significantly elevated microvascular complication risk
            return "RED", [
                "HbA1c is very high. Please see a clinician before making dietary changes."
            ]
        if a1c >= TRIAGE["a1c_caution"]:
            # 8.0–8.9% → AMBER with stronger note
            level = "AMBER"
            flags.append(
                "HbA1c is above the safe threshold — proceed with care and "
                "follow up with your doctor promptly."
            )
        elif a1c > TRIAGE["a1c_goal"]:
            # 7.0–7.9% → AMBER (ADA 2024: any value above goal warrants follow-up)
            # Previously this was only a note without changing level — corrected here.
            level = "AMBER"
            flags.append(
                "HbA1c is above the typical target of 7.0%. "
                "Focus on consistency and follow up with your doctor."
            )

    else:
        # No A1c — use fasting readings if available
        fr = [x for x in fasting_readings if x is not None and x > 0]
        if fr:
            # IDF-DAR: ≥ 250 mg/dL = urgent action threshold → RED
            if any(x >= TRIAGE["very_high"] for x in fr):
                return "RED", [
                    "Very high fasting glucose recorded. Please seek medical advice."
                ]
            # ADA Level 1 hypo: < 70 mg/dL → AMBER
            if any(x < TRIAGE["hypo"] for x in fr):
                level = "AMBER"
                flags.append(
                    "Low fasting glucose detected — discuss with your clinician."
                )
            if len(fr) >= 2:
                sd  = _std(fr)
                rng = max(fr) - min(fr)
                # Large variability → RED (Battelino 2019 consensus)
                if rng >= TRIAGE["fasting_range_red"] or sd >= TRIAGE["fasting_std_red"]:
                    return "RED", [
                        "Large variation in recent fasting readings — please see a clinician."
                    ]
                # Moderate variability or above pre-meal target → AMBER
                if sd >= TRIAGE["fasting_std_amber"] or any(x > TRIAGE["premeal_high"] for x in fr):
                    level = "AMBER"
                    flags.append(
                        "Recent fasting readings show variability or are above target — "
                        "proceed with care."
                    )
        else:
            # No clinical data at all — conservative AMBER (cannot assess risk)
            level = "AMBER"
            flags.append(
                "No A1c or fasting readings provided — "
                "proceeding with a cautious plan. Consider sharing test results for a more accurate assessment."
            )

    return level, flags
