# planner.py  –  Apni Sehat v1.2
# Generates a personalised 7-day meal plan based on the user's meal profile.

import random
from typing import Dict, List
from meal_bank import MEALS
from config import MEAL_PROFILES, get_meal_profile


def _filter(slot: str, prefer_desi: bool, veg_only: bool,
            low_sodium: bool, low_satfat: bool, light: bool) -> List[Dict]:
    pool = [m for m in MEALS if m["slot"] == slot]

    if veg_only:
        pool = [m for m in pool if "veg" in m.get("tags", [])] or pool

    if prefer_desi:
        desi = [m for m in pool if "desi" in m.get("tags", [])]
        if desi:
            pool = desi

    if low_sodium:
        ls = [m for m in pool if "low_sodium" in m.get("tags", [])]
        if ls:
            pool = ls

    if low_satfat:
        lf = [m for m in pool if "low_satfat" in m.get("tags", [])]
        if lf:
            pool = lf

    # For SMALL profile, prefer lighter options when available
    if light:
        lt = [m for m in pool if "light" in m.get("tags", [])]
        if lt:
            pool = lt

    return pool or [m for m in MEALS if m["slot"] == slot]


def generate_week_plan(
    prefer_desi: bool = True,
    veg_only: bool = False,
    has_hypertension: bool = False,
    has_high_cholesterol: bool = False,
    on_insulin: bool = False,
    hypo_episodes: bool = False,
    weakness_between: bool = False,
    bmi: float = None,
    diabetes_type: str = "Type 2",
) -> Dict:
    """
    Returns a dict with:
        profile_key: str
        profile: dict (from MEAL_PROFILES)
        days: list of 7 day dicts, each with meals keyed by slot name
    """
    profile_key = get_meal_profile(
        on_insulin=on_insulin,
        hypo_episodes=hypo_episodes,
        weakness_between=weakness_between,
        bmi=bmi or 0,
        diabetes_type=diabetes_type,
    )
    profile  = MEAL_PROFILES[profile_key]
    slots    = profile["slots"]
    is_light = profile_key == "SMALL_3M_1S"

    low_sodium  = has_hypertension
    low_satfat  = has_high_cholesterol

    days = []
    for day_num in range(1, 8):
        day = {"day": day_num}
        for slot in slots:
            day[slot] = random.choice(
                _filter(slot, prefer_desi, veg_only, low_sodium, low_satfat, is_light)
            )
        days.append(day)

    return {
        "profile_key": profile_key,
        "profile":     profile,
        "days":        days,
        "slots":       slots,
    }
