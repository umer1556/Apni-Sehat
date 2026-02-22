# 🩺 Apni Sehat — اپنی صحت

> **Bilingual AI-powered diabetes companion for Pakistan** — personalised desi meal plans, evidence-backed health chat, blood sugar tracking, and clinical triage. Built for the 33 million Pakistanis living with diabetes.

<p align="center">
  <a href="YOUR_YOUTUBE_LINK_HERE">
    <img src="https://img.shields.io/badge/▶️_Watch_Demo-2min-red?style=for-the-badge&logo=youtube" alt="Watch Demo"/>
  </a>
  &nbsp;
  <a href="https://metabolic-care-assistant-bfactskfg3axczw48u2aow.streamlit.app/">
    <img src="https://img.shields.io/badge/🌐_Live_App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Live App"/>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/LLM-Groq%20%2F%20LLaMA%203.3%2070B-F55036?style=flat-square"/>
  <img src="https://img.shields.io/badge/DB-Supabase%20PostgreSQL-3ECF8E?style=flat-square&logo=supabase&logoColor=white"/>
  <img src="https://img.shields.io/badge/Guidelines-ADA%202024%20%7C%20IDF--DAR%20%7C%20WHO-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square"/>
</p>

---

## The Problem

**Pakistan has the 3rd highest diabetes burden in the world — 33 million people, millions more undiagnosed.**

Yet access to personalised dietary guidance is expensive, clinic appointments are scarce, and most digital health tools are built for Western food culture in English. The average Pakistani patient managing diabetes is left asking:

> *"Can I eat biryani?"* &nbsp; *"How much roti is too much?"* &nbsp; *"Is my blood sugar stable enough to exercise?"*

**Apni Sehat fills this gap** — a free, bilingual, clinically-aware AI health companion that speaks the patient's language, knows their food, and routes them to professional care when it matters.

---

## What It Does

| Feature | Description |
|---|---|
| 🧙 **2-step onboarding** | Name, phone, diabetes type, height/weight (ft+inches), conditions — no account, no password, no app install |
| 🔴 **Clinical triage** | Evaluates HbA1c, BP, cholesterol and comorbidities — assigns GREEN / AMBER / RED before granting access to any features |
| 🥗 **Personalised 7-day desi meal plan** | 35 curated South Asian meals across 6 slots, filtered by conditions and dietary preferences |
| 💡 **"Why this meal?" AI explainability** | One click on any meal card reveals a clinical explanation personalised to the user's conditions — in English or Urdu |
| 🤖 **Sehat Saathi — bilingual health chatbot** | Multi-turn AI assistant that auto-detects English or Urdu, backed by ADA 2024, IDF-DAR and WHO dietary evidence |
| 📊 **Blood glucose tracker** | Log readings, view trend charts with clinical threshold lines, receive alerts |
| 📈 **AI glucose trend analysis** | One click delivers a structured 4-section clinical analysis of the user's reading patterns |
| 🔄 **AI food swaps** | Desi-appropriate, diabetes-safe alternative meals for any day |
| ✅ **Daily plan adherence** | Check-in system with AI deviation coaching when users go off-plan |

---

## Generative AI Features — In Depth

The app uses **Groq's API (LLaMA 3.3 70B)** for six distinct AI-powered features, each with a specific clinical purpose.

### 1. Sehat Saathi — Evidence-Backed Bilingual Chatbot
- Auto-detects language — responds in **Urdu script** when the user writes in Urdu, English otherwise
- Silently injected with the user's full medical profile for personalised answers
- **RAG (Retrieval-Augmented Generation)** — every user message is matched against a curated knowledge base sourced from:
  - ADA Standards of Care 2024 — Nutrition & Glycaemic Targets
  - IDF-DAR Diabetes and Ramadan Guidelines
  - WHO/South Asian Dietary Guidelines
  - Pakistan NCD Guidelines
  - GI/GL data for 20+ common desi foods
- Top 2 matching evidence chunks are silently injected into context — the LLM cites sources naturally in responses
- Strictly refuses medication advice, diagnoses, and dose changes — enforced in system prompt

### 2. "Why This Meal?" Explainability
- Every meal card has a **💡 Why this meal?** button
- The LLM receives the patient's full profile (diabetes type, BMI, hypertension, insulin status) and explains the meal in 2–3 sentences — one glycaemic benefit, one cultural/practical benefit
- Works in both English and Urdu

### 3. AI Glucose Trend Analysis
- Analyses the user's last 14 glucose readings
- Computes time-of-day averages (morning, afternoon, evening), reading-type breakdown, and trend direction
- Returns a structured 4-section report: **Pattern Summary → Time-of-Day Insights → 3 Specific Recommendations → Watch Out For**
- All recommendations are desi-context-aware and non-diagnostic

### 4. Healthy Swap Suggestions
- AI-generated, culturally relevant, diabetes-safe meal alternatives for any day in the plan

### 5. Deviation Coaching
- When a user didn't follow their plan, the LLM returns 3 personalised, encouraging tips covering portion control, carb awareness, and healthier preparation methods

All AI calls are strictly non-diagnostic, degrade gracefully when the API is unavailable, and include clinical disclaimers.

---

## Personalised Meal Frequency System

Rather than a generic "3 meals + 1 snack" structure, the app assigns one of **4 clinically-grounded profiles** based on insulin use, hypoglycaemia history, weakness between meals, and BMI.

| Profile | Structure | Who Gets It | Clinical Rationale |
|---|---|---|---|
| `3M_3S` | 3 meals + 3 snacks (incl. bedtime) | Insulin user **and** hypo episodes | Bedtime snack prevents dangerous overnight glucose drops |
| `3M_2S` | 3 meals + 2 snacks | Insulin user **or** hypo episodes **or** weakness | Mid-morning and afternoon snacks buffer inter-meal dips |
| `SMALL_3M_1S` | 3 lighter meals + 1 snack | BMI ≥ 23, Type 2, no insulin | Portion-controlled for simultaneous glucose + weight management |
| `3M_1S` | 3 meals + 1 snack | All others | Standard stable plan for well-controlled Type 2 |

**South Asian BMI thresholds** are applied throughout — overweight at 23.0, obese at 27.5, per WHO Expert Consultation recommendations.

### Meal Bank — 35 Curated Desi Meals

| Slot | Sample Meals |
|---|---|
| 🌅 Breakfast | Besan chilla + yogurt, dalia + almonds, moong daal chilla, oats + chia |
| 🍎 Mid-Morning Snack | Boiled egg + cucumber, roasted chana, yogurt + flaxseeds |
| ☀️ Lunch | Daal maash + roti, chana curry + raita, grilled chicken + sabzi |
| 🍊 Afternoon Snack | Guava, apple + almonds, roasted pumpkin seeds |
| 🌙 Dinner | Grilled fish + salad, masoor daal + roti, palak chicken |
| 🌛 Bedtime Snack | Warm low-fat milk, crackers + peanut butter, yogurt + almonds |

Every meal is tagged and filtered automatically based on conditions:

| Tag | Applied When |
|---|---|
| `low_sodium` | User has hypertension |
| `low_satfat` | User has high cholesterol |
| `veg` | User selects vegetarian |
| `light` | User is on `SMALL_3M_1S` profile |

---

## Clinical Safety Layer

Before accessing any feature, the app evaluates all provided clinical data:

| Signal | 🟢 GREEN | 🟡 AMBER | 🔴 RED |
|---|---|---|---|
| HbA1c | < 8% | 8–9% | ≥ 9% |
| Fasting glucose variability | Low | Std dev ≥ 25 | Std dev ≥ 45 or range ≥ 120 |
| Systolic BP | < 140 mmHg | 140–179 | ≥ 180 |
| Diastolic BP | < 90 mmHg | 90–119 | ≥ 120 |
| Total cholesterol | < 200 mg/dL | 200–239 | — |
| Other major conditions | — | — | Immediate RED |

🔴 **RED users are blocked from all features** and directed to seek clinical care before using the tool.

Users who answer "Not sure" on BP or cholesterol are treated conservatively (assumed positive) with a gentle recommendation to get a free clinic check. Users who select "Not sure / not diagnosed" for diabetes receive an AMBER flag, a cautious low-GI plan, and a clear message to get a fasting blood sugar test.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
│  Entry Screen → 2-Step Wizard → Main App (4 tabs)           │
│  ┌──────────┬─────────────┬────────────┬──────────────────┐ │
│  │ My Plan  │    Chat     │  Log Sugar │    Progress      │ │
│  │ Day pills│  Sehat      │  Glucose   │  Adherence +     │ │
│  │ + meal   │  Saathi     │  tracker   │  AI Trend        │ │
│  │ cards +  │  RAG-backed │  + alerts  │  Analysis        │ │
│  │ Why this │  bilingual  │            │                  │ │
│  │ meal?    │             │            │                  │ │
│  └──────────┴─────────────┴────────────┴──────────────────┘ │
└──────────────────────┬──────────────────────────────────────┘
                       │
           ┌───────────┴────────────┐
           │                        │
┌──────────▼────────┐   ┌───────────▼──────────┐
│  Groq / LLaMA     │   │  Supabase PostgreSQL  │
│  3.3 70B          │   │  (+ SQLite fallback)  │
│  · Sehat Saathi   │   │  · profiles           │
│  · Why this meal? │   │  · glucose_logs       │
│  · Swap ideas     │   │  · daily_checkins     │
│  · Coaching tips  │   └──────────────────────┘
│  · Trend analysis │
└───────────────────┘
           │
┌──────────▼──────────────────────────────────────────────┐
│                    Core Modules                         │
│  app.py          — UI, flow, session state, RAG         │
│  config.py       — MEAL_PROFILES, BMI, thresholds       │
│  planner.py      — meal frequency + plan logic          │
│  meal_bank.py    — 35-meal curated desi dataset         │
│  triage.py       — clinical safety routing              │
│  translations.py — bilingual string registry            │
│  llm.py          — Groq API (chat, swaps, coaching)     │
│  storage.py      — database abstraction layer           │
└─────────────────────────────────────────────────────────┘
```

### Privacy by Design
Phone numbers are **never stored**. A one-way SHA-256 hash with a server-side salt is used as the user identifier. Full database access cannot reveal any phone number.

---

## Project Structure

```
Apni-Sehat/
├── app.py            # Main app — all UI, RAG, AI feature integration
├── config.py         # MEAL_PROFILES, BMI thresholds, triage constants
├── planner.py        # Meal frequency assignment + 7-day plan generation
├── meal_bank.py      # 35-meal curated desi dataset across 6 slots
├── triage.py         # Clinical safety routing (GREEN / AMBER / RED)
├── llm.py            # Groq / LLaMA 3.3 — chat, swaps, coaching
├── storage.py        # Database layer (SQLAlchemy + Supabase / SQLite)
├── translations.py   # All UI strings in English and Urdu
├── requirements.txt  # Python dependencies
└── .streamlit/
    └── secrets.toml  # API keys — never committed to git
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- A [Groq API key](https://console.groq.com) — free tier is sufficient
- A [Supabase](https://supabase.com) project — free tier works, or the app runs on local SQLite automatically

### 1. Clone
```bash
git clone https://github.com/umer1556/Apni-Sehat.git
cd Apni-Sehat
```

### 2. Install
```bash
pip install -r requirements.txt
```

### 3. Configure secrets

Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY   = "your-groq-api-key"
DATABASE_URL   = "postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME"
PHONE_SALT     = "any-random-secret-string"

# Optional — defaults shown
GROQ_BASE_URL  = "https://api.groq.com/openai/v1"
GROQ_MODEL     = "llama-3.3-70b-versatile"
```

> **No Supabase?** Leave `DATABASE_URL` empty — the app falls back to a local `data.db` SQLite file automatically.

### 4. Database setup (Supabase only)

Run in the Supabase **SQL Editor**:
```sql
CREATE TABLE IF NOT EXISTS public.profiles (
    user_key             VARCHAR(80) PRIMARY KEY,
    full_name            TEXT,
    phone_last4          VARCHAR(8),
    age                  INTEGER,
    gender               TEXT,
    height_cm            INTEGER,
    weight_kg            NUMERIC,
    family_history_json  TEXT,
    diabetes_type        TEXT,
    has_hypertension     INTEGER,
    has_high_cholesterol INTEGER,
    created_at           TIMESTAMPTZ DEFAULT NOW(),
    updated_at           TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.glucose_logs (
    id           BIGSERIAL PRIMARY KEY,
    user_key     VARCHAR(80) NOT NULL,
    measured_at  TIMESTAMPTZ NOT NULL,
    logged_at    TIMESTAMPTZ DEFAULT NOW(),
    reading_type TEXT NOT NULL,
    value        NUMERIC NOT NULL,
    meal_note    TEXT
);

CREATE TABLE IF NOT EXISTS public.daily_checkins (
    id            BIGSERIAL PRIMARY KEY,
    user_key      VARCHAR(80) NOT NULL,
    checkin_date  DATE NOT NULL,
    followed_plan INTEGER NOT NULL,
    actual_meals  TEXT,
    created_at    TIMESTAMPTZ DEFAULT NOW()
);
```

> `init_db()` creates these tables automatically on first run — the SQL above is provided for manual setup and transparency.

### 5. Run
```bash
streamlit run app.py
```

---

## Deploying to Streamlit Cloud

1. Push to GitHub — ensure `.streamlit/secrets.toml` is in `.gitignore`
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → select repo and `app.py`
3. Add secrets under **Settings → Secrets**
4. Deploy — free hosting, no server management

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `sqlalchemy>=2.0` | Database ORM |
| `psycopg[binary]` | PostgreSQL driver (psycopg3) |
| `openai>=1.0` | Groq API client (OpenAI-compatible) |
| `pandas` | Data handling for the adherence dashboard |
| `matplotlib` | Glucose trend chart rendering |

---

## Disclaimers

- **Not a medical device.** For educational and supportive use only.
- **Not medication advice.** The app never suggests insulin doses, medication changes, or diagnoses.
- **Not a replacement for clinical care.** RED-triaged users are explicitly blocked and directed to a clinician.
- The meal bank should be reviewed by a registered dietitian before any real-world deployment at scale.
- AI suggestions are prompt-constrained and reviewed by our clinical advisor but are not reviewed by a clinician in real time.

---

## Roadmap

- [ ] Food photo analysis — snap a meal, get an instant carb estimate via multimodal LLM
- [ ] CSV import from glucometers and continuous glucose monitors
- [ ] Expanded meal bank (100+ dishes) validated by a registered nutritionist
- [ ] Urdu voice input for elderly users who find typing difficult
- [ ] WhatsApp bot interface for users without a data plan
- [ ] Dietitian review portal — flag high-risk users to a clinician dashboard

---

## Team

Built at the **HEC Generative AI Hackathon**:

| Name | GitHub |
|---|---|
| Muhammed Umer | [@umer1556](https://github.com/umer1556) |
| Zunaira Hawar | [@zunairakhan123](https://github.com/zunairakhan123) |
| Jaisha Khan | [@jaishakhan](https://github.com/jaishakhan) |
| Muhammad Husnain | [@MuhammadHusnain572](https://github.com/MuhammadHusnain572) |
| Dr. Fatima Farhat | [@docffarhat-prog](https://github.com/docffarhat-prog) |

> *"The meal frequency profiles and clinical triage thresholds were developed in consultation with Dr. Fatima Farhat to ensure the app's dietary guidance is clinically appropriate for Pakistani patients managing diabetes."*

---

## License

MIT License — see `LICENSE` for details.
