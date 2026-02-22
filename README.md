# 🩺 Apni Sehat — اپنی صحت

> **Bilingual AI-powered diabetes companion for Pakistan** — personalised desi meal plans, evidence-backed health chat, blood sugar tracking, and clinical triage. Built for the 33 million Pakistanis living with diabetes.

  &nbsp;
  <a href="(https://apni-sehat-jylam9hhimsvsstqtxoutx.streamlit.app/)">
    <img src="https://img.shields.io/badge/🌐_Live_App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Live App"/>
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/LLM-Groq%20%2F%20LLaMA%203.3%2070B-F55036?style=flat-square"/>
  <img src="https://img.shields.io/badge/DB-Supabase%20PostgreSQL-3ECF8E?style=flat-square&logo=supabase&logoColor=white"/>
  <img src="https://img.shields.io/badge/Guidelines-ADA%202024%20%7C%20IDF--DAR%20%7C%20PHL%202023%20%7C%20PES-blue?style=flat-square"/>
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
| 🤖 **Sehat Saathi — bilingual health chatbot** | Multi-turn AI assistant backed by ADA 2024, IDF-DAR and WHO dietary evidence via RAG |
| 📊 **Blood glucose tracker** | Log readings, view trend charts with clinical threshold lines, receive alerts |
| 📈 **AI glucose trend analysis** | Structured 4-section clinical analysis of the user's reading patterns |
| 🔄 **AI food swaps** | Desi-appropriate, diabetes-safe alternative meals for any day |
| ✅ **Daily plan adherence** | Check-in system with AI deviation coaching when users go off-plan |

---

## Generative AI Features — In Depth

The app uses **Groq's API (LLaMA 3.3 70B)** for six distinct AI-powered features, each with a specific clinical purpose.

### 1. Sehat Saathi — Evidence-Backed Bilingual Chatbot
- Auto-detects language — responds in **Urdu script** or English based on the user's input
- Silently injected with the user's full medical profile for personalised answers
- **RAG (Retrieval-Augmented Generation)** — every user message is matched against a curated knowledge base sourced from:
  - ADA Standards of Care 2024 — Nutrition & Glycaemic Targets
  - IDF-DAR Diabetes and Ramadan Guidelines 2021
  - WHO / South Asian Dietary Guidelines
  - Pakistan NCD Guidelines
  - GI/GL values for 20+ common desi foods (Foster-Powell et al.)
- Top 2 matching evidence chunks are injected into context — the LLM cites sources naturally in responses
- Strictly refuses medication advice, diagnoses, and dose changes — enforced at the system prompt level

### 2. "Why This Meal?" Explainability
- Every meal card has a **💡 Why this meal?** button
- The LLM receives the patient's full clinical profile and explains the meal in 2–3 sentences — one glycaemic benefit, one cultural/practical benefit
- Available in both English and Urdu

### 3. AI Glucose Trend Analysis
- Analyses the user's last 14 glucose readings
- Computes time-of-day averages (morning / afternoon / evening), reading-type breakdown, and trend direction
- Returns a structured 4-section report: **Pattern Summary → Time-of-Day Insights → 3 Specific Recommendations → Watch Out For**
- All recommendations are desi-context-aware and non-diagnostic

### 4. Healthy Swap Suggestions
- AI-generated, culturally relevant, diabetes-safe alternatives for any day in the plan

### 5. Deviation Coaching
- When a user didn't follow their plan, the LLM returns 3 personalised encouraging tips covering portion control, carb awareness, and healthier preparation methods

### 6. Meal Plan Generation
- Dynamically generated 7-day plan filtered by diabetes type, conditions, dietary preferences, BMI, and insulin status

All AI calls degrade gracefully when the API is unavailable and include clinical disclaimers.

---

## Personalised Meal Frequency System

The app assigns one of **4 clinically-grounded profiles** based on insulin use, hypoglycaemia history, weakness between meals, and BMI.

| Profile | Structure | Who Gets It | Clinical Rationale |
|---|---|---|---|
| `3M_3S` | 3 meals + 3 snacks (incl. bedtime) | Insulin user **and** hypo episodes | Bedtime snack prevents dangerous overnight glucose drops — ADA Standards of Care 2024, Section 5 |
| `3M_2S` | 3 meals + 2 snacks | Insulin user **or** hypo episodes **or** weakness between meals | Mid-morning and afternoon snacks buffer inter-meal glucose dips — PES meal frequency guidance |
| `SMALL_3M_1S` | 3 lighter meals + 1 snack | BMI ≥ 23, Type 2, no insulin | Portion-controlled for simultaneous glucose and weight management — ADA/PES weight management guidance |
| `3M_1S` | 3 meals + 1 snack | All others | Standard ADA nutrition therapy for stable Type 2 |

**South Asian BMI thresholds** are applied throughout — overweight at ≥ 23.0, obese at ≥ 27.5, per the WHO Expert Consultation on Asian BMI thresholds (2004), adopted by the Pakistan NCD Programme. These are lower than Western thresholds (25.0 / 30.0) and correctly reflect higher metabolic risk at lower BMI in South Asian populations.

### Meal Bank — 35 Curated Desi Meals

| Slot | Sample Meals |
|---|---|
| 🌅 Breakfast | Besan chilla + yogurt, dalia + almonds, moong daal chilla, oats + chia |
| 🍎 Mid-Morning Snack | Boiled egg + cucumber, roasted chana, yogurt + flaxseeds |
| ☀️ Lunch | Daal maash + roti, chana curry + raita, grilled chicken + sabzi |
| 🍊 Afternoon Snack | Guava, apple + almonds, roasted pumpkin seeds |
| 🌙 Dinner | Grilled fish + salad, masoor daal + roti, palak chicken |
| 🌛 Bedtime Snack | Warm low-fat milk, crackers + peanut butter, yogurt + almonds |

Every meal is tagged and filtered automatically:

| Tag | Applied When |
|---|---|
| `low_sodium` | User has hypertension — per DASH diet / Pakistan Hypertension League |
| `low_satfat` | User has high cholesterol — per Pakistan Society of Cardiology |
| `veg` | User selects vegetarian preference |
| `light` | User is on `SMALL_3M_1S` portion-controlled profile |

---

## Clinical Safety Layer

Before accessing any feature, every user's data passes through `triage.py` — a fully cited, independently tested safety module. The logic is covered by **14 automated test cases** verifying correct routing across all clinical scenarios.

### Triage Outcomes

| 🟢 GREEN | 🟡 AMBER | 🔴 RED |
|---|---|---|
| Full access — all values within clinical targets | Full access with appropriate warnings — one or more values above goal | **Blocked** — directed to seek clinical care before using the app |

### RED Triggers — any one is sufficient to block access

| Signal | Threshold | Guideline Source |
|---|---|---|
| Other major conditions | Any (kidney disease, heart disease, pregnancy, etc.) | Clinical safety — immediate referral |
| Blood pressure | ≥ 180 systolic **or** ≥ 120 diastolic | PHL 2023 — hypertensive crisis |
| HbA1c | ≥ 9.0% | ADA Standards of Care 2024 |
| Any single fasting glucose | ≥ 250 mg/dL | IDF-DAR Ramadan Guidelines 2021 |
| Fasting glucose variability | Range ≥ 120 mg/dL **or** SD ≥ 45 mg/dL | Battelino et al. *Diabetes Care* 2019 |

### AMBER Triggers — user proceeds with clinical warnings

| Signal | Threshold | Guideline Source |
|---|---|---|
| Blood pressure | ≥ 140 systolic **or** ≥ 90 diastolic | Pakistan Hypertension League (PHL) 2023 |
| HbA1c | > 7.0% — any elevation above goal | ADA 2024 + Pakistan Endocrine Society (PES) |
| HbA1c stronger warning | ≥ 8.0% | PES — accepted upper limit for elderly/complex patients |
| Any fasting glucose | < 70 mg/dL | ADA 2024 — Level 1 hypoglycaemia |
| Any fasting glucose | > 130 mg/dL pre-meal | ADA 2024 — above pre-meal target range |
| Fasting variability | SD ≥ 25 mg/dL | Pragmatic screening threshold† |
| Total cholesterol | ≥ 200 mg/dL | Pakistan Society of Cardiology / NCEP ATP III |
| Hypertension or high cholesterol ticked, no values given | — | Conservative default |
| No clinical data provided at all | — | Cannot assess risk — cautious AMBER |

> **† Note on variability thresholds:** The fasting SD and range thresholds are pragmatic screening flags. Clinical glycaemic variability is formally measured using Coefficient of Variation (CV% >36% = high variability, Danne et al. *Diabetes Care* 2017). Our proxy uses SD of a small fasting readings sample — described in the UI as a "screening flag" rather than a diagnostic threshold, and reviewed by our clinical advisor.

### Handling Uncertainty

Users who answer "Not sure" on blood pressure or cholesterol are treated conservatively (assumed positive for safety) and shown a gentle prompt to get a free clinic check. Users who select "Not sure / not diagnosed" for diabetes receive an AMBER flag, a cautious low-GI plan, and a direct message to get a fasting blood sugar test.

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
│  config.py       — thresholds with full source citations│
│  planner.py      — meal frequency + plan generation     │
│  meal_bank.py    — 35-meal curated desi dataset         │
│  triage.py       — safety routing (14 automated tests)  │
│  translations.py — bilingual string registry            │
│  llm.py          — Groq API (chat, swaps, coaching)     │
│  storage.py      — database abstraction layer           │
└─────────────────────────────────────────────────────────┘
```

### Privacy by Design
Phone numbers are **never stored**. A one-way SHA-256 hash with a server-side salt is used as the user identifier. Even with full database access, no phone number can be recovered.

---

## Project Structure

```
Apni-Sehat/
├── app.py            # Main app — all UI, RAG, AI feature integration
├── config.py         # Clinical thresholds with full guideline citations
├── planner.py        # Meal frequency assignment + 7-day plan generation
├── meal_bank.py      # 35-meal curated desi dataset across 6 slots
├── triage.py         # Clinical safety routing — GREEN / AMBER / RED
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

> `init_db()` creates these tables automatically on first run — the SQL above is for manual setup and transparency.

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

- [ ] Food photo analysis — snap a meal, get a carb estimate via multimodal LLM
- [ ] CSV import from glucometers and continuous glucose monitors
- [ ] Expanded meal bank (100+ dishes) validated by a registered nutritionist
- [ ] Age-adjusted A1c targets for elderly users (≥ 65 years)
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

> *"The clinical triage thresholds, meal frequency profiles, and safety routing logic were developed and reviewed in consultation with Dr. Fatima Farhat to ensure the app's guidance is clinically appropriate for Pakistani patients managing diabetes."*

---

## License

MIT License — see `LICENSE` for details.
