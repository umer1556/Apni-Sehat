# 🩺 Apni Sehat — اپنی صحت

> **Your Personal Diabetes Health Companion**  
> **HEC GenAI Hackathon 2025 Submission**  
> **Bilingual AI-powered diabetes companion for Pakistan** — personalised desi meal plans, evidence-backed health chat, blood sugar tracking, and clinical triage. Built for the 33 million Pakistanis living with diabetes.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/LLM-Groq%20%2F%20LLaMA%203.3%2070B-F55036?style=flat-square"/>
  <img src="https://img.shields.io/badge/DB-PostgreSQL%20%2B%20SQLite-3ECF8E?style=flat-square"/>
  <img src="https://img.shields.io/badge/Guidelines-ADA%202024%20%7C%20IDF--DAR%20%7C%20PHL%202023%20%7C%20PES-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square"/>
</p>

<p align="center">
  <strong>Clinical advisor:</strong> Dr. Fatima Farhat
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
| 🌐 **Full Urdu/English toggle** | Every UI string, every prompt, and every AI response stays in the user’s selected language |
| 🔴 **Clinical triage** | Evaluates HbA1c, BP, cholesterol and comorbidities — assigns GREEN / AMBER / RED before granting access to any features |
| 🥗 **Personalised 7-day desi meal plan** | 39 curated South Asian meals across 6 slots, filtered by conditions and dietary preferences, with 4 clinical meal-frequency profiles |
| 💡 **"Why this meal?" AI explainability** | One click on any meal card reveals a clinical explanation personalised to the user's conditions — in English or Urdu |
| 🤖 **Sehat Saathi — bilingual health chatbot** | Multi-turn RAG chatbot backed by ADA 2024, IDF-DAR and WHO dietary evidence, with source-aware responses |
| 📊 **Blood glucose tracker** | Log readings, view trend charts with clinical threshold lines, receive alerts |
| 📈 **AI glucose trend analysis** | Structured clinical analysis of the user’s last 14 readings with time-of-day insights and practical actions |
| 🔄 **AI food swaps** | Desi-appropriate, diabetes-safe alternative meals for any day in the plan |
| ✅ **Daily plan adherence** | Check-in system with duplicate-safe upsert guard and AI deviation coaching when users go off-plan |
| 🔒 **Privacy-first identity** | Raw phone number is never stored — user identity uses one-way HMAC-SHA256 hashing with a server-side secret |

---

## Generative AI Features — In Depth

The app uses **Groq's API (LLaMA 3.3 70B)** for **five distinct AI-powered features**, each with a specific clinical purpose.

### 1. Sehat Saathi — Evidence-Backed Bilingual Chatbot
- Responds in **English or Urdu** based on the user’s selected language
- Silently injected with the user's medical profile for personalised answers
- **RAG (Retrieval-Augmented Generation)** — every user message is matched against a curated knowledge base sourced from:
  - ADA Standards of Care 2024 — Nutrition & Glycaemic Targets
  - IDF-DAR Diabetes and Ramadan Guidelines 2021
  - WHO / South Asian Dietary Guidelines
  - Pakistan NCD Guidelines
  - GI/GL values for common desi foods (Foster-Powell et al., Atkinson et al.)
- Top evidence chunks are injected into context for grounded answers
- Strictly refuses medication advice, diagnoses, and dose changes — enforced at the system prompt level

### 2. "Why This Meal?" Explainability
- Every meal card has a **💡 Why this meal?** button
- The LLM receives the patient’s profile and explains the meal in 2–3 sentences:
  - one glycaemic / metabolic benefit
  - one cultural or practical benefit
- Available in both English and Urdu

### 3. AI Glucose Trend Analysis
- Analyses the user’s **last 14 glucose readings**
- Reviews time-of-day patterns (morning / afternoon / evening) and risk signals
- Returns a structured response with:
  - **Pattern Summary**
  - **Time-of-Day Insights**
  - **3 Practical Actions**
  - **Watch Out For**
- Non-diagnostic and clinically cautious by design

### 4. Healthy Swap Suggestions
- AI-generated, culturally relevant, diabetes-safe alternatives for meals in the user’s plan
- Supports English and Urdu output
- Designed for realistic South Asian household food choices (not generic Western swaps)

### 5. Deviation Coaching
- If a user logs what they actually ate instead of the plan, the app gives:
  - kind encouragement
  - portion guidance
  - carb awareness tips
  - healthier prep suggestions
- Delivered in the user’s selected language for better adherence and usability

> All AI calls degrade gracefully when the API is unavailable, use retry/backoff handling, and include clear safety messaging.

---

## Personalised Meal Frequency System

The app assigns one of **4 clinically-grounded profiles** based on insulin use, hypoglycaemia history, weakness between meals, and BMI.

| Profile | Structure | Who Gets It | Clinical Rationale |
|---|---|---|---|
| `3M_3S` | 3 meals + 3 snacks (incl. bedtime) | Insulin user **and** hypo episodes | Bedtime snack helps reduce risk of overnight glucose drops — ADA Standards of Care 2024 |
| `3M_2S` | 3 meals + 2 snacks | Insulin user **or** hypo episodes **or** weakness between meals | Mid-morning and afternoon snacks help buffer inter-meal glucose dips |
| `SMALL_3M_1S` | 3 lighter meals + 1 snack | BMI ≥ 23, Type 2, no insulin | Portion-controlled for glucose + weight management in South Asian populations |
| `3M_1S` | 3 meals + 1 snack | All others | Standard nutrition structure for stable Type 2 management |

**South Asian BMI thresholds** are applied throughout — overweight at **≥ 23.0**, obese at **≥ 27.5**, reflecting higher metabolic risk at lower BMI in South Asian populations.

### Meal Bank — 39 Curated Desi Meals

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
| `low_sodium` | User has hypertension — per DASH / Pakistan hypertension guidance |
| `low_satfat` | User has high cholesterol — per lipid management guidance |
| `veg` | User selects vegetarian preference |
| `light` | User is on `SMALL_3M_1S` portion-controlled profile |
| `high_fiber` | Prioritised where possible for improved satiety and glycaemic control |

---

## Clinical Accuracy

All key thresholds are sourced and cited inline in the codebase (`config.py`) and used consistently across triage and guidance.

| Threshold | Value | Source |
|---|---|---|
| Hypertensive crisis | ≥ 180/120 mmHg | PHL Guidelines 2023 / ESC-ESH |
| Stage 2 hypertension | ≥ 140/90 mmHg | PHL Guidelines 2023 |
| Hypoglycaemia | < 70 mg/dL | ADA Standards of Care 2024 |
| Urgent glucose action | ≥ 250 mg/dL | IDF-DAR Ramadan Guidelines 2021 |
| HbA1c well-controlled | < 7.0% | ADA 2024 + Pakistan Endocrine Society |
| HbA1c RED trigger | ≥ 9.0% | ADA 2024 |
| Overweight (South Asian) | BMI ≥ 23.0 | WHO Expert Consultation |

**GI values** in the meal knowledge base are sourced from Foster-Powell et al. and Atkinson et al. and used for educational support only.

---

## Clinical Safety Layer

Before accessing any feature, every user’s data passes through `triage.py` — a fully cited, independently tested safety module.

### Triage Outcomes

| 🟢 GREEN | 🟡 AMBER | 🔴 RED |
|---|---|---|
| Full access — values within clinical targets | Full access with warnings — one or more values above goal or uncertain | **Blocked** — directed to seek clinical care before using the app |

### RED Triggers — any one is sufficient to block access

| Signal | Threshold | Guideline Source |
|---|---|---|
| Other major conditions | Any (kidney disease, heart disease, pregnancy, etc.) | Clinical safety — immediate referral |
| Blood pressure | ≥ 180 systolic **or** ≥ 120 diastolic | PHL 2023 — hypertensive crisis |
| HbA1c | ≥ 9.0% | ADA Standards of Care 2024 |
| Any single fasting glucose | ≥ 250 mg/dL | IDF-DAR Ramadan Guidelines 2021 |
| Fasting glucose variability | Range ≥ 120 mg/dL **or** SD ≥ 45 mg/dL | Safety screening flag |

### AMBER Triggers — user proceeds with warnings

| Signal | Threshold | Guideline Source |
|---|---|---|
| Blood pressure | ≥ 140 systolic **or** ≥ 90 diastolic | PHL 2023 |
| HbA1c | > 7.0% | ADA 2024 + PES |
| HbA1c stronger warning | ≥ 8.0% | PES (pragmatic upper target in some cases) |
| Any fasting glucose | < 70 mg/dL | ADA 2024 |
| Any fasting glucose | > 130 mg/dL pre-meal | ADA 2024 |
| Fasting variability | SD ≥ 25 mg/dL | Screening flag (non-diagnostic) |
| Total cholesterol | ≥ 200 mg/dL | Standard lipid risk threshold |
| Hypertension/high cholesterol ticked, no values given | — | Conservative safety default |
| No clinical data provided at all | — | Cannot assess risk — cautious AMBER |

### Handling Uncertainty

Users who answer **“Not sure”** for blood pressure or cholesterol are treated conservatively for safety and shown a gentle prompt to get checked. Users unsure of their diabetes status receive a cautious AMBER route and a clear recommendation to seek diagnostic testing.

---

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
│  Entry Screen → 2-Step Wizard → Main App (4 tabs)          │
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
│  Groq / LLaMA     │   │  SQLAlchemy Storage   │
│  3.3 70B          │   │  PostgreSQL / SQLite  │
│  · Sehat Saathi   │   │  · profiles           │
│  · Why this meal? │   │  · glucose_logs       │
│  · Swap ideas     │   │  · daily_checkins     │
│  · Coaching tips  │   └──────────────────────┘
│  · Trend analysis │
└───────────────────┘
           │
┌──────────▼──────────────────────────────────────────────┐
│                    Core Modules                         │
│  app.py          — UI, flow, routing, RAG integration   │
│  config.py       — thresholds + meal profiles           │
│  planner.py      — meal frequency + plan generation     │
│  meal_bank.py    — 39-meal curated desi dataset         │
│  triage.py       — safety routing (GREEN/AMBER/RED)     │
│  translations.py — bilingual string registry (en/ur)    │
│  llm.py          — Groq API (chat, swaps, coaching)     │
│  storage.py      — DB abstraction + upsert guards       │
└─────────────────────────────────────────────────────────┘
```

### Privacy by Design
Raw phone numbers are **never stored**. A one-way **HMAC-SHA256** hash (with a server-side secret via `PHONE_SALT`) is used as the user identifier.

---

## Project Structure

```text
Apni-Sehat/
├── app.py            # Main app — UI, navigation, RAG, AI feature integration
├── config.py         # Clinical thresholds + meal profiles (with inline citations)
├── planner.py        # 7-day meal plan generator (deduplication, clinical filters)
├── meal_bank.py      # Curated desi meal dataset (39 meals, tagged slots)
├── triage.py         # Clinical safety routing — GREEN / AMBER / RED
├── llm.py            # Groq / LLaMA 3.3 — chat, swaps, coaching, trend analysis
├── storage.py        # SQLAlchemy layer (PostgreSQL + SQLite fallback, upsert guard)
├── translations.py   # English + Urdu UI strings (full parity across app)
├── requirements.txt  # Python dependencies
└── .streamlit/
    └── secrets.toml  # API keys — never commit to git
```

### Module Responsibilities

**`config.py`** — Single source of truth for clinical thresholds and meal profile logic. All clinical values are documented and easy to update by doctor/clinical teammates.

**`triage.py`** — Safety gate. RED users are blocked and advised to seek care. AMBER users can proceed with warnings. GREEN users get full access.

**`planner.py`** — Builds the 7-day meal plan using randomised, deduplicated selection to minimise repetition while preserving dietary and clinical filters.

**`meal_bank.py`** — Curated desi meal dataset with tags such as `veg`, `low_sodium`, `low_satfat`, `high_fiber`, and `light`.

**`llm.py`** — Handles all Groq LLM calls (chatbot, swaps, meal explainability, coaching, trend analysis) with language-aware prompts, retry/backoff, and safe fallbacks.

**`storage.py`** — Database layer with PostgreSQL + SQLite support, Streamlit-friendly connection handling, and one-check-in-per-day upsert protection to avoid adherence inflation.

**`translations.py`** — Central registry of all app strings in English and Urdu, keeping UI and AI feature labels consistent across both languages.

---

## Getting Started

### Prerequisites
- Python 3.10+
- A [Groq API key](https://console.groq.com) — free tier is sufficient
- A PostgreSQL database URL (e.g. [Supabase](https://supabase.com)) **or** leave it blank to use local SQLite automatically

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
GROQ_MODEL     = "llama-3.3-70b-versatile"
GROQ_BASE_URL  = "https://api.groq.com/openai/v1"

# PostgreSQL (optional — leave blank for SQLite fallback)
DATABASE_URL   = "postgresql+psycopg://USER:PASSWORD@HOST:PORT/DBNAME"

# Required for privacy-safe user identity hashing
PHONE_SALT     = "any-random-secret-string"
```

> **No Supabase?** Leave `DATABASE_URL` empty — the app falls back to a local SQLite file automatically.

### 4. Database setup (Supabase / PostgreSQL only)

Run in the Supabase **SQL Editor** (optional — `init_db()` can also create tables automatically on first run):

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

### 5. Run
```bash
streamlit run app.py
```

App opens at: `http://localhost:8501`

---

## Deploying to Streamlit Cloud

1. Push to GitHub — ensure `.streamlit/secrets.toml` is in `.gitignore`
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo and `app.py`
4. Add secrets under **Settings → Secrets**
5. Deploy — free hosting, no server management

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `sqlalchemy>=2.0` | Database ORM / DB abstraction |
| `psycopg[binary]` | PostgreSQL driver (optional if using PostgreSQL) |
| `openai>=1.0` | Groq API client (OpenAI-compatible) |
| `pandas` | Data handling for logs and adherence tracking |
| `matplotlib` | Glucose trend chart rendering |

### Minimum Requirements
```txt
streamlit>=1.30.0
openai>=1.0.0
sqlalchemy>=2.0.0
pandas>=2.0.0
matplotlib>=3.7.0
psycopg[binary]>=3.0.0   # optional — for PostgreSQL
```

---

## Known Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| RAG uses TF-IDF + n-gram cosine (no embeddings) | May miss strongly paraphrased queries | Broad keyword coverage and cosine similarity improve partial matching |
| Groq API dependency | AI features may be unavailable temporarily | Retry/backoff + graceful fallbacks + clear user-facing error messages |
| Meal bank has 39 meals | Some slots may repeat after several days | Deduplicated selection reduces consecutive repeats |

---

## Disclaimers

- **Not a medical device.** For educational and supportive use only.
- **Not medication advice.** The app never suggests insulin doses, medication changes, or diagnoses.
- **Not a replacement for clinical care.** RED-triaged users are explicitly blocked and directed to a clinician.
- The meal bank should be reviewed by a registered dietitian before any real-world deployment at scale.
- AI suggestions are prompt-constrained and clinically reviewed at design level, but not reviewed by a clinician in real time.

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

| Name | Role | GitHub |
|---|---|---|
| Muhammed Umer | Front-end developer | [@umer1556](https://github.com/umer1556) |
| Zunaira Hawar | Front-end developer | [@zunairakhan123](https://github.com/zunairakhan123) |
| Jaisha Khan | Back-end developer | [@jaishakhan](https://github.com/jaishakhan) |
| Muhammad Husnain | Back-end developer | [@MuhammadHusnain572](https://github.com/MuhammadHusnain572) |
| Dr. Fatima Farhat | Clinical advisor | [@docffarhat-prog](https://github.com/docffarhat-prog) |

> *"The clinical triage thresholds, meal frequency profiles, and safety routing logic were developed and reviewed in consultation with Dr. Fatima Farhat to ensure the app's guidance is clinically appropriate for Pakistani patients managing diabetes."*

---

## License

MIT License — see `LICENSE` for details.
