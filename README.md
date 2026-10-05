<div align="center">

# ◈ AI Risk Engine

### Financial Text → Risk Signals → Portfolio Stress

**An explainable AI/NLP risk intelligence engine for financial events**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)

![NLP](https://img.shields.io/badge/NLP-Financial_Text-6C5CE7?style=for-the-badge)

![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

![Status](https://img.shields.io/badge/Status-In_Development-F59E0B?style=for-the-badge)

**Turn unstructured financial information into structured, explainable risk signals for downstream portfolio stress analysis.**

</div>

---

## ◇ Why this project?

Financial risk rarely arrives as a neat number. It appears as an earnings announcement, regulatory filing, geopolitical development, supply-chain disruption, or macroeconomic signal.

**AI Risk Engine** transforms these signals into a machine-readable risk layer while preserving the evidence behind each result.

```text

┌─────────────────────┐

│  FINANCIAL SOURCES  │

│  SEC EDGAR          │

│  GDELT GKG          │

└──────────┬──────────┘

           ▼

┌─────────────────────┐

│   INGESTION +       │

│   NORMALIZATION     │

└──────────┬──────────┘

           ▼

┌─────────────────────┐

│     AI RISK ENGINE  │

│  Sentiment          │

│  Event Classifier   │

│  Impact Scoring     │

│  Explainability     │

└──────────┬──────────┘

           ▼

┌─────────────────────┐

│ RISK INTELLIGENCE   │

│ Evidence + Exposure │

│ Risk Propagation    │

└──────────┬──────────┘

           ▼

┌─────────────────────┐

│ PORTFOLIO STRESS    │

│ TESTING             │

└─────────────────────┘

```

## ◇ Core problem

Traditional financial analysis can require analysts to manually read large volumes of text before answering:

- **What happened?**

- **Who is exposed?**

- **How severe is it?**

- **What could the event mean for a portfolio?**

The project automates the first layer of this workflow and converts unstructured information into structured signals that feed a downstream stress-testing module.

---

# ◇ Data Layer

The current ingestion pipeline uses two complementary public sources.

| Source | Contribution | Current role |

|---|---|---|

| **SEC EDGAR** | Company filings and disclosures | Primary source of financial text |

| **GDELT GKG** | Global news metadata, financial themes, organizations and tone | External event context |

### SEC EDGAR

The SEC pipeline extracts filing metadata and substantive filing/exhibit text into a normalized representation. Current processed examples include company financial results, revenue, EPS, margins, tariff effects and disclosed risk language.

### GDELT GKG

GDELT's Global Knowledge Graph provides structured context around news coverage, including financial themes, organizations, sources, URLs, article counts and tone.

The implementation deliberately does **not** fabricate article body text from GDELT metadata:

```text

SEC   → text_available = True

GDELT → text_available = False

```

This distinction is preserved in the unified representation.

---

# ◇ Unified Document Architecture

Both sources are normalized into a common `FinancialDocument` structure:

```python

FinancialDocument(

    *source*=...,

    *timestamp*=...,

    *title*=...,

    *text*=...,

    *url*=...,

    *entity*=...,

    *document_type*=...,

    *text_available*=...,

    *metadata*={...}

)

```

Source-specific information stays inside `metadata`, so downstream components consume one consistent interface without losing useful source information.

```text

             ┌───────────────┐

             │   SEC EDGAR   │

             └───────┬───────┘

                     ▼

              ┌──────────────┐

              │ FinancialDoc │

              └──────────────┘

                     ▲

                     │

             ┌───────┴───────┐

             │   GDELT GKG   │

             └───────────────┘

```

---

# ◇ AI Risk Engine

The current risk engine is implemented incrementally as a transparent, testable pipeline:

```text

Financial Text

      │

      ▼

FinBERT Sentiment

      │

      ▼

Rule-based Event Classification

      │

      ▼

Transparent Impact Scoring

      │

      ▼

Unified Risk Signal

      │

      ▼

Explainable Evidence

```

### 01 · Financial Sentiment

The engine uses **ProsusAI/FinBERT** to classify financial text as positive, neutral or negative.

A normalized sentiment score is calculated as:

```text

-1.0  ◄────────────────►  +1.0

negative                  positive

```

Long documents are split into token-bounded chunks and analyzed across the full document rather than relying on a truncated prefix.

### 02 · Event Classification

The current event classifier is a **transparent rule-based baseline**. It identifies financially meaningful event categories using domain-specific keyword evidence.

Current categories include:

```text

Earnings

M&A

Credit Event

Regulatory

Geopolitical

Macroeconomic

Product / Business

Litigation

Unknown

```

The classifier returns the selected event, an evidence-based confidence score, and the matched keywords.

This is intentionally interpretable and provides a clear baseline for later evaluation or replacement with a learned classifier.

### 03 · Impact Scoring

Each detected event receives a transparent severity signal on a **1–10** scale.

The current scoring layer combines:

- Event-type severity

- Sentiment adjustment

- Event evidence/confidence

The design explicitly avoids treating generic negative sentiment as equivalent to financial impact.

Conceptually:

```text

Impact

  =

Event Severity

+ Sentiment Adjustment

+ Evidence Adjustment

```

The result is clipped to the `1–10` range.

### 04 · Unified Risk Signal

The individual outputs are combined into one structured signal containing:

- Entity

- Sentiment label and score

- Event type and confidence

- Matched evidence

- Impact score

- Impact components

- Overall risk level

Current risk bands:

```text

1–4.99   → LOW

5–7.99   → MEDIUM

8–10     → HIGH

```

### 05 · Explainability

Every generated signal retains the evidence used to produce it.

Example reasoning structure:

```text

Event classified as earnings.

Supporting evidence: earnings, revenue, financial results, ...

Sentiment is broadly neutral (+0.08).

Calculated event impact is 6.70/10.

```

---

# ◇ Validated Example: Apple Inc.

The current end-to-end risk engine has been validated against a processed Apple 8-K filing.

```text

Entity

Apple Inc.

Sentiment

Neutral

Score: +0.0779

Event

Earnings

Confidence: 0.4286

Impact

6.70 / 10

Risk Level

MEDIUM

```

The result demonstrates the complete Day 3 pipeline:

```text

Apple 8-K

   ↓

FinBERT

   ↓

Neutral sentiment (+0.0779)

   ↓

Earnings classification

   ↓

Impact = 6.70 / 10

   ↓

Medium risk

   ↓

Human-readable explanation

```

The event confidence is an evidence ratio from the current rule-based classifier. It is **not presented as a calibrated probability**.

---

# ◇ Differentiator: Risk Propagation

A headline does not necessarily stop at the company mentioned in the headline.

```text

EVENT

  │

  ▼

COMPANY

  │

  ▼

SECTOR

  │

  ▼

PORTFOLIO EXPOSURE

```

The intended system moves beyond:

*> "This article is negative."*

toward:

*> "This event affects this entity, through this financial mechanism, with this level of portfolio exposure."*

This is the next major engineering layer after the completed risk engine.

---

# ◇ Downstream Module: Strategic Event-Driven Stress Testing

The selected downstream module is **portfolio stress testing**.

```text

Detected Event

      │

      ▼

Risk Signal

      │

      ▼

Exposure Mapping

      │

      ▼

Scenario Shock

      │

      ▼

Portfolio Impact

```

The stress-testing output is intended as **scenario analysis**, not a prediction of future market prices.

The final interface will allow users to explore counterfactual questions such as:

```text

"What happens to the portfolio

 if this event produces a larger shock?"

```

---

# ◇ Explainability

A central design principle is:

_>&#x20;_**Every important risk signal should have evidence behind it.**

Rather than exposing only:

```text

RISK = HIGH

```

the target reasoning chain is:

```text

Source

  ↓

Financial evidence

  ↓

Entity

  ↓

Detected event

  ↓

Sentiment

  ↓

Impact

  ↓

Exposure

  ↓

Stress scenario

```

This makes the system easier to audit, debug and defend.

---

# ◇ Current Project Structure

```text

AI-Risk-Engine/

│

├── data/

│   ├── raw/

│   │   ├── gdelt/

│   │   └── edgar/

│   ├── processed/

│   └── demo/

│

├── src/

│   ├── ingestion/

│   │   ├── edgar_loader.py

│   │   ├── gdelt_gkg_loader.py

│   │   ├── schema.py

│   │   └── test_edgar.py

│   │

│   ├── preprocessing/

│   │   ├── cleaner.py

│   │   ├── processor.py

│   │   ├── test_cleaner.py

│   │   └── test_processor.py

│   │

│   ├── pipeline/

│   │   ├── __init__.py

│   │   └── unified.py

│   │

│   └── risk_engine/

│       ├── __init__.py

│       ├── sentiment.py

│       ├── event_classifier.py

│       ├── impact_scorer.py

│       ├── risk_signal.py

│       ├── explanation.py

│       └── test_risk_signal.py

│

├── experiments/

├── tests/

├── docs/

├── README.md

├── requirements.txt

├── .gitignore

└── LICENSE

```

---

# ◇ Current Build Status

| Component | Status |

|---|:---:|

| Project structure | ✅ |

| SEC EDGAR ingestion | ✅ |

| SEC filing/exhibit extraction | ✅ |

| SEC text cleaning | ✅ |

| GDELT GKG ingestion | ✅ |

| GDELT financial-theme filtering | ✅ |

| Common `FinancialDocument` schema | ✅ |

| SEC → unified document | ✅ |

| GDELT → unified document | ✅ |

| Unified document saver | ✅ |

| Financial sentiment model | ✅ |

| Long-document sentiment chunking | ✅ |

| Event classifier | ✅ |

| Impact scoring | ✅ |

| Unified risk signal | ✅ |

| Explainability | ✅ |

| Risk propagation | ⏳ |

| Portfolio stress testing | ⏳ |

| FastAPI service | ⏳ |

| Interactive dashboard | ⏳ |

| Evaluation & benchmarking | ⏳ |

| Demo | ⏳ |

_>&#x20;_**Current milestone:**_&#x20;The ingestion foundation and core AI Risk Engine are complete and validated end-to-end. The next milestone is connecting risk signals to entity/sector exposure and portfolio-level stress scenarios._

---

# ◇ Day-by-Day Build Progress

### Day 1 · Data Foundation

- Initialized the project architecture and Git repository

- Implemented SEC EDGAR ingestion

- Extracted filing metadata and 8-K exhibits

- Added SEC text cleaning and preprocessing

- Implemented GDELT GKG bulk ingestion

- Added financial-theme filtering

- Created the common `FinancialDocument` schema

- Added unified document persistence

### Day 2 · Data Validation & Normalization

- Validated SEC filing/exhibit extraction

- Tested GDELT financial-theme filtering

- Preserved GDELT organizations, themes, source URLs and financial domains

- Preserved GDELT tone metadata

- Established reproducible raw/processed data paths

- Verified both sources against the unified document schema

### Day 3 · AI Risk Engine

- Integrated FinBERT financial sentiment analysis

- Added long-document chunking

- Implemented transparent rule-based event classification

- Added keyword evidence extraction

- Implemented transparent impact scoring

- Built the unified risk signal

- Added human-readable risk explanations

- Validated the complete pipeline on an Apple 8-K filing

**Validated Apple result:**

```text

Sentiment: Neutral (+0.0779)

Event: Earnings

Confidence: 0.4286

Impact: 6.70 / 10

Risk: Medium

```

---

# ◇ Technology Stack

| Layer | Technology |

|---|---|

| Language | Python |

| Data processing | pandas, NumPy |

| NLP | Transformers, FinBERT |

| ML | PyTorch, scikit-learn |

| API | FastAPI |

| Validation | Pydantic |

| Visualization | Streamlit, Plotly |

| Data format | JSON, CSV |

| Sources | SEC EDGAR, GDELT GKG |

---

# ◇ Design Principles

**01 · Evidence first**  

Models should operate on traceable source information.

**02 · Financial context over generic sentiment**  

A negative sentence is not automatically a high-risk event.

**03 · Explainable outputs**  

The system should show why a signal was produced.

**04 · Scenario, not prophecy**  

Portfolio stress testing explores hypothetical shocks rather than claiming to predict markets.

**05 · Incremental engineering**  

Each major layer is independently testable and understandable.

---

# ◇ Quick Start

### 1. Clone

```bash

git clone <repository-url>

*cd* AI-Risk-Engine

```

### 2. Create environment

```bash

python -m venv .venv

```

Windows:

```cmd

.venv\Scripts\activate

```

### 3. Install dependencies

```bash

pip install -r requirements.txt

```

### 4. Run the current preprocessing validation

```bash

python -m src.preprocessing.test_processor

```

### 5. Run the current risk engine validation

```bash

python -m src.risk_engine.test_risk_signal

```

The second command runs the current end-to-end risk-signal validation against the processed Apple example.

---

# ◇ Data & Reproducibility

The project is designed around **public and reproducible financial information**. No confidential client information is required.

```text

data/

├── raw/

│   ├── edgar/

│   └── gdelt/

├── processed/

└── demo/

```

Large source archives should not be committed directly to Git if they exceed repository limits. The repository documents the expected data paths and keeps large GDELT archives excluded from version control.

The GDELT implementation uses publicly available GKG bulk data and preserves the distinction between structured news metadata and actual document text.

---

# ◇ Current Risk Signal Schema

The current implemented signal has the following structure:

```json

{

  "entity": "Apple Inc.",

  "sentiment": {

    "label": "neutral",

    "score": 0.0779

  },

  "event": {

    "type": "earnings",

    "confidence": 0.4286,

    "matched_keywords": [

      "earnings",

      "revenue",

      "loss",

      "financial results",

      "net income",

      "eps"

    ]

  },

  "impact": {

    "score": 6.7,

    "base_score": 6.0,

    "sentiment_adjustment": -0.16,

    "evidence_adjustment": 0.86

  },

  "risk_level": "medium"

}

```

The schema will evolve as exposure mapping and portfolio stress testing are implemented.

---

# ◇ Roadmap

```text

[✓] Data ingestion

       ↓

[✓] Source normalization

       ↓

[✓] Financial NLP

       ↓

[✓] Event classification

       ↓

[✓] Impact scoring

       ↓

[✓] Unified risk signal

       ↓

[✓] Explainability

       ↓

[ ] Risk propagation

       ↓

[ ] Portfolio stress testing

       ↓

[ ] API + dashboard

       ↓

[ ] Evaluation

       ↓

[ ] Demo

```

---

# ◇ Next Milestone

The next development phase focuses on **Risk Propagation**:

```text

Risk Signal

     ↓

Entity Exposure

     ↓

Sector Exposure

     ↓

Portfolio Mapping

     ↓

Scenario Shock

     ↓

Portfolio Stress

```

This is where the project moves from **"understanding financial text"** toward **"understanding how financial events can propagate through a portfolio."**

---

<div align="center">

## ◈ From documents to decisions

**AI Risk Engine** is an explainable bridge between

**unstructured financial information** and **structured portfolio risk analysis**.

<br>

**Built for the S&P Global × CRISIL Campus Hackathon 2026**

</div>
