# app.py  –  Apni Sehat v1.2
import os, re, hashlib
from datetime import datetime, date
from typing import List, Optional

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from config import APP, CARB, TRIAGE
from triage import triage_profile
from planner import generate_week_plan
from llm import generate_swaps, coach_on_actual_meal, chat_with_assistant
from translations import T, get_tip

st.set_page_config(
    page_title="Apni Sehat — اپنی صحت",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Secrets ───────────────────────────────────────────────────────────────────
def _sget(k, d=""):
    try:    return str(st.secrets.get(k, d)).strip()
    except: return d

os.environ["GROQ_API_KEY"]  = _sget("GROQ_API_KEY",  os.getenv("GROQ_API_KEY",  ""))
os.environ["GROQ_BASE_URL"] = _sget("GROQ_BASE_URL", os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"))
os.environ["GROQ_MODEL"]    = _sget("GROQ_MODEL",    os.getenv("GROQ_MODEL",    "llama-3.3-70b-versatile"))
os.environ["DATABASE_URL"]  = _sget("DATABASE_URL",  os.getenv("DATABASE_URL",  ""))
os.environ["PHONE_SALT"]    = _sget("PHONE_SALT",    os.getenv("PHONE_SALT",    "dev-salt-change-me"))

from storage import (init_db, get_profile, upsert_profile,
                     add_glucose_log, fetch_glucose_logs,
                     add_daily_checkin, fetch_checkins)
init_db()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');

:root {
    --bg:      #0d1117;
    --bg2:     #161b22;
    --bg3:     #21262d;
    --border:  #30363d;
    --green:   #3fb950;
    --green2:  #2ea043;
    --green-t: rgba(63,185,80,0.15);
    --amber:   #d29922;
    --red:     #f85149;
    --blue:    #58a6ff;
    --txt:     #e6edf3;
    --txt2:    #8b949e;
    --txt3:    #9ca3af;
    --shadow:  rgba(0,0,0,0.4);
    color-scheme: dark light;
}
@media (prefers-color-scheme: light) {
    :root {
        --bg:      #ffffff; --bg2: #f6f8fa; --bg3: #eaeef2; --border: #d0d7de;
        --green:   #1a7f37; --green2: #2da44e; --green-t: rgba(26,127,55,0.1);
        --amber:   #9a6700; --red: #cf222e; --blue: #0969da;
        --txt:     #1f2328; --txt2: #57606a; --txt3: #6e7781;
        --shadow:  rgba(0,0,0,0.12); color-scheme: light;
    }
}
html { color-scheme: dark light; }
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="block-container"],
div.block-container, .main {
    background: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--txt) !important;
}
[data-testid="stChatInput"], [data-testid="stChatInputContainer"],
[data-testid="stChatInputContainer"] > div,
[data-testid="stChatInputContainer"] textarea {
    background: var(--bg3) !important; color: var(--txt) !important; border-color: var(--border) !important;
}
[data-testid="stChatInputContainer"] textarea::placeholder { color: var(--txt3) !important; opacity: 1 !important; }
[data-testid="stChatInputContainer"] button { background: var(--green2) !important; color: #fff !important; border: none !important; }
[data-testid="stBottom"], [data-testid="stBottom"] > div {
    background: var(--bg) !important; border-top: 1px solid var(--border) !important;
}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background: var(--bg2) !important; border-right: 1px solid var(--border) !important;
}
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li,
[data-testid="stCaptionContainer"] p, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] li, [data-testid="stSidebar"] label {
    font-family: 'Inter', sans-serif !important; color: var(--txt) !important;
}
[data-testid="stMarkdownContainer"] p, [data-testid="stSidebar"] p { font-size: 1.08rem !important; line-height: 1.85 !important; }
[data-testid="stCaptionContainer"] p { font-size: 0.95rem !important; color: var(--txt3) !important; line-height: 1.75 !important; }
[data-testid="stMarkdownContainer"] h1 { font-size: 2.3rem !important; font-weight: 800 !important; color: var(--green) !important; letter-spacing: -0.5px !important; }
[data-testid="stMarkdownContainer"] h2 { font-size: 1.55rem !important; font-weight: 700 !important; color: var(--green) !important; }
[data-testid="stMarkdownContainer"] h3 { font-size: 1.25rem !important; font-weight: 700 !important; color: var(--txt) !important; }
.stTabs [data-baseweb="tab-list"] { background: var(--bg2) !important; border-bottom: 1px solid var(--border) !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: var(--txt2) !important;
    font-family: 'Inter', sans-serif !important; font-size: 1rem !important; font-weight: 600 !important;
    padding: 12px 20px !important; border-bottom: 2px solid transparent !important; min-height: 48px !important;
}
.stTabs [aria-selected="true"] { color: var(--green) !important; border-bottom-color: var(--green) !important; }
.stTabs [data-baseweb="tab-panel"] { background: var(--bg) !important; padding-top: 24px !important; }
.stButton > button {
    font-family: 'Inter', sans-serif !important; font-size: 1.05rem !important; font-weight: 600 !important;
    border-radius: 6px !important; min-height: 46px !important; padding: 0.6rem 1.3rem !important;
    transition: all 0.15s ease !important; background: var(--bg3) !important;
    color: var(--txt) !important; border: 1px solid var(--border) !important;
}
.stButton > button:hover { background: var(--bg2) !important; border-color: var(--green) !important; color: var(--green) !important; }
.stButton > button[kind="primary"] { background: var(--green2) !important; color: #fff !important; border: none !important; font-weight: 700 !important; }
.stButton > button[kind="primary"]:hover { background: var(--green) !important; transform: translateY(-1px) !important; box-shadow: 0 4px 14px var(--green-t) !important; }
.stButton > button:focus, .stButton > button:focus-visible { outline: none !important; box-shadow: none !important; }
.stButton > button[kind="primary"]:focus, .stButton > button[kind="primary"]:focus-visible { outline: none !important; box-shadow: 0 4px 14px var(--green-t) !important; }
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea,
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: var(--bg3) !important; color: var(--txt) !important;
    border: 1px solid var(--border) !important; border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important; font-size: 1.05rem !important;
}
[data-baseweb="input"] input:focus, [data-baseweb="textarea"] textarea:focus { border-color: var(--green) !important; box-shadow: 0 0 0 3px var(--green-t) !important; }
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stDateInput label, .stTimeInput label,
.stRadio legend, .stCheckbox label, .stToggle label, .stMultiSelect label {
    color: var(--txt2) !important; font-size: 0.9rem !important; font-weight: 600 !important;
    letter-spacing: 0.04em !important; text-transform: uppercase !important;
}
[data-baseweb="select"] > div { background: var(--bg3) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; color: var(--txt) !important; }
[data-baseweb="popover"] [role="listbox"], [data-baseweb="menu"] { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; }
[data-baseweb="menu"] li { color: var(--txt) !important; font-size: 1.05rem !important; }
[data-baseweb="menu"] li:hover { background: var(--bg3) !important; }
.stRadio [role="radiogroup"] label, .stCheckbox label, .stToggle label {
    color: var(--txt) !important; font-size: 1.05rem !important; font-weight: 400 !important;
    text-transform: none !important; letter-spacing: 0 !important;
}
[data-testid="stMetric"] { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; padding: 16px 20px !important; }
[data-testid="stMetricValue"] { font-family: 'Inter', sans-serif !important; font-size: 2rem !important; font-weight: 800 !important; color: var(--green) !important; }
[data-testid="stMetricLabel"] { font-family: 'Inter', sans-serif !important; color: var(--txt2) !important; font-size: 0.88rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }
[data-testid="stSuccess"] { background: var(--green-t) !important; border-left: 3px solid var(--green) !important; border-radius: 6px !important; }
[data-testid="stInfo"]    { background: rgba(88,166,255,0.1) !important; border-left: 3px solid var(--blue) !important; border-radius: 6px !important; }
[data-testid="stWarning"] { background: rgba(210,153,34,0.1) !important; border-left: 3px solid var(--amber) !important; border-radius: 6px !important; }
[data-testid="stError"]   { background: rgba(248,81,73,0.1) !important; border-left: 3px solid var(--red) !important; border-radius: 6px !important; }
[data-testid="stSuccess"] p, [data-testid="stSuccess"] li,
[data-testid="stInfo"] p, [data-testid="stInfo"] li,
[data-testid="stWarning"] p, [data-testid="stWarning"] li,
[data-testid="stError"] p, [data-testid="stError"] li { color: var(--txt) !important; }
[data-testid="stExpander"] { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }
[data-testid="stExpander"] summary { padding: 12px 16px !important; }
[data-testid="stExpander"] summary:hover { background: var(--bg3) !important; border-radius: 8px !important; }
[data-testid="stExpander"] > div > div { background: var(--bg2) !important; padding: 12px 16px !important; }
[data-testid="stDataFrame"] { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }
input[type="date"], input[type="time"] { background: var(--bg3) !important; color: var(--txt) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; }
.stNumberInput button { background: var(--bg3) !important; border-color: var(--border) !important; color: var(--txt2) !important; }
hr { border-color: var(--border) !important; }
[data-testid="stSpinner"] p { color: var(--green) !important; }
[data-baseweb="tag"] { background: var(--green-t) !important; color: var(--green) !important; }

.tip-banner { background: var(--green-t); border: 1px solid var(--green2); border-radius: 10px; padding: 16px 20px; margin-bottom: 18px; font-family: 'Inter', sans-serif; font-size: 1.08rem; line-height: 1.85; color: var(--txt); }
.tip-label { font-family: 'Inter', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--green); margin-bottom: 6px; display: block; }
.profile-card { background: var(--bg2); border: 1px solid var(--border); border-left: 3px solid var(--green); border-radius: 8px; padding: 14px 20px; margin-bottom: 16px; font-family: 'Inter', sans-serif; }
.profile-name   { font-size: 1.2rem; font-weight: 700; color: var(--txt); }
.profile-detail { font-size: 0.98rem; color: var(--txt2); margin-top: 3px; }
.badge-g { background: var(--green-t); color: var(--green); border: 1px solid var(--green2); border-radius: 5px; padding: 2px 10px; font-weight: 700; font-size: 0.9rem; display: inline-block; font-family: 'Inter', sans-serif; }
.badge-a { background: rgba(210,153,34,0.1); color: var(--amber); border: 1px solid var(--amber); border-radius: 5px; padding: 2px 10px; font-weight: 700; font-size: 0.9rem; display: inline-block; font-family: 'Inter', sans-serif; }
.badge-r { background: rgba(248,81,73,0.1); color: var(--red); border: 1px solid var(--red); border-radius: 5px; padding: 2px 10px; font-weight: 700; font-size: 0.9rem; display: inline-block; font-family: 'Inter', sans-serif; }
.badge-n { background: var(--bg3); color: var(--txt3); border: 1px solid var(--border); border-radius: 5px; padding: 2px 10px; font-weight: 700; font-size: 0.9rem; display: inline-block; font-family: 'Inter', sans-serif; }
.bubble-user { background: var(--green-t); border: 1px solid var(--green2); border-radius: 12px 12px 3px 12px; padding: 12px 16px; margin: 6px 0; margin-left: 8%; font-family: 'Inter', sans-serif; font-size: 1.05rem; line-height: 1.85; color: var(--txt); }
.bubble-bot { background: var(--bg2); border: 1px solid var(--border); border-radius: 12px 12px 12px 3px; padding: 12px 16px; margin: 6px 0; margin-right: 8%; font-family: 'Inter', sans-serif; font-size: 1.05rem; line-height: 1.85; color: var(--txt); }
.bubble-label { font-family: 'Inter', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--txt3); margin-bottom: 3px; }
.wizard-box { background: var(--bg2); border: 1px solid var(--border); border-top: 3px solid var(--green); border-radius: 10px; padding: 28px 32px; margin: 0 auto; max-width: 560px; font-family: 'Inter', sans-serif; }
.step-pill { background: var(--green-t); color: var(--green); border: 1px solid var(--green2); border-radius: 20px; padding: 3px 12px; font-size: 0.73rem; font-weight: 700; display: inline-block; margin-bottom: 12px; font-family: 'Inter', sans-serif; }
.feature-card { background: var(--bg2); border: 1px solid var(--border); border-radius: 10px; padding: 22px 24px; height: 100%; font-family: 'Inter', sans-serif; }
.sb-disc { background: rgba(210,153,34,0.08); border: 1px solid var(--amber); border-left: 3px solid var(--amber); border-radius: 6px; padding: 10px 12px; margin-top: 4px; font-family: 'Inter', sans-serif; }
.sb-disc-title { font-size: 0.92rem; font-weight: 700; color: var(--amber); margin-bottom: 4px; font-family: 'Inter', sans-serif; }
.meal-card { background: var(--bg); border: 1px solid var(--border); border-left: 3px solid var(--green); border-radius: 8px; padding: 14px 18px; margin-bottom: 10px; }
.meal-card-slot { font-family: 'Inter', sans-serif; font-size: 0.8rem; font-weight: 700; color: var(--green); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
.meal-card-name { font-family: 'Inter', sans-serif; font-size: 1.08rem; font-weight: 700; color: var(--txt); margin-bottom: 4px; }
.meal-card-note { font-family: 'Inter', sans-serif; font-size: 0.88rem; color: var(--txt3); line-height: 1.6; }
.section-label { font-family: 'Inter', sans-serif; font-size: 0.82rem; font-weight: 700; color: var(--txt3); text-transform: uppercase; letter-spacing: 0.1em; border-bottom: 1px solid var(--border); padding-bottom: 5px; margin-bottom: 12px; }
.login-hero { text-align: center; padding: 48px 20px 28px; }
.login-hero-logo { font-family: 'Inter', sans-serif; font-size: 4rem; font-weight: 900; color: var(--green); letter-spacing: -2px; line-height: 1; display: block; }
.login-hero-urdu { font-size: 2.2rem; color: var(--green); font-weight: 700; display: block; margin-top: 4px; }
.login-hero-sub  { font-family: 'Inter', sans-serif; font-size: 1.15rem; color: var(--txt2); margin-top: 10px; display: block; }
.footer { font-family: 'Inter', sans-serif; font-size: 0.88rem; color: var(--txt3); text-align: center; padding: 10px 0; border-top: 1px solid var(--border); margin-top: 28px; }
</style>
""", unsafe_allow_html=True)

ss = st.session_state

# ── Triage flag translations — exact strings produced by triage.py ────────────
_FLAG_UR = {
    # RED
    "Other major conditions selected. Please consult a clinician before using this app for dietary changes.":
        "دیگر بڑی بیماریاں منتخب کی گئی ہیں۔ خوراک میں تبدیلی سے پہلے ڈاکٹر سے مشورہ کریں۔",
    "Blood pressure is in a severe range. Please seek urgent medical care.":
        "بلڈ پریشر بہت زیادہ ہے۔ فوری طبی مدد حاصل کریں۔",
    "HbA1c is very high. Please see a clinician before making dietary changes.":
        "HbA1c بہت زیادہ ہے۔ خوراک میں تبدیلی سے پہلے ڈاکٹر سے ملیں۔",
    "Very high fasting glucose recorded. Please seek medical advice.":
        "بہت زیادہ فاسٹنگ گلوکوز ریکارڈ ہوئی۔ ڈاکٹر سے مشورہ کریں۔",
    "Large variation in recent fasting readings — please see a clinician.":
        "حالیہ فاسٹنگ ریڈنگز میں بہت زیادہ فرق — ڈاکٹر سے ملیں۔",
    # AMBER
    "Type 1 diabetes: this app provides dietary support only — never adjust insulin or medication based on this app.":
        "قسم 1 ذیابیطس: یہ ایپ صرف خوراک کی رہنمائی دیتی ہے — اس ایپ کی بنیاد پر انسولین یا دوا کبھی تبدیل نہ کریں۔",
    "Blood pressure is elevated. Clinician follow-up recommended.":
        "بلڈ پریشر بڑھا ہوا ہے۔ ڈاکٹر سے فالو اپ کریں۔",
    "Hypertension selected but BP values not provided — proceed with care.":
        "ہائی بلڈ پریشر بتایا گیا لیکن قدریں نہیں دی گئیں — احتیاط سے آگے بڑھیں۔",
    "Total cholesterol is high — a heart-healthy plan is recommended. Please follow up with your doctor.":
        "کل کولیسٹرول زیادہ ہے — دل کے لیے صحت مند منصوبہ تجویز ہے۔ ڈاکٹر سے فالو اپ کریں۔",
    "Total cholesterol is borderline high — heart-healthy plan applied.":
        "کل کولیسٹرول حد پر ہے — دل کے لیے صحت مند منصوبہ لاگو کیا گیا۔",
    "High cholesterol selected but value not provided — proceed with care.":
        "زیادہ کولیسٹرول بتایا گیا لیکن قدر نہیں دی گئی — احتیاط سے آگے بڑھیں۔",
    "HbA1c is above the safe threshold — proceed with care and follow up with your doctor promptly.":
        "HbA1c محفوظ حد سے اوپر ہے — احتیاط سے آگے بڑھیں اور جلد ڈاکٹر سے ملیں۔",
    "HbA1c is above the typical target of 7.0%. Focus on consistency and follow up with your doctor.":
        "HbA1c عام ہدف 7.0٪ سے اوپر ہے۔ باقاعدگی پر توجہ دیں اور ڈاکٹر سے ملیں۔",
    "Low fasting glucose detected — discuss with your clinician.":
        "کم فاسٹنگ گلوکوز ملی — اپنے ڈاکٹر سے بات کریں۔",
    "Recent fasting readings show variability or are above target — proceed with care.":
        "حالیہ فاسٹنگ ریڈنگز میں اتار چڑھاؤ یا ہدف سے زیادہ ہیں — احتیاط سے آگے بڑھیں۔",
    "No A1c or fasting readings provided — proceeding with a cautious plan. Consider sharing test results for a more accurate assessment.":
        "HbA1c یا فاسٹنگ ریڈنگز نہیں دی گئیں — احتیاطی منصوبے کے ساتھ آگے بڑھ رہے ہیں۔ بہتر جائزے کے لیے ٹیسٹ کے نتائج شامل کریں۔",
    # Wizard unconfirmed flags
    "Diabetes status unconfirmed — please get a fasting blood sugar test.":
        "ذیابیطس کی تصدیق نہیں — براہ کرم فاسٹنگ بلڈ شوگر ٹیسٹ کروائیں۔",
    "Following a cautious low-GI plan until diagnosis is confirmed.":
        "تشخیص کی تصدیق تک احتیاطی کم GI منصوبہ دیا جا رہا ہے۔",
}

def _translate_flag(f):
    return _FLAG_UR.get(f, f) if _lang() == "ur" else f

# ── LLM caller ────────────────────────────────────────────────────────────────
def _call_llm(system, user, max_tokens=400):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("GROQ_API_KEY",""), base_url=os.getenv("GROQ_BASE_URL","https://api.groq.com/openai/v1"))
        resp = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL","llama-3.3-70b-versatile"),
            messages=[{"role":"system","content":system},{"role":"user","content":user}],
            max_tokens=max_tokens, temperature=0.4)
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[AI unavailable: {e}]"

# ── RAG KB ────────────────────────────────────────────────────────────────────
_RAG_KB = {
    "carbohydrates": {"keywords":["carb","carbohydrate","sugar","glucose","roti","rice","bread","atta","starch","grams"],"source":"ADA Standards of Care 2024 — Nutrition","text":"ADA: No single ideal carb percentage for diabetes. Focus on quality — high-fibre, low-processed sources. 45–60g carbs per meal is a practical starting point for most adults with Type 2. Low-GI foods (GI<55) blunt post-meal spikes. Atta roti GI≈62, white rice GI≈72, dalia GI≈41."},
    "gi_desi_foods": {"keywords":["biryani","roti","rice","chapati","naan","paratha","daal","chana","gi","glycaemic","glycemic","lentil"],"source":"GI/GL values — Foster-Powell et al. + Pakistan NCD Guidelines","text":"South Asian GI values: basmati rice 58, biryani ≈70, atta roti 62, naan 71, paratha 74, daal maash 30, chana 28, rajma 29, moong daal 38. Legumes are excellent — low GI, high fibre, high protein."},
    "portion_control": {"keywords":["portion","serving","how much","quantity","katori","plate","too much","cup"],"source":"WHO South Asia Dietary Guidelines + ADA Plate Method","text":"Diabetes Plate: half non-starchy vegetables, quarter lean protein, quarter quality carbs. 1 medium atta roti ≈ 15g carbs. 1 katori (150ml) cooked rice ≈ 30g carbs. Target 2–4 carb servings per meal depending on meal frequency profile."},
    "hypertension": {"keywords":["blood pressure","bp","hypertension","sodium","salt","namak","salty","heart"],"source":"DASH Diet + Pakistan Hypertension Guidelines","text":"DASH diet strongly recommended for diabetes+hypertension. Limit sodium <2300mg/day (~1 tsp salt). Avoid achar, papad, processed chutneys. Increase potassium: spinach, tomatoes, daal, yogurt. Every 10mmHg systolic reduction cuts cardiovascular risk ~20%."},
    "cholesterol": {"keywords":["cholesterol","fat","ghee","oil","fried","saturated","lipid","heart","cardiovascular"],"source":"ADA/AHA Joint Guidelines + Pakistan NCD Guidelines","text":"Limit saturated fat <7% of calories. Replace ghee/butter with small amounts of olive or canola oil. Limit fried foods. Each 5–10g increase in soluble fibre (oats, isabgol, daal) reduces LDL ~5%. Fish 2–3x/week for omega-3. Choose low-fat dairy."},
    "fasting_targets": {"keywords":["fasting","morning","waking","empty stomach","before breakfast","HbA1c","a1c","target","range"],"source":"ADA Standards of Care 2024 — Glycaemic Targets","text":"ADA targets: fasting/pre-meal 80–130 mg/dL, post-meal <180 mg/dL, HbA1c <7% for most adults. A1c of 7% = average glucose ~154 mg/dL. Each 1% A1c reduction cuts microvascular complication risk ~37%."},
    "hypoglycaemia": {"keywords":["low sugar","hypo","shakiness","dizzy","sweating","low blood","under 70","below 70","hypoglycemia"],"source":"ADA Hypoglycaemia Management Guidelines","text":"Hypoglycaemia: blood glucose <70 mg/dL. Symptoms: shakiness, sweating, dizziness, confusion. Rule of 15: 15g fast carbs (3–4 glucose tablets or 3 tsp sugar in water), wait 15 min, recheck. Follow with snack if next meal >1 hour away."},
    "exercise": {"keywords":["exercise","walk","walking","physical activity","gym","sport","movement","active","workout"],"source":"ADA Physical Activity Guidelines 2024","text":"ADA: 150 min/week moderate aerobic (brisk walking) for Type 2 diabetes. 10–15 min walk after each meal significantly reduces post-meal glucose spikes. South Asian context: morning walks after Fajr prayer are culturally aligned and clinically effective."},
    "ramadan": {"keywords":["ramadan","roza","fast","iftar","sehri","suhoor","fasting month"],"source":"IDF-DAR Diabetes and Ramadan Guidelines","text":"Type 2 on diet/metformin alone can usually fast safely with planning. Those on insulin face hypo risk — must consult doctor. Sehri: dalia, eggs, daal, atta roti — avoid sugary drinks. Break fast immediately if glucose <70 or >300 mg/dL."},
    "desi_safe_foods": {"keywords":["karela","bhindi","methi","daal","chana","moong","spinach","palak","yogurt","dahi","guava","amrood"],"source":"Diabetes-Friendly South Asian Foods — Clinical Review","text":"Karela: charantin has blood-glucose-lowering properties. Bhindi: high soluble fibre, slows carb absorption. Methi dana: reduces fasting glucose and improves insulin sensitivity. Plain dahi: low GI, high protein — no added sugar. Guava (amrood): GI 12 — one of the best fruits for diabetes."},
    "insulin_diet": {"keywords":["insulin","injection","dose","units","pen","basal","bolus","on insulin","taking insulin"],"source":"ADA Insulin Management + Dietary Coordination","text":"Meal timing is critical on insulin. Never skip a meal after taking insulin. Fixed insulin doses require consistent carb amounts at each meal daily. Bedtime snack essential to prevent overnight lows: warm low-fat milk, yogurt+nuts, or 2 crackers+peanut butter. Always carry fast-acting glucose."},
}

def _rag_retrieve(query, top_k=2):
    q = query.lower()
    scored = sorted([(sum(1 for kw in c["keywords"] if kw in q), k, c) for k,c in _RAG_KB.items() if any(kw in q for kw in c["keywords"])], key=lambda x: -x[0])
    return [{"source":c["source"],"text":c["text"]} for _,_,c in scored[:top_k]]

def normalize_phone(p): return re.sub(r"[^\d+]","",p.strip())
def user_key_from_phone(p):
    salt = os.getenv("PHONE_SALT","dev-salt-change-me")
    return hashlib.sha256((salt+p).encode()).hexdigest()
def last4(p):
    d = re.sub(r"\D","",p)
    return d[-4:] if len(d)>=4 else d

def _lang():  return ss.get("lang","en")
def t(k):     return T[_lang()].get(k, T["en"].get(k,k))
def _get_user():     return ss.get("user_key","").strip()
def _triage_level(): return ss.get("triage_level")
def _blocked():      return _triage_level()=="RED"
def _parse_fastings(v): return [x for x in v if x and x>0]

def _lang_toggle(suffix=""):
    lbl = "🌐 اردو" if _lang()=="en" else "🌐 English"
    if st.button(lbl, key=f"lt_{suffix}_{ss.get('_lc',0)}"):
        ss["lang"] = "ur" if _lang()=="en" else "en"
        ss["_lc"]  = ss.get("_lc",0)+1
        ss["current_tip"] = get_tip(_lang())
        st.rerun()

def _profile_context():
    p = []
    for k,v in [("name",ss.get("name")),("age",ss.get("age")),("diabetes_type",ss.get("diabetes_type"))]:
        if v: p.append(f"{k}: {v}")
    if ss.get("has_hypertension"):     p.append("hypertension")
    if ss.get("has_high_cholesterol"): p.append("high cholesterol")
    if ss.get("triage_level"):         p.append(f"triage: {ss['triage_level']}")
    plan = ss.get("week_plan")
    if plan:
        days  = plan.get("days",[]) if isinstance(plan,dict) else plan
        slots = plan.get("slots",["breakfast","lunch","dinner"]) if isinstance(plan,dict) else ["breakfast","lunch","dinner"]
        if days:
            d1 = days[0]
            p.append("today: "+", ".join(f"{s}={d1[s]['name']}" for s in slots if s in d1))
    return " | ".join(p)

def _run_triage(dtype,hy,ch,bp_sys=None,bp_dia=None,a1c=None,fasting_readings=None,total_chol=None,other_major=False):
    lv,fl = triage_profile(diabetes_type=dtype,has_hypertension=hy,has_high_cholesterol=ch,bp_sys=bp_sys,bp_dia=bp_dia,a1c=a1c,fasting_readings=fasting_readings or [],total_cholesterol=total_chol,other_major_conditions=other_major)
    ss["triage_level"]=lv; ss["triage_flags"]=fl
    return lv,fl

def _plan_days():
    p=ss.get("week_plan"); return p.get("days",[]) if isinstance(p,dict) else (p or [])
def _plan_slots():
    p=ss.get("week_plan"); return p.get("slots",["breakfast","lunch","dinner","snack"]) if isinstance(p,dict) else ["breakfast","lunch","dinner","snack"]
def _plan_profile():
    p=ss.get("week_plan"); return p.get("profile") if isinstance(p,dict) else None

_NOTES_UR = {
    "High protein and fibre. Very gentle on blood sugar.":"زیادہ پروٹین اور فائبر۔ بلڈ شوگر کے لیے بہت محفوظ۔",
    "No sugar. A few almonds add healthy fat and slow sugar absorption.":"چینی نہیں۔ چند بادام صحت مند چکنائی دیتے اور شوگر جذب کو سست کرتے ہیں۔",
    "No sugar. Pinch of cinnamon helps blood sugar. Use water or low-fat milk.":"چینی نہیں۔ دار چینی بلڈ شوگر میں مدد کرتی ہے۔ پانی یا کم چکنائی والا دودھ استعمال کریں۔",
    "Boil or poach eggs. Tomato and cucumber on the side.":"انڈے ابالیں یا پوچ کریں۔ ساتھ ٹماٹر اور کھیرا۔",
    "Very little oil. Yogurt adds protein. No butter or ghee on top.":"بہت کم تیل۔ دہی پروٹین دیتا ہے۔ اوپر سے مکھن یا گھی نہیں۔",
    "High protein, slow-digesting. Keeps you full longer.":"زیادہ پروٹین، آہستہ ہضم ہوتا ہے۔ دیر تک پیٹ بھرا رہتا ہے۔",
    "High fibre, low GI. Add nuts for protein.":"زیادہ فائبر، کم GI۔ گری دار میوے شامل کریں۔",
    "Complex carbs + protein combo. Slow glucose release.":"پیچیدہ کاربس اور پروٹین۔ شوگر آہستہ آہستہ بڑھتی ہے۔",
    "Very low GI. High protein. Filling and blood-sugar friendly.":"بہت کم GI۔ زیادہ پروٹین۔ پیٹ بھرنے والا اور بلڈ شوگر کے لیے اچھا۔",
    "Good fats + protein. Very low carb impact.":"اچھی چکنائی اور پروٹین۔ کاربس کا بہت کم اثر۔",
    "Low GI, high fibre. Very filling.":"کم GI، زیادہ فائبر۔ بہت پیٹ بھرنے والا۔",
    "Anti-inflammatory. Good fat. Very low carb.":"سوزش کم کرتا ہے۔ اچھی چکنائی۔ کاربس بہت کم۔",
    "High protein, no carbs. Very blood-sugar safe.":"زیادہ پروٹین، کاربس نہیں۔ بلڈ شوگر کے لیے بالکل محفوظ۔",
    "Slow digesting protein + fat. No sugar spike.":"آہستہ ہضم ہونے والا پروٹین اور چکنائی۔ شوگر نہیں بڑھتی۔",
    "Low GI. High protein and fibre.":"کم GI۔ زیادہ پروٹین اور فائبر۔",
    "Good fats, fibre, very low GI. A handful only.":"اچھی چکنائی، فائبر، بہت کم GI۔ صرف ایک مٹھی۔",
    "Low GI fruit. High fibre. Rich in vitamin C.":"کم GI پھل۔ زیادہ فائبر۔ وٹامن سی سے بھرپور۔",
    "Low GI. Filling. Good for blood sugar.":"کم GI۔ پیٹ بھرنے والا۔ بلڈ شوگر کے لیے اچھا۔",
    "Cooling, filling and blood-sugar friendly.":"ٹھنڈا، پیٹ بھرنے والا اور بلڈ شوگر کے لیے اچھا۔",
    "Low GI. Rich in antioxidants and fibre.":"کم GI۔ اینٹی آکسیڈینٹس اور فائبر سے بھرپور۔",
    "Low GI. Good fats. Heart healthy.":"کم GI۔ اچھی چکنائی۔ دل کے لیے فائدہ مند۔",
    "Complex carbs + protein. Prevents overnight dip.":"پیچیدہ کاربس اور پروٹین۔ رات میں شوگر گرنے سے بچاتا ہے۔",
    "Slow protein. Bedtime safe for insulin users.":"آہستہ پروٹین۔ انسولین استعمال کرنے والوں کے لیے سونے سے پہلے محفوظ۔",
    "Protein + fat. Stable overnight glucose.":"پروٹین اور چکنائی۔ رات بھر شوگر مستحکم رکھتا ہے۔",
    "Chickpeas are excellent for blood sugar. Avoid too much oil.":"چنے بلڈ شوگر کے لیے بہترین ہیں۔ زیادہ تیل سے بچیں۔",
    "Legumes lower blood sugar. Keep roti to 1 medium.":"دالیں بلڈ شوگر کم کرتی ہیں۔ روٹی ایک درمیانی رکھیں۔",
    "Low GI daal. Protein rich. Avoid heavy tarka.":"کم GI دال۔ پروٹین سے بھرپور۔ بھاری تڑکے سے بچیں۔",
    "Excellent protein and fibre. Low GI.":"بہترین پروٹین اور فائبر۔ کم GI۔",
    "Excellent blood sugar control. Avoid too much ghee.":"بلڈ شوگر کنٹرول کے لیے بہترین۔ زیادہ گھی سے بچیں۔",
    "High protein. No carb impact. Ask for less oil.":"زیادہ پروٹین۔ کاربس کا اثر نہیں۔ کم تیل مانگیں۔",
    "Ask for less oil. Atta roti instead of naan.":"کم تیل مانگیں۔ نان کی جگہ آٹے کی روٹی لیں۔",
    "Lean protein. Low carb. Blood-sugar safe.":"دبلا پروٹین۔ کاربس کم۔ بلڈ شوگر کے لیے محفوظ۔",
    "High protein, very low GI. Filling dinner.":"زیادہ پروٹین، بہت کم GI۔ پیٹ بھرنے والا رات کا کھانا۔",
    "Iron + folate + protein. Blood sugar friendly.":"آئرن، فولیٹ اور پروٹین۔ بلڈ شوگر کے لیے فائدہ مند۔",
    "Very low GI. High fibre. Anti-inflammatory.":"بہت کم GI۔ زیادہ فائبر۔ سوزش کم کرتا ہے۔",
    "Rice is high GI — keep to half katori. Add raita.":"چاول زیادہ GI والے ہیں — آدھی کٹوری رکھیں۔ رائتہ شامل کریں۔",
    "Omega-3 + protein. Heart and blood-sugar friendly.":"اومیگا-3 اور پروٹین۔ دل اور بلڈ شوگر کے لیے فائدہ مند۔",
    "Bitter melon lowers blood sugar naturally.":"کریلا قدرتی طور پر بلڈ شوگر کم کرتا ہے۔",
    "Okra has blood sugar lowering properties.":"بھنڈی بلڈ شوگر کم کرنے کی خاصیت رکھتی ہے۔",
    "Zero-carb snack — protein keeps you full without spiking sugar.":"کاربس نہیں — پروٹین شوگر بڑھائے بغیر پیٹ بھرتا ہے۔",
    "High protein and fibre. Roasted, not fried.":"زیادہ پروٹین اور فائبر۔ بھنے ہوئے، تلے ہوئے نہیں۔",
    "Probiotic + healthy fat. Flaxseeds add fibre and omega-3.":"پروبائیوٹک اور صحت مند چکنائی۔ السی فائبر اور اومیگا-3 دیتی ہے۔",
    "Guava is one of the best fruits for diabetics. Almonds slow sugar absorption.":"امرود ذیابیطس کے مریضوں کے لیے بہترین پھل ہے۔ بادام شوگر جذب کو سست کرتے ہیں۔",
    "Salted lassi only — no sugar. Cooling and filling.":"صرف نمکین لسی — چینی نہیں۔ ٹھنڈا اور پیٹ بھرنے والا۔",
    "Walnuts add omega-3 and slow down sugar absorption from the apple.":"اخروٹ اومیگا-3 دیتے ہیں اور سیب سے شوگر جذب کو سست کرتے ہیں۔",
    "Season with herbs and lemon. No frying.":"جڑی بوٹیوں اور لیموں سے مصالحہ لگائیں۔ تلیں نہیں۔",
    "Load up on vegetables. Under 1 tsp oil.":"سبزیاں زیادہ کھائیں۔ 1 چائے کے چمچ سے کم تیل۔",
    "Spinach adds iron and fibre. Light on cream or butter.":"پالک آئرن اور فائبر دیتی ہے۔ کریم یا مکھن کم رکھیں۔",
    "Best fruit for diabetics — high fibre, low glycemic.":"ذیابیطس کے مریضوں کے لیے بہترین پھل — زیادہ فائبر، کم گلائسیمک۔",
    "Apple fibre slows sugar absorption. Almonds add healthy fat.":"سیب کا فائبر شوگر جذب کو سست کرتا ہے۔ بادام صحت مند چکنائی دیتے ہیں۔",
    "High in magnesium which helps insulin sensitivity.":"میگنیشیم زیادہ جو انسولین حساسیت میں مدد کرتا ہے۔",
    "Light on cream or butter. Spinach adds fibre.":"کریم یا مکھن کم۔ پالک فائبر دیتی ہے۔",
    "Slow-release protein. Helps prevent overnight blood sugar drops.":"آہستہ پروٹین۔ رات میں بلڈ شوگر گرنے سے بچاتا ہے۔",
    "Carb + protein combination keeps blood sugar stable overnight.":"کاربس اور پروٹین کا مجموعہ رات بھر بلڈ شوگر مستحکم رکھتا ہے۔",
    "Protein slows overnight glucose drop. Good for insulin users.":"پروٹین رات میں گلوکوز گرنے کو سست کرتا ہے۔ انسولین استعمال کرنے والوں کے لیے اچھا۔",
    "Light and satisfying. Walnuts add omega-3 and slow sugar release.":"ہلکا اور تسلی بخش۔ اخروٹ اومیگا-3 دیتے اور شوگر آہستہ خارج ہوتی ہے۔",
    "Haldi doodh — anti-inflammatory, slow protein release. No sugar.":"ہلدی دودھ — سوزش کم کرتا ہے، پروٹین آہستہ جذب۔ چینی نہیں۔",
    "Probiotic + omega-3. Keeps blood sugar stable overnight.":"پروبائیوٹک اور اومیگا-3۔ رات بھر بلڈ شوگر مستحکم رکھتا ہے۔",
    "Scrambled eggs with tomato, onion, green chilli. Minimal oil.":"ٹماٹر، پیاز، ہری مرچ کے ساتھ بھرجی۔ کم سے کم تیل۔",
}

SLOT_CFG = {
    "breakfast": ("🌅","Breakfast","ناشتہ"),
    "snack_am":  ("🍎","Mid-Morning Snack","دوپہر سے پہلے کا ناشتہ"),
    "lunch":     ("☀️","Lunch","دوپہر کا کھانا"),
    "snack_pm":  ("🍊","Afternoon Snack","شام کا ناشتہ"),
    "dinner":    ("🌙","Dinner","رات کا کھانا"),
    "snack_bed": ("🌛","Bedtime Snack","سونے سے پہلے کا ناشتہ"),
    "snack":     ("🍎","Snack","ناشتہ"),
}
DAY_NAMES    = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
DAY_NAMES_UR = ["پیر","منگل","بدھ","جمعرات","جمعہ","ہفتہ","اتوار"]

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def _sidebar():
    with st.sidebar:
        _lang_toggle("sb")
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.markdown(f"## 🩺 {t('app_title')}")
        st.caption(t("app_subtitle"))
        if _get_user():
            name = ss.get("name") or ss.get("display_name","")
            st.success(f"**{t('hi_user')}**, {name}!")
            lv = _triage_level()
            if lv:
                cls = {"GREEN":"badge-g","AMBER":"badge-a","RED":"badge-r"}.get(lv,"badge-n")
                lbl = {"GREEN":t("status_green"),"AMBER":t("status_amber"),"RED":t("status_red")}.get(lv,"")
                st.markdown(f'<span class="{cls}">{lbl}</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge-n">⬤ Not assessed</span>', unsafe_allow_html=True)
            st.divider()
            if st.button(t("logout_btn"), use_container_width=True):
                ss["_confirm_logout"] = True
            if ss.get("_confirm_logout"):
                st.warning(t("logout_confirm"))
                c1,c2 = st.columns(2)
                if c1.button(t("yes"),key="ly"): [ss.__delitem__(k) for k in list(ss)]; st.rerun()
                if c2.button(t("no"), key="ln"): ss["_confirm_logout"]=False; st.rerun()
        st.divider()
        if _lang()=="en":
            st.markdown("""<div class="sb-disc"><p class="sb-disc-title">⚠️ Medical Disclaimer</p>
<p>For information only — not medical advice.</p>
<p>• Does not diagnose or prescribe</p><p>• Does not replace your doctor</p>
<p>• Glucose above <strong>180 mg/dL</strong> repeatedly? See your doctor</p>
<p>• Emergency? Call emergency services now</p></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="sb-disc"><p class="sb-disc-title">⚠️ طبی وضاحت</p>
<p>صرف معلومات — طبی مشورہ نہیں۔</p>
<p>• تشخیص یا دوائی تجویز نہیں کرتی</p><p>• ڈاکٹر کی جگہ نہیں لیتی</p>
<p>• شوگر <strong>180 mg/dL</strong> سے بار بار اوپر؟ ڈاکٹر سے ملیں</p>
<p>• ہنگامی صورت میں ایمرجنسی کو کال کریں</p></div>""", unsafe_allow_html=True)
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        st.caption(t("version"))

_sidebar()

# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if "user_key" not in ss:
    h1,h2 = st.columns([5,1])
    with h2: _lang_toggle("entry")
    lang = _lang()
    st.markdown(
        f'<div class="login-hero"><span class="login-hero-logo">🩺 Apni Sehat</span>'
        f'<span class="login-hero-urdu">اپنی صحت</span>'
        f'<span class="login-hero-sub">{"Your personal diabetes health companion" if lang=="en" else "آپ کا ذاتی ذیابیطس صحت ساتھی"}</span></div>',
        unsafe_allow_html=True)
    st.divider()
    left,right = st.columns([1,1],gap="large")
    with left:
        st.markdown(f'<div class="section-label">{"Your details" if lang=="en" else "آپ کی تفصیلات"}</div>',unsafe_allow_html=True)
        name  = st.text_input(t("entry_name"), placeholder=t("entry_name_hint"), label_visibility="collapsed")
        st.markdown('<div style="height:4px"></div>',unsafe_allow_html=True)
        phone = st.text_input(t("entry_phone"),placeholder=t("entry_phone_ph"),  label_visibility="collapsed")
        st.caption(t("entry_phone_hint")); st.caption(t("entry_privacy"))
        st.markdown('<div style="height:10px"></div>',unsafe_allow_html=True)
        go_col,_ = st.columns([1,2])
        with go_col: go = st.button(t("entry_btn"),type="primary",use_container_width=True)
        if go:
            pn = normalize_phone(phone)
            if not name.strip(): st.error(t("name_error")); st.stop()
            if not pn.startswith("+") or len(pn)<8: st.error(t("phone_error")); st.stop()
            with st.spinner(t("finding_plan")):
                uk = user_key_from_phone(pn)
                ss["user_key"]=uk; ss["display_name"]=name.strip(); ss["phone_last4"]=last4(pn)
                try:    prof=get_profile(uk)
                except: st.error(t("db_error")); st.stop()
                if prof and prof.get("age"):
                    ss.update({"name":prof.get("full_name") or name.strip(),"age":prof.get("age",30),"gender":prof.get("gender","Prefer not to say"),"height_cm":prof.get("height_cm",0),"weight_kg":prof.get("weight_kg",0.0),"family_history":prof.get("family_history",[]),"diabetes_type":prof.get("diabetes_type","Type 2"),"has_hypertension":bool(prof.get("has_hypertension",0)),"has_high_cholesterol":bool(prof.get("has_high_cholesterol",0)),"phone_last4":prof.get("phone_last4",last4(pn)),"prefer_desi":True,"veg_only":False,"profile_complete":True,"setup_step":"done","on_insulin":False,"hypo_episodes":False,"weakness_between":False})
                    h=prof.get("height_cm") or 0; w=prof.get("weight_kg") or 0
                    if h>0 and w>0: ss["bmi"]=w/((h/100)**2)
                    _run_triage(ss.get("diabetes_type","Type 2"),ss.get("has_hypertension",False),ss.get("has_high_cholesterol",False))
                    st.success(f"{t('welcome_back')}, {ss['name']}! 👋")
                else:
                    upsert_profile(uk,{"full_name":name.strip(),"phone_last4":last4(pn),"family_history":[]})
                    ss.update({"name":name.strip(),"profile_complete":False,"setup_step":1,"prefer_desi":True,"veg_only":False})
                    st.info(t("new_user_found"))
            st.rerun()
    with right:
        feats = [
            ("✅","Bilingual health chatbot — English & Urdu" if lang=="en" else "اردو اور انگریزی میں صحت کا مددگار"),
            ("🥗","Personalised 7-day desi meal plan"         if lang=="en" else "ذاتی 7 دن کا دیسی کھانے کا منصوبہ"),
            ("📊","Blood sugar tracker with trend chart"       if lang=="en" else "بلڈ شوگر ٹریکر"),
            ("💡","AI food swap suggestions"                   if lang=="en" else "AI سے کھانے کی تجاویز"),
        ]
        rows="".join(f'<p><span style="margin-right:10px;">{i}</span>{txt}</p>' for i,txt in feats)
        disc=("This app supports healthy habits — it does <strong>not</strong> replace your doctor." if lang=="en" else "یہ ایپ صحت مند عادات میں مدد کرتی ہے — آپ کے <strong>ڈاکٹر کی جگہ نہیں لیتی</strong>۔")
        st.markdown(f'<div class="feature-card"><div class="section-label">{"What you get" if lang=="en" else "کیا ملتا ہے"}</div>{rows}<hr style="border:none;border-top:1px solid #2A3147;margin:16px 0 12px;"><p class="disc">⚠️ {disc}</p></div>',unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
#  WIZARD
# ══════════════════════════════════════════════════════════════════════════════
if ss.get("setup_step") in (1,2):
    step=ss["setup_step"]
    wl,wr=st.columns([5,1])
    with wr: _lang_toggle("wiz")
    st.markdown(f"# 🩺 {t('app_title')}")
    _,mid,_=st.columns([1,3,1])
    with mid:
        heading=t("wizard_step1_heading") if step==1 else t("wizard_step2_heading")
        caption=t("wizard_step1_caption") if step==1 else t("wizard_step2_caption")
        st.markdown(f'<div class="wizard-box"><span class="step-pill">Step {"1" if step==1 else "2"} / 2</span><h2>{heading}</h2><p>{caption}</p></div>',unsafe_allow_html=True)
        st.markdown('<div style="height:12px"></div>',unsafe_allow_html=True)

        if step==1:
            lg=_lang()
            name_v=st.text_input(t("wizard_name"),value=ss.get("name",""))
            col_age,col_gen=st.columns(2)
            with col_age: age_v=st.number_input(t("wizard_age"),1,110,int(ss.get("age",50)))
            with col_gen:
                gender_opts=["Prefer not to say","Male","Female","Other"]
                saved_g=ss.get("gender","Prefer not to say")
                g_idx=gender_opts.index(saved_g) if saved_g in gender_opts else 0
                gender_v=st.selectbox(t("pf_gender"),gender_opts,index=g_idx)
            st.markdown(f"**{t('pf_height_lbl')}**")
            col_ft,col_in=st.columns(2)
            with col_ft: height_ft=st.number_input(t("pf_feet"),0,8,int(ss.get("height_ft",5)),key="wiz_ft")
            with col_in: height_in=st.number_input(t("pf_inches"),0,11,int(ss.get("height_in",6)),key="wiz_in")
            height_cm_calc=round((height_ft*12+height_in)*2.54)
            weight_kg_v=st.number_input("Weight (kg)" if lg=="en" else "وزن (کلوگرام)",20.0,400.0,float(ss.get("weight_kg",70.0) or 70.0),0.5,key="wiz_wt")
            bmi_v=None
            if height_cm_calc>0 and weight_kg_v>0:
                bmi_v=round(weight_kg_v/((height_cm_calc/100)**2),1)
                bmi_txt=f"📏 آپ کا BMI: **{bmi_v}** (تخمینہ)" if lg=="ur" else f"📏 Your BMI: **{bmi_v}** (estimated)"
                st.caption(bmi_txt)
            st.divider()
            d_opts=["Type 1","Type 2","Not sure / not diagnosed"]
            saved_d=ss.get("diabetes_type","Type 2")
            d_idx=d_opts.index(saved_d) if saved_d in d_opts else 1
            dtype_d=st.selectbox(t("wiz_diabetes_q"),d_opts,index=d_idx)
            if dtype_d=="Not sure / not diagnosed": st.warning(t("wiz_not_sure_warning"))
            st.divider()
            pref=st.checkbox(t("wizard_desi"),value=ss.get("prefer_desi",True))
            veg =st.checkbox(t("wizard_veg"), value=ss.get("veg_only",False))
            st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
            nc,_=st.columns([1,2])
            with nc:
                if st.button(t("wizard_next"),type="primary",use_container_width=True):
                    if not name_v.strip(): st.error(t("name_error")); st.stop()
                    ss.update({"name":name_v.strip(),"age":int(age_v),"gender":gender_v,"height_ft":int(height_ft),"height_in":int(height_in),"height_cm":height_cm_calc,"weight_kg":float(weight_kg_v),"bmi":bmi_v,"diabetes_type":dtype_d,"prefer_desi":pref,"veg_only":veg,"setup_step":2})
                    st.rerun()

        else:
            # ── Step 2 — fully bilingual ─────────────────────────────────────
            lg=_lang()
            _yn3   = ["No","Yes","Not sure"] if lg=="en" else ["نہیں","ہاں","یقین نہیں"]
            _yn3_en= ["No","Yes","Not sure"]
            _yn2   = ["No","Yes"] if lg=="en" else ["نہیں","ہاں"]

            st.markdown("### "+("Do you have any of the following conditions?" if lg=="en" else "کیا آپ کو درج ذیل میں سے کوئی بیماری ہے؟"))
            st.caption("Tick all that apply. If you have none, leave all unticked and click Finish." if lg=="en" else "جو لاگو ہو وہ چیک کریں۔ اگر کوئی نہیں تو سب خالی چھوڑ کر مکمل کریں۔")

            hy_saved=ss.get("hy_ans","No")
            hy_idx=_yn3_en.index(hy_saved) if hy_saved in _yn3_en else 0
            hy_q=st.radio("High blood pressure (hypertension)?" if lg=="en" else "ہائی بلڈ پریشر (ہائپرٹینشن)؟",_yn3,index=hy_idx,horizontal=True,key="wiz_hy")
            hy_en=_yn3_en[_yn3.index(hy_q)]

            ch_saved=ss.get("ch_ans","No")
            ch_idx=_yn3_en.index(ch_saved) if ch_saved in _yn3_en else 0
            ch_q=st.radio("High cholesterol?" if lg=="en" else "زیادہ کولیسٹرول؟",_yn3,index=ch_idx,horizontal=True,key="wiz_ch")
            ch_en=_yn3_en[_yn3.index(ch_q)]

            ot_saved=ss.get("other_ans","No")
            ot_idx=["No","Yes"].index(ot_saved) if ot_saved in ["No","Yes"] else 0
            other_q=st.radio("Other major conditions? (kidney disease, heart disease, pregnancy, etc.)" if lg=="en" else "دیگر بڑی بیماریاں؟ (گردے، دل، حمل وغیرہ)",_yn2,index=ot_idx,horizontal=True,key="wiz_ot")
            other_en="Yes" if other_q in ("Yes","ہاں") else "No"

            hy=(hy_en=="Yes"); ch=(ch_en=="Yes"); other=(other_en=="Yes")
            hy_ns=(hy_en=="Not sure"); ch_ns=(ch_en=="Not sure")

            if hy_ns:
                st.info("💡 If you're unsure about blood pressure, ask your doctor or pharmacist — many clinics offer free checks." if lg=="en" else "💡 بلڈ پریشر کے بارے میں یقین نہ ہو تو ڈاکٹر یا فارماسسٹ سے پوچھیں — بہت سے کلینک مفت چیک کرتے ہیں۔")
            if ch_ns:
                st.info("💡 A simple lipid panel blood test will tell you your cholesterol levels. Worth asking your doctor." if lg=="en" else "💡 ایک سادہ لپڈ پینل بلڈ ٹیسٹ آپ کا کولیسٹرول بتائے گا۔ ڈاکٹر سے پوچھنا مفید ہے۔")

            st.divider()
            st.markdown("**"+("A few more questions about your daily routine:" if lg=="en" else "آپ کے روزمرہ کے بارے میں چند اور سوالات:")+"**")
            ins =st.checkbox(t("q_insulin"), value=ss.get("on_insulin",False),     help=t("q_insulin_help"))
            hypo=st.checkbox(t("q_hypo"),    value=ss.get("hypo_episodes",False),  help=t("q_hypo_help"))
            wkn =st.checkbox(t("q_weakness"),value=ss.get("weakness_between",False),help=t("q_weakness_help"))

            st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
            bc,fc,_=st.columns([1,1,1])
            with bc:
                if st.button(t("wizard_back"),use_container_width=True): ss["setup_step"]=1; st.rerun()
            with fc:
                if st.button(t("wizard_finish"),type="primary",use_container_width=True):
                    with st.spinner(t("wizard_saving")):
                        dtype=ss.get("diabetes_type","Type 2")
                        if dtype=="Not sure / not diagnosed":
                            ss["triage_level"]="AMBER"
                            ss["triage_flags"]=["Diabetes status unconfirmed — please get a fasting blood sugar test.","Following a cautious low-GI plan until diagnosis is confirmed."]
                        else:
                            _run_triage(dtype,hy or hy_ns,ch or ch_ns,other_major=other)
                        ss.update({"has_hypertension":hy or hy_ns,"has_high_cholesterol":ch or ch_ns,"hy_ans":hy_en,"ch_ans":ch_en,"other_ans":other_en,"on_insulin":ins,"hypo_episodes":hypo,"weakness_between":wkn,"family_history":[]})
                        upsert_profile(ss["user_key"],{"full_name":ss["name"],"phone_last4":ss.get("phone_last4"),"age":ss["age"],"gender":ss.get("gender","Prefer not to say"),"height_cm":ss.get("height_cm",0),"weight_kg":ss.get("weight_kg",0.0),"family_history":[],"diabetes_type":dtype,"has_hypertension":1 if (hy or hy_ns) else 0,"has_high_cholesterol":1 if (ch or ch_ns) else 0})
                        ss["week_plan"]=generate_week_plan(prefer_desi=ss.get("prefer_desi",True),veg_only=ss.get("veg_only",False),has_hypertension=hy or hy_ns,has_high_cholesterol=ch or ch_ns,on_insulin=ins,hypo_episodes=hypo,weakness_between=wkn,bmi=ss.get("bmi"),diabetes_type=dtype)
                        ss["profile_complete"]=True; ss["setup_step"]="done"
                    st.success(t("wizard_done_msg")); st.rerun()
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════════════════════
if "current_tip"     not in ss: ss["current_tip"]     = get_tip(_lang())
if "chat_history"    not in ss: ss["chat_history"]    = []
if "editing_profile" not in ss: ss["editing_profile"] = False

tl,tr=st.columns([6,1])
with tr: _lang_toggle("main")

if not ss.get("week_plan"):
    with st.spinner(t("loading_plan")):
        ss["week_plan"]=generate_week_plan(prefer_desi=ss.get("prefer_desi",True),veg_only=ss.get("veg_only",False),has_hypertension=ss.get("has_hypertension",False),has_high_cholesterol=ss.get("has_high_cholesterol",False),on_insulin=ss.get("on_insulin",False),hypo_episodes=ss.get("hypo_episodes",False),weakness_between=ss.get("weakness_between",False),bmi=ss.get("bmi"),diabetes_type=ss.get("diabetes_type","Type 2"))

tabs=st.tabs([t("tab_plan"),t("tab_chat"),t("tab_glucose"),t("tab_dashboard")])

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 0 — MY PLAN
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    lv=_triage_level()
    bcls={"GREEN":"badge-g","AMBER":"badge-a","RED":"badge-r"}.get(lv or "","badge-n")
    blbl={"GREEN":t("status_green"),"AMBER":t("status_amber"),"RED":t("status_red")}.get(lv or "",t("status_none"))
    conds=([("Hypertension" if _lang()=="en" else "ہائی بلڈ پریشر")] if ss.get("has_hypertension") else [])+([("High Cholesterol" if _lang()=="en" else "زیادہ کولیسٹرول")] if ss.get("has_high_cholesterol") else [])
    cond_str=", ".join(conds) if conds else t("no_conditions")
    name_d=ss.get("name",ss.get("display_name","")); age_d=ss.get("age",""); dtype_d=ss.get("diabetes_type","")

    pc1,pc2=st.columns([5,1])
    with pc1:
        st.markdown(f'<div class="profile-card"><div class="profile-name">👤 {name_d}'+(f', {age_d}' if age_d else '')+'</div><div class="profile-detail">'+(f'{dtype_d} · ' if dtype_d else '')+f'{cond_str}</div><div style="margin-top:10px;"><span class="{bcls}">{blbl}</span></div></div>',unsafe_allow_html=True)
    with pc2:
        st.markdown('<div style="height:20px"></div>',unsafe_allow_html=True)
        if st.button(t("edit_profile_btn"),use_container_width=True): ss["editing_profile"]=not ss.get("editing_profile",False); st.rerun()

    if ss.get("editing_profile"):
        ef1,ef2=st.columns(2)
        with ef1:
            en =st.text_input(t("pf_name"),value=ss.get("name",""),key="e_name")
            ea =st.number_input(t("pf_age"),1,110,int(ss.get("age",50) or 50),key="e_age")
        with ef2:
            go =t("pf_gender_opts"); ge=T["en"]["pf_gender_opts"]
            gs =ss.get("gender","Prefer not to say"); gi=ge.index(gs) if gs in ge else 0
            egn=st.selectbox(t("pf_gender"),go,index=gi,key="e_gender")
            do =t("pf_diabetes_opts"); de=T["en"]["pf_diabetes_opts"]
            ds =ss.get("diabetes_type","Type 2"); di=de.index(ds) if ds in de else 0
            edt=st.selectbox(t("pf_diabetes"),do,index=di,key="e_dtype")
        _stored_cm=int(ss.get("height_cm",0) or 0); _total_in=round(_stored_cm/2.54); _def_ft=_total_in//12; _def_in=_total_in%12
        st.markdown(f"**{t('pf_height_lbl')}**")
        ef3a,ef3b,ef4=st.columns([1,1,1])
        with ef3a: e_ft=st.number_input(t("pf_feet"),0,8,int(ss.get("edit_height_ft",_def_ft)),key="e_ft")
        with ef3b: e_in=st.number_input(t("pf_inches"),0,11,int(ss.get("edit_height_in",_def_in)),key="e_in")
        eh=round((e_ft*12+e_in)*2.54)
        with ef4: ew=st.number_input(t("pf_weight"),0.0,400.0,float(ss.get("weight_kg",0.0) or 0.0),0.5,key="e_w")
        eb=None
        if eh>0 and ew>0: eb=ew/((eh/100)**2); st.caption(f"{t('pf_bmi')}: **{eb:.1f}** {t('pf_bmi_note')}")
        efam=st.multiselect(t("pf_family"),T["en"]["pf_family_opts"],default=ss.get("family_history",[]),key="e_fam")
        ec1,ec2,ec3=st.columns(3)
        with ec1: ehy=st.checkbox(t("pf_hypert"),value=ss.get("has_hypertension",False),key="e_hy")
        with ec2: ech=st.checkbox(t("pf_chol"),  value=ss.get("has_high_cholesterol",False),key="e_ch")
        with ec3: eot=st.checkbox(t("pf_other"),key="e_ot")
        st.divider()
        st.markdown(f"**{'Meal frequency' if _lang()=='en' else 'کھانے کی تعداد'}**")
        ef_1,ef_2,ef_3=st.columns(3)
        with ef_1: eins=st.checkbox(t("q_insulin"), value=ss.get("on_insulin",False),      key="e_ins",help=t("q_insulin_help"))
        with ef_2: ehyp=st.checkbox(t("q_hypo"),    value=ss.get("hypo_episodes",False),   key="e_hyp",help=t("q_hypo_help"))
        with ef_3: ewkn=st.checkbox(t("q_weakness"),value=ss.get("weakness_between",False),key="e_wkn",help=t("q_weakness_help"))
        adv_key="show_adv_"+str(ss.get("user_key",""))[:8]
        if adv_key not in ss: ss[adv_key]=False
        if st.button("➕ "+("Add recent test results (optional)" if _lang()=="en" else "حالیہ ٹیسٹ کے نتائج شامل کریں"),key="adv_tog"):
            ss[adv_key]=not ss[adv_key]; st.rerun()
        ebps=ebpd=ea1c=etc=ef1=ef2=ef3=0
        if ss.get(adv_key,False):
            st.caption(t("pf_advanced_note"))
            a1,a2,a3=st.columns(3)
            with a1: ebps=st.number_input(t("pf_bp_sys"),0,300,130 if ehy else 0,key="e_bps"); ebpd=st.number_input(t("pf_bp_dia"),0,200,80 if ehy else 0,key="e_bpd")
            with a2: ea1c=st.number_input(t("pf_a1c"),0.0,20.0,0.0,0.1,key="e_a1c")
            with a3: etc =st.number_input(t("pf_chol_val"),0.0,600.0,0.0,1.0,key="e_tc")
            st.markdown(f"**{t('pf_fasting_head')}**"); st.caption(t("pf_fasting_note"))
            f1c,f2c,f3c=st.columns(3)
            with f1c: ef1=st.number_input(t("pf_day3"),0.0,600.0,0.0,1.0,key="e_f1")
            with f2c: ef2=st.number_input(t("pf_day2"),0.0,600.0,0.0,1.0,key="e_f2")
            with f3c: ef3=st.number_input(t("pf_day1"),0.0,600.0,0.0,1.0,key="e_f3")
        sv_c,_=st.columns([1,2])
        with sv_c:
            if st.button(t("save_profile_btn"),type="primary",use_container_width=True,key="sp"):
                with st.spinner(t("saving_profile")):
                    gn=T["en"]["pf_gender_opts"][T[_lang()]["pf_gender_opts"].index(egn)]
                    dn=T["en"]["pf_diabetes_opts"][T[_lang()]["pf_diabetes_opts"].index(edt)]
                    ss.update({"name":en.strip(),"age":int(ea),"gender":gn,"diabetes_type":dn,"height_cm":int(eh),"weight_kg":float(ew),"family_history":efam,"bmi":eb,"has_hypertension":ehy,"has_high_cholesterol":ech,"on_insulin":eins,"hypo_episodes":ehyp,"weakness_between":ewkn})
                    _run_triage(dn,ehy,ech,bp_sys=float(ebps) if ebps>0 else None,bp_dia=float(ebpd) if ebpd>0 else None,a1c=float(ea1c) if ea1c>0 else None,fasting_readings=_parse_fastings([ef1,ef2,ef3]),total_chol=float(etc) if etc>0 else None,other_major=eot)
                    upsert_profile(ss["user_key"],{"full_name":en.strip(),"phone_last4":ss.get("phone_last4"),"age":int(ea),"gender":gn,"height_cm":int(eh) if eh else None,"weight_kg":float(ew) if ew else None,"family_history":efam,"diabetes_type":dn,"has_hypertension":1 if ehy else 0,"has_high_cholesterol":1 if ech else 0})
                    ss["week_plan"]=generate_week_plan(prefer_desi=ss.get("prefer_desi",True),veg_only=ss.get("veg_only",False),has_hypertension=ehy,has_high_cholesterol=ech,on_insulin=eins,hypo_episodes=ehyp,weakness_between=ewkn,bmi=eb,diabetes_type=dn)
                    ss["editing_profile"]=False
                st.success(t("profile_saved")); st.rerun()
        if ss.get("triage_level"):
            lv2=ss["triage_level"]
            if lv2=="GREEN": st.success(t("green_result"))
            elif lv2=="AMBER": st.warning(t("amber_result"))
            else: st.error(t("red_result"))
            for f in ss.get("triage_flags",[]): st.write("•", _translate_flag(f))

    st.divider()
    tc,tb=st.columns([5,1])
    with tc: st.markdown(f'<div class="tip-banner"><span class="tip-label">{t("tip_title")}</span>{ss["current_tip"]}</div>',unsafe_allow_html=True)
    with tb:
        st.markdown('<div style="height:16px"></div>',unsafe_allow_html=True)
        if st.button(t("tip_new"),use_container_width=True,key="new_tip"): ss["current_tip"]=get_tip(_lang()); st.rerun()

    pp=_plan_profile()
    if pp:
        lg=_lang()
        reason=pp.get("reason_en" if lg=="en" else "reason_ur",""); label=pp.get("label_en" if lg=="en" else "label_ur",""); portion=pp.get("portion_note_en" if lg=="en" else "portion_note_ur","")
        if reason: st.info(f"**{t('meal_structure')}: {label}**\n\n{reason}"+(f"\n\n📏 {portion}" if portion else ""))
    if ss.get("on_insulin"):    st.warning(t("insulin_reminder"))
    if ss.get("hypo_episodes"): st.warning(t("hypo_reminder"))

    st.markdown(f"## 🥗 {t('plan_heading')}")
    if _blocked():
        st.error(t("plan_blocked"))
    else:
        tc1,tc2,tc3=st.columns([2,2,2])
        with tc1: prefer_desi=st.toggle(t("desi_toggle"),value=ss.get("prefer_desi",True),key="pd_tog")
        with tc2: veg_only   =st.toggle(t("veg_toggle"), value=ss.get("veg_only",False),  key="vo_tog")
        with tc3:
            if st.button(t("regen_btn")):
                with st.spinner(t("building_plan")):
                    ss["week_plan"]=generate_week_plan(prefer_desi=prefer_desi,veg_only=veg_only,has_hypertension=ss.get("has_hypertension",False),has_high_cholesterol=ss.get("has_high_cholesterol",False),on_insulin=ss.get("on_insulin",False),hypo_episodes=ss.get("hypo_episodes",False),weakness_between=ss.get("weakness_between",False),bmi=ss.get("bmi"),diabetes_type=ss.get("diabetes_type","Type 2"))
                ss["prefer_desi"]=prefer_desi; ss["veg_only"]=veg_only; st.rerun()
        ss["prefer_desi"]=prefer_desi; ss["veg_only"]=veg_only

        days=_plan_days(); slots=_plan_slots(); lg=_lang()
        if "selected_day" not in ss: ss["selected_day"]=1
        st.markdown(f"#### {'Select Day' if lg=='en' else 'دن منتخب کریں'}")
        _day_word="Day" if lg=="en" else "دن"
        active_dn=ss["selected_day"]
        cols=st.columns(len(days))
        for i,day in enumerate(days):
            dn=day["day"]; day_name=(DAY_NAMES_UR if lg=="ur" else DAY_NAMES)[(dn-1)%7]; is_active=(dn==active_dn); label=f"{day_name}\n{_day_word} {dn}"
            def _select(d=dn): ss["selected_day"]=d
            with cols[i]:
                st.button(label,key=f"day_sel_{dn}",use_container_width=True,on_click=_select,type="primary" if is_active else "secondary")
        st.markdown('<div style="height:8px"></div>',unsafe_allow_html=True)
        st.divider()

        sel_day=next((d for d in days if d["day"]==ss["selected_day"]),days[0])
        sel_num=sel_day["day"]
        day_name_full=(DAY_NAMES_UR if lg=="ur" else DAY_NAMES)[(sel_num-1)%7]
        day_carbs=sum(sel_day[s]["carb_servings"]*CARB["carb_serving_grams"] for s in slots if s in sel_day)
        st.markdown(f"#### 📅 {'Day' if lg=='en' else 'دن'} {sel_num} {'Menu' if lg=='en' else 'مینو'} — {day_name_full} &nbsp; <span style='font-size:0.85rem;color:var(--txt3);font-weight:400'>~{day_carbs:.0f}g {t('carbs_label')}</span>",unsafe_allow_html=True)
        st.markdown('<div style="height:6px"></div>',unsafe_allow_html=True)

        for slot in slots:
            if slot not in sel_day: continue
            meal=sel_day[slot]
            ico,le,lu=SLOT_CFG.get(slot,("🍽️",slot.title(),slot.title()))
            lbl=le if lg=="en" else lu
            cg=meal["carb_servings"]*CARB["carb_serving_grams"]
            meal_name=meal.get("name_ur",meal["name"]) if lg=="ur" else meal["name"]
            meal_note=_NOTES_UR.get(meal["notes"],meal["notes"]) if lg=="ur" else meal["notes"]
            st.markdown(
                f'<div class="meal-card">'
                f'<div class="meal-card-slot">{ico} {lbl}</div>'
                f'<div class="meal-card-name">{meal_name}</div>'
                f'<div class="meal-card-note">~{cg}{"گرام کاربس" if lg=="ur" else "g carbs"} &nbsp;·&nbsp; {meal_note}</div>'
                f'</div>',unsafe_allow_html=True)
            why_key=f"why_{sel_num}_{slot}"
            w_col,_=st.columns([1,4])
            with w_col:
                if st.button("💡 "+("Why this meal?" if lg=="en" else "یہ کھانا کیوں؟"),key=f"why_btn_{sel_num}_{slot}",use_container_width=True):
                    profile_str=f"diabetes type: {ss.get('diabetes_type','Type 2')}, hypertension: {ss.get('has_hypertension',False)}, high cholesterol: {ss.get('has_high_cholesterol',False)}, BMI: {ss.get('bmi','unknown')}, on insulin: {ss.get('on_insulin',False)}"
                    with st.spinner("💭 Thinking..." if lg=="en" else "💭 سوچ رہا ہے..."):
                        explanation=_call_llm(
                            system=("You are a clinical dietitian explaining a meal choice to a Pakistani diabetes patient. Be warm, brief (2–3 sentences), and specific. Reference the patient's conditions. Mention one glycaemic benefit and one cultural/practical benefit. Do NOT suggest medication changes. Do NOT diagnose. "+("Respond in Urdu script." if lg=="ur" else "Respond in plain English.")),
                            user=f"Patient profile: {profile_str}\nMeal slot: {lbl}\nMeal chosen: {meal['name']}\nWhy was this specific meal chosen for this patient?",
                            max_tokens=180)
                    ss[why_key]=explanation
            if ss.get(why_key):
                clinical_lbl="💡 وجہ" if lg=="ur" else "💡 Clinical Reasoning"
                st.markdown(f'<div style="background:var(--green-t);border:1px solid var(--green2);border-radius:8px;padding:12px 16px;margin:-4px 0 12px 0;font-size:0.95rem;line-height:1.7;color:var(--txt);"><span style="font-size:0.75rem;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:0.08em;">{clinical_lbl}</span><br>{ss[why_key]}</div>',unsafe_allow_html=True)

        st.markdown('<div style="height:12px"></div>',unsafe_allow_html=True)
        sw_c,_=st.columns([1,3])
        with sw_c:
            if st.button(t("swaps_btn"),key="sw_sel",use_container_width=True):
                names=[sel_day[s]["name"] for s in slots if s in sel_day]
                with st.spinner(t("getting_swaps")): swaps=generate_swaps("; ".join(names))
                st.markdown(f"**{t('swaps_heading')}**")
                for s in swaps: st.write("•",s)

    st.divider()
    st.markdown(f"### {t('checkin_heading')}")
    user=_get_user()
    if not _blocked():
        ci_date =st.date_input(t("checkin_date"),value=date.today(),key="ci_date")
        followed=st.radio(t("followed_q"),[t("yes_opt"),t("no_opt")],horizontal=True,key="ci_rad")
        if followed==t("yes_opt"):
            cb,_=st.columns([1,3])
            with cb:
                if st.button(t("save_ci_btn"),type="primary",use_container_width=True,key="ci_yes"):
                    add_daily_checkin(user,ci_date,followed_plan=True,actual_meals=""); st.success(t("ci_saved")); st.balloons()
        else:
            actual=st.text_area(t("ate_label"),placeholder=t("ate_ph"),height=100,key="ci_ate")
            sb,_=st.columns([1,3])
            with sb:
                if st.button(t("save_suggest_btn"),type="primary",use_container_width=True,key="ci_no"):
                    if not actual.strip(): st.warning(t("describe_ate"))
                    else:
                        with st.spinner(t("saving_suggest")):
                            add_daily_checkin(user,ci_date,followed_plan=False,actual_meals=actual.strip()); tips=coach_on_actual_meal(actual.strip())
                        st.success(t("suggest_saved"))
                        for tip in tips: st.write("•",tip)
                        st.caption(t("suggest_note"))
    st.markdown(f'<div class="footer">⚠️ {APP["disclaimer"]}</div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — CHAT
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown(f"## 💬 {t('chat_heading')}")
    st.caption(t("chat_caption"))
    st.divider()
    if not ss["chat_history"]:
        st.markdown(f'<div class="bubble-bot"><div class="bubble-label">🩺 Sehat Saathi / صحت ساتھی</div>{t("chat_greeting_en").replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
    uname=ss.get("name",ss.get("display_name","You"))
    for msg in ss["chat_history"]:
        content=msg["content"].replace("\n","<br>")
        if msg["role"]=="user":
            st.markdown(f'<div class="bubble-user"><div class="bubble-label">👤 {uname}</div>{content}</div>',unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-bot"><div class="bubble-label">🩺 Sehat Saathi</div>{content}</div>',unsafe_allow_html=True)
    user_input=st.chat_input(t("chat_placeholder"))
    if user_input:
        rag_chunks=_rag_retrieve(user_input,top_k=2)
        if rag_chunks:
            rag_context="\n\n".join(f"[Evidence — {c['source']}]\n{c['text']}" for c in rag_chunks)
            enriched_input=f"[CLINICAL CONTEXT — use this evidence to inform your answer, cite the source naturally if relevant]:\n{rag_context}\n\n[Patient question]: {user_input}"
        else:
            enriched_input=user_input
        ss["chat_history"].append({"role":"user","content":user_input})
        with st.spinner(t("chat_thinking")):
            history_for_llm=ss["chat_history"][:-1]+[{"role":"user","content":enriched_input}]
            reply=chat_with_assistant(history_for_llm,lang=_lang(),user_profile=_profile_context())
        ss["chat_history"].append({"role":"assistant","content":reply})
        st.rerun()
    if ss["chat_history"]:
        cl,_=st.columns([1,4])
        with cl:
            if st.button(t("chat_clear"),key="clr_chat",use_container_width=True): ss["chat_history"]=[]; st.rerun()
    st.caption(t("chat_note"))


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — LOG SUGAR
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown(f"## 📊 {t('glucose_heading')}")
    user=_get_user()
    if _blocked():
        st.error(t("blocked_msg"))
    else:
        c1,c2=st.columns(2)
        with c1:
            r_type =st.selectbox(t("reading_lbl"),t("reading_types"))
            m_date =st.date_input(t("date_lbl"),value=date.today())
            m_time =st.time_input(t("time_lbl"),value=datetime.now().time())
        with c2:
            value    =st.number_input(t("value_lbl"),0.0,600.0,110.0,1.0)
            meal_note=st.text_input(t("note_lbl"),placeholder=t("note_ph"))
            st.caption(t("ref_ranges").format(h=TRIAGE["hypo"],vh=TRIAGE["very_high"]))
            if value>=TRIAGE["very_high"]: st.error(t("very_high_alert"))
            elif 0<value<TRIAGE["hypo"]:  st.warning(t("low_alert"))
        sb,_=st.columns([1,3])
        with sb:
            if st.button("Save Reading" if _lang()=="en" else "ریڈنگ محفوظ کریں",type="primary",use_container_width=True):
                with st.spinner(t("saving_reading")): add_glucose_log(user,datetime.combine(m_date,m_time),r_type,value,meal_note)
                st.success(t("reading_saved"))
    st.markdown(f'<div class="footer">⚠️ {APP["disclaimer"]}</div>',unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — PROGRESS / DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown(f"## 📈 {t('dash_heading')}")
    st.caption(t("dash_caption"))
    user=_get_user()
    c1,c2=st.columns(2); rows=None
    with c1:
        st.markdown(f"### {t('adh_section')}")
        checkins=fetch_checkins(user)
        if checkins:
            cdf=pd.DataFrame(checkins,columns=["date","followed_plan","actual_meals"])
            cdf["date"]=pd.to_datetime(cdf["date"]).dt.date
            adh=(cdf["followed_plan"].sum()/len(cdf))*100
            st.metric(t("adh_metric"),f"{adh:.0f}%",delta=t("adh_delta").format(n=len(cdf)))
            st.dataframe(cdf[["date","followed_plan"]].rename(columns={"date":t("col_date"),"followed_plan":t("col_fol")}),use_container_width=True)
        else: st.info(t("no_checkins"))
    with c2:
        st.markdown(f"### {t('gluc_section')}")
        rows=fetch_glucose_logs(user)
        if rows:
            df=pd.DataFrame(rows,columns=["measured_at","type","value","meal_note"])
            df["measured_at"]=pd.to_datetime(df["measured_at"])
            avg=df["value"].mean(); std=df["value"].std()
            hc=int((df["value"]>=TRIAGE["very_high"]).sum()); lc=int((df["value"]<TRIAGE["hypo"]).sum())
            m1,m2,m3=st.columns(3)
            m1.metric(t("avg_lbl"),f"{avg:.0f} mg/dL"); m2.metric(t("var_lbl"),f"±{std:.0f}"); m3.metric(t("total_lbl"),len(df))
            if hc: st.warning(t("high_alert_d").format(n=hc))
            if lc: st.warning(t("low_alert_d").format(n=lc))
        else: st.info(t("no_glucose"))

    if rows:
        st.markdown(f"### {t('trend_head')}")
        plt.rcParams.update({"figure.facecolor":"#0F1117","axes.facecolor":"#1E2436","axes.edgecolor":"#2A3147","text.color":"#E2E8F0","xtick.color":"#64748B","ytick.color":"#64748B","axes.labelcolor":"#64748B","grid.color":"#2A3147"})
        fig,ax=plt.subplots(figsize=(10,3))
        ax.plot(df["measured_at"],df["value"],marker="o",lw=2,color="#22C55E",ms=5,zorder=3)
        ax.fill_between(df["measured_at"],df["value"],alpha=0.10,color="#22C55E")
        ax.axhline(TRIAGE["very_high"],color="#EF4444",ls="--",lw=1.2,alpha=0.7,label=f"Very high ({TRIAGE['very_high']})")
        ax.axhline(TRIAGE["hypo"],     color="#F59E0B",ls="--",lw=1.2,alpha=0.7,label=f"Low ({TRIAGE['hypo']})")
        ax.set_ylabel("mg/dL",fontsize=10); ax.grid(axis="y",alpha=0.25)
        ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
        ax.legend(fontsize=8,labelcolor="#E2E8F0",facecolor="#1E2436",edgecolor="#2A3147")
        plt.xticks(rotation=30,fontsize=8); plt.tight_layout()
        st.pyplot(fig); plt.rcParams.update(plt.rcParamsDefault)
        st.caption(t("trend_note"))
        if st.button("📋 "+("View all readings" if _lang()=="en" else "تمام ریڈنگز دیکھیں"),key="tog_readings"):
            ss["show_all_readings"]=not ss.get("show_all_readings",False); st.rerun()
        if ss.get("show_all_readings",False):
            st.dataframe(df.rename(columns={"measured_at":t("col_time"),"type":t("col_type"),"value":t("col_val"),"meal_note":t("col_note")}),use_container_width=True)

        st.divider()
        lg=_lang()
        st.markdown("### 🤖 "+("AI Trend Analysis" if lg=="en" else "AI رجحان تجزیہ"))
        st.caption("AI-powered pattern analysis of your readings — not a diagnosis." if lg=="en" else "آپ کی ریڈنگز کا AI تجزیہ — یہ تشخیص نہیں ہے۔")
        if st.button("🔍 "+("Analyse My Glucose Trends" if lg=="en" else "میری گلوکوز رجحانات کا تجزیہ کریں"),key="ai_glucose_btn",type="primary"):
            df_sorted=df.sort_values("measured_at"); recent=df_sorted.tail(14).copy()
            recent["hour"]=recent["measured_at"].dt.hour
            morning_avg  =recent[recent["hour"].between(5,10)]["value"].mean()
            afternoon_avg=recent[recent["hour"].between(11,16)]["value"].mean()
            evening_avg  =recent[recent["hour"].between(17,22)]["value"].mean()
            type_avgs=recent.groupby("type")["value"].mean().to_dict()
            type_str="; ".join(f"{k}: {v:.0f} mg/dL" for k,v in type_avgs.items())
            y=recent["value"].tolist(); slope=(y[-1]-y[0])/max(len(y)-1,1) if len(y)>=2 else 0
            trend_dir="improving (decreasing)" if slope<-2 else ("worsening (increasing)" if slope>2 else "stable")
            readings_str="\n".join(f"  {row['measured_at'].strftime('%Y-%m-%d %H:%M')} | {row['type']} | {row['value']:.0f} mg/dL"+(f" | note: {row['meal_note']}" if row.get("meal_note") else "") for _,row in recent.iterrows())
            profile_str=f"Name: {ss.get('name','Patient')}, Age: {ss.get('age','?')}, Diabetes: {ss.get('diabetes_type','Type 2')}, Hypertension: {ss.get('has_hypertension',False)}, On insulin: {ss.get('on_insulin',False)}, BMI: {ss.get('bmi','?')}"
            with st.spinner("🧠 Analysing your patterns..." if lg=="en" else "🧠 آپ کے نمونوں کا تجزیہ ہو رہا ہے..."):
                analysis=_call_llm(
                    system=("You are a clinical endocrinologist reviewing a diabetes patient's glucose log. Provide a structured analysis in exactly this format:\n\n**PATTERN SUMMARY** (2 sentences)\n\n**TIME-OF-DAY INSIGHTS** (1-2 sentences)\n\n**3 SPECIFIC RECOMMENDATIONS** (numbered, actionable, desi-context-aware)\n\n**WATCH OUT FOR** (1 sentence — biggest risk in this data)\n\nBe specific, reference actual numbers. Never diagnose or suggest medication changes. "+("Respond in Urdu script." if lg=="ur" else "Respond in English.")),
                    user=f"Patient: {profile_str}\n\nStats (last {len(recent)} readings): Average {avg:.0f} mg/dL | Variability ±{std:.0f} | High (≥{TRIAGE['very_high']}): {hc} | Low (<{TRIAGE['hypo']}): {lc}\nTrend: {trend_dir} | By type: {type_str}\nMorning avg: {morning_avg:.0f} | Afternoon: {afternoon_avg:.0f} | Evening: {evening_avg:.0f}\n\nRecent readings:\n{readings_str}",
                    max_tokens=600)
            ss["glucose_analysis"]=analysis
        if ss.get("glucose_analysis"):
            st.markdown(f'<div style="background:var(--bg2);border:1px solid var(--border);border-top:3px solid var(--green);border-radius:10px;padding:20px 24px;margin-top:8px;line-height:1.85;">{ss["glucose_analysis"].replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
            st.caption("⚠️ AI analysis is for awareness only — not a clinical diagnosis. Share with your doctor." if lg=="en" else "⚠️ AI تجزیہ صرف آگاہی کے لیے ہے — طبی تشخیص نہیں۔ اپنے ڈاکٹر سے شیئر کریں۔")

    st.markdown(f'<div class="footer">⚠️ {APP["disclaimer"]}</div>',unsafe_allow_html=True)
