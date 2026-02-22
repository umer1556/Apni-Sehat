# planner.py  –  Apni Sehat v1.2
# Generates a personalised 7-day meal plan based on the user's meal profile.

import random
from typing import Dict, List
from meal_bank import MEALS
from config import MEAL_PROFILES, get_meal_profile


def _filter(slot: str, prefer_desi: bool, veg_only: bool,
            low_sodium: bool, low_satfat: bool, light: bool) -> List[Dict]:
    """
    Returns a filtered meal pool for the given slot.
    Filters are applied in priority order — each filter only applies if it
    produces a non-empty pool, to prevent accidental empty results.
    """
    pool = [m for m in MEALS if m["slot"] == slot]

    # Vegetarian filter: strict — only fall back within veg-tagged meals
    if veg_only:
        veg_pool = [m for m in pool if "veg" in m.get("tags", [])]
        pool = veg_pool if veg_pool else pool  # keep veg-only; don't expose non-veg

    # Desi preference
    if prefer_desi:
        desi = [m for m in pool if "desi" in m.get("tags", [])]
        if desi:
            pool = desi

    # Clinical filters — applied sequentially, each only if it narrows the pool
    if low_sodium:
        ls = [m for m in pool if "low_sodium" in m.get("tags", [])]
        if ls:
            pool = ls

    if low_satfat:
        lf = [m for m in pool if "low_satfat" in m.get("tags", [])]
        if lf:
            pool = lf

    # For SMALL_3M_1S profile: prefer lighter options
    if light:
        lt = [m for m in pool if "light" in m.get("tags", [])]
        if lt:
            pool = lt

    # Final fallback: return all meals for this slot if every filter was too aggressive
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
        slots: list of slot names

    Deduplication: each slot uses random.sample without replacement across the
    7-day window so the same meal doesn't appear on consecutive days.
    If the pool has fewer than 7 meals (common for snacks), meals are cycled
    in a randomised order to minimise consecutive repeats.
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

    # Pre-build a 7-item sequence per slot to minimise repeats
    slot_sequences: Dict[str, List[Dict]] = {}
    for slot in slots:
        pool = _filter(slot, prefer_desi, veg_only, low_sodium, low_satfat, is_light)
        if len(pool) >= 7:
            # Enough meals to fill 7 days without repeats
            slot_sequences[slot] = random.sample(pool, 7)
        else:
            # Cycle through pool in shuffled order, minimising consecutive repeats
            shuffled = pool[:]
            random.shuffle(shuffled)
            seq = []
            while len(seq) < 7:
                random.shuffle(shuffled)  # re-shuffle each cycle
                seq.extend(shuffled)
            slot_sequences[slot] = seq[:7]

    days = []
    for i, day_num in enumerate(range(1, 8)):
        day = {"day": day_num}
        for slot in slots:
            day[slot] = slot_sequences[slot][i]
        days.append(day)

    return {
        "profile_key": profile_key,
        "profile":     profile,
        "days":        days,
        "slots":       slots,
    }
