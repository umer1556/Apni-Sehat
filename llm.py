# llm.py  –  Apni Sehat v1.2
# Groq / LLaMA 3.3 integration.
# Three functions: chat_with_assistant, generate_swaps, coach_on_actual_meal

import json
import os
from typing import List, Dict

from openai import OpenAI


def _client():
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        return None
    return OpenAI(
        api_key=key,
        base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
    )


def _model() -> str:
    return os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def _fallback(lang: str = "en") -> List[str]:
    if lang == "ur":
        return [
            "سبزیوں کی مقدار بڑھائیں — اضافی کاربس کے بغیر پیٹ بھرتا ہے۔",
            "میدے کی روٹی کی جگہ گندم کی آٹے کی روٹی کھائیں۔",
            "میٹھے کے بغیر دہی شامل کریں — پروٹین ملتا ہے اور شوگر نہیں بڑھتی۔",
        ]
    return [
        "Increase vegetable portion to add volume without extra carbs.",
        "Choose whole wheat roti instead of white flour roti.",
        "Add a side of unsweetened yogurt for protein without sugar.",
    ]


# ── CHATBOT ───────────────────────────────────────────────────────────────────

SYSTEM = """You are Sehat Saathi (صحت ساتھی), a warm and friendly health assistant for people
with diabetes in Pakistan and South Asia.

ROLE:
- Help users understand how food affects blood sugar
- Suggest healthy desi food alternatives
- Explain blood sugar readings in plain everyday language
- Encourage healthy habits with kindness and patience
- When the user's profile is provided, personalise advice to their conditions

AUDIENCE: Elderly or non-tech-savvy users who eat desi food and may be anxious about their health.

LANGUAGE RULE (CRITICAL):
- If the user writes in Urdu → reply in Urdu script
- If the user writes in English → reply in English
- Use simple language, no medical jargon
- Be warm, like a caring family member who happens to know about health

DESI FOOD KNOWLEDGE:
- White rice / biryani: high glycemic — suggest smaller portions, add raita/salad
- Maida roti: prefer whole wheat atta roti, 1–2 medium per meal
- Daal: excellent — high protein and fibre, very good for blood sugar
- Sabzi (vegetables): great — fill half the plate at every meal
- Nihari / haleem: high fat — limit portions, skip oil pooled on top
- Karahi: often high oil — ask for less oil, add vegetables
- Sweet chai: major blood sugar spike — reduce sugar, try green tea or kawa
- Sweet lassi: high sugar — prefer salted lassi or plain yogurt
- Good fruits: guava (jamun), apple — reasonable portions
- High-sugar fruits: mango, banana, grapes — very small amounts only
- Pakoras / samosas: deep fried — avoid or have rarely in tiny amounts
- Fenugreek seeds (methi): excellent for blood sugar — add to cooking
- Lemon juice on food: lowers glycemic impact of a meal
- Roasted chana: great snack — high protein and fibre, low glycemic

HEALTHY HABITS TO RECOMMEND:
- 15-min walk after meals lowers blood sugar significantly
- Eating at regular times helps stability
- Drink water before meals to reduce overeating
- Never skip breakfast

ABSOLUTE RULES — NEVER BREAK:
1. NEVER recommend specific medications, insulin doses or prescriptions
2. NEVER provide a medical diagnosis
3. NEVER tell someone to stop or change a doctor's prescribed treatment
4. If someone reports readings above 300 mg/dL, below 60 mg/dL, chest pain,
   difficulty breathing, or loss of consciousness — immediately tell them to
   call emergency services or go to a hospital
5. Always note that guidance is for dietary awareness, not medical advice
6. Never shame users about food choices — always be encouraging and kind
7. Keep responses concise and practical — use bullet points for lists"""


def chat_with_assistant(
    messages: List[Dict[str, str]],
    lang: str = "en",
    user_profile: str = "",
) -> str:
    """
    Multi-turn bilingual chatbot.
    messages: [{"role": "user"/"assistant", "content": "..."}]
    lang: "en" or "ur"
    user_profile: optional profile context string injected silently
    """
    client = _client()
    if client is None:
        if lang == "ur":
            return "معذرت، AI سروس ابھی دستیاب نہیں۔ براہ کرم بعد میں کوشش کریں۔"
        return "Sorry, the AI service is not available right now. Please try again later."

    lang_note = (
        "\n\nThe user prefers Urdu. Always respond in Urdu script "
        "unless they write in English."
        if lang == "ur" else ""
    )

    profile_note = (
        f"\n\nUSER PROFILE (use this silently to personalise answers):\n{user_profile}"
        if user_profile else ""
    )

    try:
        resp = client.chat.completions.create(
            model=_model(),
            messages=[
                {"role": "system", "content": SYSTEM + lang_note + profile_note},
                *messages,
            ],
            temperature=0.5,
            max_tokens=600,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        if lang == "ur":
            return "معذرت، ابھی جواب نہیں مل سکا۔ دوبارہ کوشش کریں۔"
        return "Sorry, I could not get a response. Please try again."


# ── SWAP SUGGESTIONS ──────────────────────────────────────────────────────────

def generate_swaps(meal_text: str, lang: str = "en") -> List[str]:
    """
    Returns 3 healthy swap suggestions for a given meal.
    lang: "en" or "ur" — response language for suggestions
    """
    client = _client()
    if client is None:
        return _fallback(lang)

    lang_instruction = (
        "Respond in Urdu script only." if lang == "ur"
        else "Respond in English."
    )

    prompt = (
        "Return exactly 3 safe, non-medical healthy swap suggestions for the meal below. "
        "Focus on South Asian / Pakistani desi food context. "
        "No medication advice. Keep it practical and specific. "
        f"{lang_instruction} "
        "Respond ONLY as a JSON array of 3 strings, no other text.\n\n"
        f"Meal: {meal_text}"
    )
    try:
        resp = client.chat.completions.create(
            model=_model(),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        raw  = (resp.choices[0].message.content or "").strip()
        raw  = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data[:3]
    except Exception:
        pass
    return _fallback(lang)


# ── DEVIATION COACHING ────────────────────────────────────────────────────────

def coach_on_actual_meal(actual_meal_text: str, lang: str = "en") -> List[str]:
    """
    Friendly coaching when a user deviated from their plan.
    lang: "en" or "ur" — response language for coaching tips
    """
    client = _client()
    if client is None:
        return _fallback(lang)

    lang_instruction = (
        "Respond in Urdu script only." if lang == "ur"
        else "Respond in English."
    )

    prompt = (
        "A diabetes patient ate these foods instead of their plan. "
        "Give exactly 3 kind, practical tips on portion control, carb awareness, "
        "and healthier preparation for South Asian foods. "
        "No medication advice. Be encouraging, not judgmental. "
        f"{lang_instruction} "
        "Respond ONLY as a JSON array of 3 strings, no other text.\n\n"
        f"Foods eaten: {actual_meal_text}"
    )
    try:
        resp = client.chat.completions.create(
            model=_model(),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        raw  = (resp.choices[0].message.content or "").strip()
        raw  = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data[:3]
    except Exception:
        pass
    return _fallback(lang)
