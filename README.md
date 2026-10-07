<div align="center">

# ◈ AI Risk Engine

### Financial Text → Risk Signals → Portfolio Stress

********An explainable AI/NLP risk intelligence engine for financial events********

![Python](https\://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)

![NLP](https\://img.shields.io/badge/NLP-Financial_Text-6C5CE7?style=for-the-badge)

![FastAPI](https\://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

![Status](https\://img.shields.io/badge/Status-In_Development-F59E0B?style=for-the-badge)

********Turn unstructured financial information into structured, explainable risk signals for downstream portfolio stress analysis.********

</div>

---

## ◇ Why this project?

Financial risk rarely arrives as a neat number. It appears as an earnings announcement, regulatory filing, geopolitical development, supply-chain disruption, or macroeconomic signal.

********AI Risk Engine******** transforms these signals into a machine-readable risk layer while preserving the evidence behind each result.

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

- ********What happened?********

- ********Who is exposed?********

- ********How severe is it?********

- ********What could the event mean for a portfolio?********

The project automates the first layer of this workflow and converts unstructured information into structured signals that feed a downstream stress-testing module.

---

# ◇ Data Layer

The current ingestion pipeline uses two complementary public sources.

| Source | Contribution | Current role |
|---|---|---|
| ********SEC EDGAR******** | Company filings and disclosures | Primary source of financial text |
| ********GDELT GKG******** | Global news metadata, financial themes, organizations and tone | External event context |

### SEC EDGAR

The SEC pipeline extracts filing metadata and substantive filing/exhibit text into a normalized representation. Current processed examples include company financial results, revenue, EPS, margins, tariff effects and disclosed risk language.

### GDELT GKG

GDELT's Global Knowledge Graph provides structured context around news coverage, including financial themes, organizations, sources, URLs, article counts and tone.

The implementation deliberately does ********not******** fabricate article body text from GDELT metadata:

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

The engine uses ********ProsusAI/FinBERT******** to classify financial text as positive, neutral or negative.

A normalized sentiment score is calculated as:

```text

-1.0  ◄────────────────►  +1.0

negative                  positive

```

Long documents are split into token-bounded chunks and analyzed across the full document rather than relying on a truncated prefix.

### 02 · Event Classification

The current event classifier is a ********transparent rule-based baseline********. It identifies financially meaningful event categories using domain-specific keyword evidence.

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

Each detected event receives a transparent severity signal on a ********1–10******** scale.

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

\\+ Sentiment Adjustment

\\+ Evidence Adjustment

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

Impact = 6.58 / 10

   ↓

Medium risk

   ↓

Human-readable explanation

```

The event confidence is an evidence ratio from the current rule-based classifier. It is ********not presented as a calibrated probability********.

---

# ◇ Two-Source Risk Intelligence

The current engine combines company-level filing risk from ********SEC EDGAR******** with external context from ********GDELT GKG********.

SEC remains the primary company-risk signal. GDELT contributes a deliberately bounded external-context adjustment using organization mentions, article counts, financial domains, and GDELT tone.

### Validated Apple result

```text

SEC company impact       : 6.70 / 10

GDELT records found      : 6

GDELT average tone       : +0.4904

GDELT tone score         : +0.0490

External adjustment      : +0.02

Combined impact          : 6.72 / 10

Combined risk            : MEDIUM

```

The GDELT tone is ********not treated as equivalent to FinBERT sentiment********. It remains an external structured-context signal.

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

*******> "This article is negative."*******

toward:

*******> "This event affects this entity, through this financial mechanism, with this level of portfolio exposure."*******

Risk propagation is now implemented as the bridge between entity-level risk and portfolio-level exposure.

---

# ◇ Downstream Module: Strategic Event-Driven Stress Testing

The selected downstream module is ********portfolio stress testing********.

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

Sector Propagation

      │

      ▼

Scenario Shock

      │

      ▼

Portfolio Impact

```

The current implementation supports three analyst-defined counterfactual scenarios:

| Scenario | Entity Shock |
|---|---:|
| Mild | -4% |
| Moderate | -8% |
| Severe | -15% |

### Validated Apple portfolio stress test

For the current six-holding demo portfolio, the validated results are:

| Scenario | Direct Impact | Indirect Impact | Portfolio Impact |
|---|---:|---:|---:|
| Mild | -1.00% | -0.42% | ********-1.42%******** |
| Moderate | -2.00% | -0.84% | ********-2.84%******** |
| Severe | -3.75% | -1.58% | ********-5.32%******** |

These are ********counterfactual scenario estimates********, not observed losses or market predictions. The current baseline uses the affected entity's portfolio weight and a transparent same-sector propagation factor of `0.30`.

The future dashboard will allow users to explore counterfactual questions such as:

```text

"What happens to the portfolio

if this event produces a larger shock?"

```

---

# ◇ Explainability

A central design principle is:

_***_> _*********Every important risk signal should have evidence behind it.******

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

│       └── portfolio.csv

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

│   ├── risk_engine/

│   │   ├── __init__.py

│   │   ├── sentiment.py

│   │   ├── event_classifier.py

│   │   ├── impact_scorer.py

│   │   ├── risk_signal.py

│   │   ├── explanation.py

│   │   ├── gdelt_context.py

│   │   ├── combined_risk.py

│   │   └── test_risk_signal.py

│   │

│   └── stress_testing/

│       ├── __init__.py

│       ├── portfolio.py

│       ├── exposure.py

│       ├── propagation.py

│       ├── scenarios.py

│       ├── stress_engine.py

│       ├── risk_stress.py

│       ├── test_portfolio.py

│       ├── test_exposure.py

│       ├── test_propagation.py

│       ├── test_scenarios.py

│       ├── test_stress_engine.py

│       ├── test_validation.py

│       ├── test_risk_stress.py

│       ├── test_gdelt_context.py

│       ├── test_combined_risk.py

│       ├── test_combined_stress.py

│       └── test_end_to_end.py

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
| Risk propagation | ✅ |
| Portfolio stress testing | ✅ |
| SEC + GDELT combined risk | ✅ |
| Risk → stress integration | ✅ |
| FastAPI service | ✅ |
| Interactive dashboard | ✅ |
| Evaluation & sanity checks | ✅ |
| Demo | ⏳ |

**Current milestone:** API, dashboard, two-source risk intelligence and portfolio stress testing are implemented and validated end-to-end. The remaining phase is final demonstration, presentation and submission preparation.

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

********Validated Apple result:********

```text

Sentiment: Neutral (+0.0779)

Event: Earnings

Confidence: 0.4286

Impact: 6.58 / 10

Risk: Medium

```

### Day 4 · Two-Source Risk & Portfolio Stress Testing

- Added a reproducible demo portfolio

- Implemented portfolio validation and loading

- Implemented direct entity exposure mapping

- Implemented same-sector risk propagation

- Added mild, moderate and severe stress scenarios

- Built the portfolio stress engine

- Connected risk signals to portfolio stress testing

- Added GDELT external-context analysis

- Combined SEC company risk with bounded GDELT context

- Added two-source end-to-end validation

- Validated the complete SEC → GDELT → combined risk → stress workflow

********Validated Apple two-source result:********

```text

SEC Impact:          6.70 / 10

GDELT Records:       6

GDELT Tone:          +0.4904

External Adjustment: +0.02

Combined Impact:     6.72 / 10

Combined Risk:       Medium

```

********Validated portfolio stress scenarios:********

| Scenario | Shock | Direct Impact | Indirect Impact | Portfolio Impact |
|---|---:|---:|---:|---:|
| Mild | -4.00% | -1.00% | -0.42% | ********-1.42%******** |
| Moderate | -8.00% | -2.00% | -0.84% | ********-2.84%******** |
| Severe | -15.00% | -3.75% | -1.58% | ********-5.32%******** |

These are ********counterfactual scenario estimates********, not observed losses or market predictions. The current baseline uses the entity portfolio weight and a transparent same-sector propagation factor of `0.30`.

---

---

### Day 5 · Evaluation & Model Sanity Checks

- Added manually labelled sentiment evaluation examples

- Evaluated FinBERT sentiment classification on 15 examples

- Added manually labelled event classification examples

- Evaluated the rule-based event classifier on 20 examples

- Added impact scorer validation for severity ordering, sentiment direction, confidence and score bounds

- Added portfolio stress-engine validation for scenario severity, direct exposure, sector propagation, unrelated-sector isolation and impact reconciliation

- Kept evaluation data inside `data/evaluation/` for reproducibility

- Validated the evaluation suite against the implemented risk and stress-testing components

****Sentiment evaluation result:****

```text

Examples: 15

Correct: 13

Incorrect: 2

Accuracy: 86.67%

Macro F1: 0.8611

```

The two sentiment errors were neutral financial statements that FinBERT interpreted as positive. This is treated as a limitation of the current model rather than hidden or manually corrected.

****Event classification result:****

```text

Examples: 20

Correct: 20

Incorrect: 0

Accuracy: 100.00%

```

This is a small manually labelled sanity-check set, not a claim of generalization performance.

****Impact and stress validation:****

```text

Impact scorer: PASS

Stress engine: PASS

```

The stress engine checks that more severe scenarios produce larger portfolio losses, direct exposure is calculated from portfolio weight, same-sector propagation uses the configured factor, unrelated sectors receive no propagated shock, and direct plus indirect impact reconciles with total portfolio impact.

---

### Day 6 · API, Dashboard & Decision-Facing Delivery

- Added a FastAPI service for programmatic risk analysis
- Added `/risk` for financial text risk analysis
- Added `/combined-risk` for SEC company risk with bounded GDELT external context
- Added `/stress` for portfolio stress scenarios
- Added FastAPI interactive API documentation
- Added an interactive Streamlit dashboard
- Connected the dashboard to the risk engine, GDELT context and portfolio stress engine
- Added SEC filing selection and manual-text analysis
- Added risk overview, evidence, external context, exposure and stress-testing views
- Added decorative dashboard UI for decision-facing presentation
- Validated the dashboard using a real Apple 8-K filing and an additional filing with a different event classification

**Current Day 6 validated workflow:**

```text
SEC Filing / Manual Text
        ↓
Financial Risk Engine
        ↓
Company Risk Signal
        ↓
GDELT External Context
        ↓
Combined Risk
        ↓
Portfolio Exposure
        ↓
Sector Propagation
        ↓
Mild / Moderate / Severe Stress Scenarios
```

**Current validated Apple result:**

```text
SEC company impact: 6.58 / 10
GDELT records: 6
GDELT average tone: +0.4904
GDELT tone score: +0.0490
External adjustment: +0.02
Combined impact: 6.60 / 10
Combined risk: Medium
```

**Validated portfolio stress scenarios:**

| Scenario | Shock | Direct Impact | Indirect Impact | Portfolio Impact |
|---|---:|---:|---:|---:|
| Mild | -4.00% | -1.00% | -0.42% | **-1.42%** |
| Moderate | -8.00% | -2.00% | -0.84% | **-2.84%** |
| Severe | -15.00% | -3.75% | -1.58% | **-5.32%** |

These are counterfactual scenario estimates, not observed losses or market predictions.

# ◇ Technology Stack
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

********01 · Evidence first********

Models should operate on traceable source information.

********02 · Financial context over generic sentiment********

A negative sentence is not automatically a high-risk event.

********03 · Explainable outputs********

The system should show why a signal was produced.

********04 · Scenario, not prophecy********

Portfolio stress testing explores hypothetical shocks rather than claiming to predict markets.

********05 · Incremental engineering********

Each major layer is independently testable and understandable.

---

# ◇ Quick Start

### 1. Clone

```bash

git clone <repository-url>

**cd** AI-Risk-Engine

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

### 6. Run the two-source risk → stress test

```bash

python -m src.stress_testing.test_combined_stress

```

This validates the SEC risk signal, GDELT external context, combined risk signal, and portfolio stress scenarios end-to-end.

---

# ◇ Data & Reproducibility

The project is designed around ********public and reproducible financial information********. No confidential client information is required.

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

The company-level schema is implemented; the two-source and stress-testing layers additionally retain external context, combined impact, and scenario results.

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

[✓] Risk propagation

      ↓

[✓] Portfolio stress testing

      ↓

[✓] Two-source risk integration

      ↓

[✓] Evaluation & sanity checks

      ↓

[✓] API + dashboard

      ↓

[ ] Final demo

```

---

# ◇ Next Milestone

The next development phase focuses on ********API, Dashboard & Decision-Facing Delivery********:

```text

Risk Engine

     ↓

Evaluation & Sanity Checks

     ↓

API / Dashboard

     ↓

Decision-Facing Demo

     ↓

Final Presentation

```

This phase moves the project from a validated engineering pipeline toward an interactive, decision-facing delivery.

<div align="center">

## ◈ From documents to decisions

********AI Risk Engine******** is an explainable bridge between

********unstructured financial information******** and ********structured portfolio risk analysis********.

<br>

********Built for the S&P Global × CRISIL Campus Hackathon 2026********

</div>
