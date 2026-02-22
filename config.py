# config.py  –  Apni Sehat v1.2
# Clinical thresholds and meal structure profiles.
# Doctor teammate can adjust thresholds here without touching any other file.
#
# ── Reference sources ────────────────────────────────────────────────────────
# BP:          Pakistan Hypertension League (PHL) Guidelines 2023
#              JNC 8 / ESC-ESH 2018 (adopted by Pakistan Society of Cardiology)
# Glucose:     ADA Standards of Care 2024
#              IDF-DAR Diabetes and Ramadan Guidelines 2021
#              Pakistan Endocrine Society (PES) Clinical Practice Guidelines
# HbA1c:       ADA 2024 + PES consensus
# Cholesterol: Pakistan Society of Cardiology / NCEP ATP III
# BMI:         WHO Expert Consultation on Asian BMI thresholds (2004)
#              Used by Pakistan NCD Programme
# Variability: International Consensus on Time in Range (Battelino et al. 2019)
#              CV% >36% = high variability (Danne et al. Diabetes Care 2017)
# ─────────────────────────────────────────────────────────────────────────────

TRIAGE = {
    # ── Blood pressure (mmHg) ────────────────────────────────────────────────
    # PHL / ESC-ESH: Stage 2 hypertension ≥ 140/90 — intervention threshold
    # used across Pakistan clinical guidelines (AHA 2017 uses 130/80 but that
    # is not yet adopted as the Pakistan action threshold).
    # Hypertensive crisis ≥ 180/120 — emergency referral required.
    "bp_stage2_sys":  140,
    "bp_stage2_dia":  90,
    "bp_crisis_sys":  180,
    "bp_crisis_dia":  120,

    # ── Glucose (mg/dL) ──────────────────────────────────────────────────────
    # ADA 2024 / PES — awareness thresholds, NOT diagnostic values.
    # hypo:          < 70 mg/dL — Level 1 hypoglycaemia (ADA 2024)
    # premeal_high:  > 130 mg/dL — above ADA pre-meal target (80–130)
    # postmeal_high: > 180 mg/dL — above ADA 1–2hr post-meal target
    # very_high:     ≥ 250 mg/dL — IDF-DAR Ramadan guideline break-fast
    #                threshold; Pakistan clinicians generally use 250–270 as
    #                the urgent action threshold. 300 was too conservative
    #                and delayed alerts when ketosis risk is already meaningful.
    "hypo":           70,
    "premeal_high":   130,
    "postmeal_high":  180,
    "very_high":      250,

    # ── HbA1c (%) ────────────────────────────────────────────────────────────
    # ADA 2024 + PES:
    #   < 7.0% = well-controlled (GREEN)
    #   7.0–8.9% = sub-optimal (AMBER) — 8.0% chosen as caution trigger
    #     because Pakistani guidelines accept up to 8.0% for elderly/complex
    #     patients; flagging at 8.0% prompts check without over-alarming
    #   ≥ 9.0% = poorly controlled (RED) — high microvascular complication risk
    "a1c_goal":       7.0,
    "a1c_caution":    8.0,
    "a1c_red":        9.0,

    # ── Total cholesterol (mg/dL) ─────────────────────────────────────────────
    # Pakistan Society of Cardiology / NCEP ATP III:
    #   < 200  = desirable
    #   200–239 = borderline high (AMBER)
    #   ≥ 240  = high (used for RED flag in combination with other factors)
    "tc_borderline":  200,
    "tc_high":        240,

    # ── Fasting glucose variability ───────────────────────────────────────────
    # Derived from International Consensus on Time in Range (Battelino 2019)
    # and Danne et al. Diabetes Care 2017 (CV% >36% = high variability).
    # We use std dev and range of a small fasting readings sample as a
    # pragmatic proxy — described in the UI as "screening flags" not
    # clinical diagnostic thresholds.
    #   std_amber: SD ≥ 25 mg/dL — suggests inconsistent fasting control
    #   std_red:   SD ≥ 45 mg/dL — suggests significant instability
    #   range_red: range ≥ 120 mg/dL — wide swing across readings
    "fasting_std_amber":  25.0,
    "fasting_std_red":    45.0,
    "fasting_range_red":  120.0,
}

CARB = {
    # 1 carb serving = 15g carbs (standard exchange system — ADA / PES)
    "carb_serving_grams": 15,
}

# ── South Asian BMI thresholds ────────────────────────────────────────────────
# WHO Expert Consultation on obesity in Asian populations (2004).
# Adopted by Pakistan NCD Programme and Pakistan Endocrine Society.
# South Asian metabolic risk begins at lower BMI than Western populations:
#   Overweight: ≥ 23.0 (vs 25.0 Western)
#   Obese:      ≥ 27.5 (vs 30.0 Western)
BMI = {
    "underweight":  18.5,
    "normal_max":   22.9,
    "overweight":   23.0,
    "obese":        27.5,
}

# ── Meal structure profiles ───────────────────────────────────────────────────
# Each profile defines which slots appear in the daily plan.
# Slots: breakfast, snack_am, lunch, snack_pm, dinner, snack_bed
# Clinical basis: ADA nutrition therapy recommendations + PES meal frequency
# guidance for insulin users and hypoglycaemia-prone patients.

MEAL_PROFILES = {
    # Standard: stable Type 2, no insulin, no hypo episodes
    "3M_1S": {
        "label_en": "3 meals + 1 snack",
        "label_ur": "3 کھانے + 1 ناشتہ",
        "reason_en": "Standard plan for stable blood sugar — 3 balanced meals with one afternoon snack.",
        "reason_ur": "مستحکم بلڈ شوگر کے لیے معیاری منصوبہ۔",
        "slots": ["breakfast", "lunch", "snack_pm", "dinner"],
    },

    # Insulin OR hypo episodes OR weakness between meals → 2 snacks
    "3M_2S": {
        "label_en": "3 meals + 2 snacks",
        "label_ur": "3 کھانے + 2 ناشتے",
        "reason_en": (
            "You need regular fuel throughout the day to prevent blood sugar dips. "
            "A mid-morning and afternoon snack keeps your levels steady."
        ),
        "reason_ur": (
            "آپ کو بلڈ شوگر گرنے سے بچانے کے لیے دن بھر باقاعدہ کھانا ضروری ہے۔ "
            "صبح اور دوپہر کے درمیان اور شام کا ناشتہ آپ کی شوگر مستحکم رکھتا ہے۔"
        ),
        "slots": ["breakfast", "snack_am", "lunch", "snack_pm", "dinner"],
    },

    # Insulin AND hypo episodes — highest risk of dangerous glucose drops
    "3M_3S": {
        "label_en": "3 meals + 3 snacks",
        "label_ur": "3 کھانے + 3 ناشتے",
        "reason_en": (
            "Because you use insulin and experience low sugar episodes, "
            "eating every 2–3 hours is important to stay safe. "
            "The bedtime snack is essential to prevent overnight glucose drops. "
            "Do not go more than 3 hours without eating."
        ),
        "reason_ur": (
            "چونکہ آپ انسولین لیتے ہیں اور کم شوگر کی علامات آتی ہیں، "
            "ہر 2-3 گھنٹے میں کچھ نہ کچھ کھانا ضروری ہے۔ "
            "سونے سے پہلے کا ناشتہ رات میں شوگر گرنے سے بچاتا ہے۔ "
            "3 گھنٹے سے زیادہ بھوکے نہ رہیں۔"
        ),
        "slots": ["breakfast", "snack_am", "lunch", "snack_pm", "dinner", "snack_bed"],
    },

    # Overweight/obese Type 2, no insulin — portion-controlled
    "SMALL_3M_1S": {
        "label_en": "3 lighter meals + 1 snack (portion-controlled)",
        "label_ur": "3 ہلکے کھانے + 1 ناشتہ (کم مقدار)",
        "reason_en": (
            "Because your BMI suggests you are carrying extra weight, "
            "your plan uses smaller portions and lighter meals "
            "to support gradual, healthy weight loss alongside blood sugar control."
        ),
        "reason_ur": (
            "آپ کا BMI اضافی وزن ظاہر کرتا ہے، اس لیے آپ کے منصوبے میں "
            "کم مقدار اور ہلکے کھانے شامل ہیں تاکہ وزن آہستہ آہستہ کم ہو "
            "اور بلڈ شوگر بھی کنٹرول میں رہے۔"
        ),
        "slots": ["breakfast", "lunch", "snack_pm", "dinner"],
        "portion_note_en": "Keep portions small — use a side plate, not a full plate.",
        "portion_note_ur": "کھانا کم مقدار میں کھائیں — بڑی پلیٹ کی بجائے چھوٹی پلیٹ استعمال کریں۔",
    },
}


def get_meal_profile(
    on_insulin: bool,
    hypo_episodes: bool,
    weakness_between: bool,
    bmi: float,
    diabetes_type: str,
) -> str:
    """
    Returns the meal profile key based on clinical inputs.
    Priority order: insulin+hypo > insulin/hypo/weakness > overweight > standard.

    Clinical basis:
    - 3M_3S: ADA recommends bedtime snack for insulin users with nocturnal
             hypoglycaemia history (ADA Standards of Care 2024, Section 5)
    - 3M_2S: PES guidance for insulin users and those with inter-meal symptoms
    - SMALL_3M_1S: ADA/PES weight management for overweight South Asian Type 2
    - 3M_1S: ADA standard nutrition therapy for stable Type 2
    """
    if on_insulin and hypo_episodes:
        return "3M_3S"

    if on_insulin or hypo_episodes or weakness_between:
        return "3M_2S"

    dtype_lower = diabetes_type.strip().lower()
    if bmi and bmi >= BMI["overweight"] and "2" in dtype_lower and not on_insulin:
        return "SMALL_3M_1S"

    return "3M_1S"


APP = {
    "title":   "Apni Sehat",
    "version": "1.2.0",
    "disclaimer": (
        "This app provides general dietary information only. "
        "It does not diagnose, prescribe, or replace professional medical advice. "
        "Always follow your doctor's instructions."
    ),
}
