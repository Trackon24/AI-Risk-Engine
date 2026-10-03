<div align="center">

# ◈ AI Risk Engine

### Financial Text → Risk Signals → Portfolio Stress

**An explainable AI/NLP risk intelligence engine for financial events**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Financial_Text-6C5CE7?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Status](https://img.shields.io/badge/Status-In_Development-F59E0B?style=for-the-badge)

> Turn unstructured financial information into structured, explainable risk signals for downstream portfolio stress analysis.

</div>

---

## ◇ Why this project?

Financial risk rarely arrives as a neat number. It appears as an earnings announcement, regulatory filing, geopolitical development, supply-chain disruption, or macroeconomic signal.

**AI Risk Engine** is being built to transform these signals into a machine-readable risk layer while preserving the evidence behind each result.

```text
┌─────────────────────┐
│  FINANCIAL SOURCES  │
│  SEC EDGAR          │
│  GDELT GKG          │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│   INGESTION +       │
│   NORMALIZATION     │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│     AI RISK ENGINE  │
│  Sentiment          │
│  Event Classifier   │
│  Impact Scoring     │
│  Entity Detection   │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ RISK INTELLIGENCE   │
│ Evidence + Exposure│
│ Risk Propagation    │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ PORTFOLIO STRESS    │
│ TESTING             │
└─────────────────────┘
```

## ◇ Core problem

Traditional financial analysis can require analysts to manually read large volumes of text before answering:

- **What happened?**
- **Who is exposed?**
- **How severe is it?**
- **What could the event mean for a portfolio?**

The project automates the first layer of this workflow and converts unstructured information into structured signals that can feed a downstream stress-testing module.

---

# ◇ Data Layer

The current ingestion pipeline uses two complementary public sources.

| Source | Contribution | Current role |
|---|---|---|
| **SEC EDGAR** | Company filings and disclosures | Primary source of financial text |
| **GDELT GKG** | Global news metadata, financial themes, organizations and tone | External event context |

### SEC EDGAR

The SEC pipeline extracts filing metadata and substantive filing/exhibit text into a normalized representation. The current processed examples include company financial results, revenue, EPS, margins, tariff effects and disclosed risk language.

### GDELT GKG

GDELT's Global Knowledge Graph provides structured context around news coverage, including financial themes, organizations, sources, URLs, article counts and tone.

The implementation deliberately does **not** fabricate article body text from GDELT metadata:

```text
SEC   → text_available = True
GDELT → text_available = False
```

This distinction is preserved in the unified representation.

---

# ◇ Unified Document Architecture

Both sources are normalized into a common `FinancialDocument` structure:

```python
FinancialDocument(
    source=...,
    timestamp=...,
    title=...,
    text=...,
    url=...,
    entity=...,
    document_type=...,
    text_available=...,
    metadata={...}
)
```

Source-specific information stays inside `metadata`, so downstream components can consume one consistent interface without losing useful source information.

```text
             ┌───────────────┐
             │   SEC EDGAR   │
             └───────┬───────┘
                     ▼
              ┌──────────────┐
              │ FinancialDoc │
              └──────────────┘
                     ▲
                     │
             ┌───────┴───────┐
             │   GDELT GKG   │
             └───────────────┘
```

---

# ◇ AI Risk Engine

The planned NLP layer converts financial text and event context into structured risk signals.

### 01 · Sentiment

Financial-language modeling will produce a normalized sentiment score:

```text
-1.0  ◄────────────────►  +1.0
negative                  positive
```

### 02 · Event Classification

The engine will classify financially meaningful events such as:

```text
Geopolitical     Macroeconomic
Credit Event     M&A
Regulatory       Earnings
Product Launch   Supply Chain
Management      Other
```

The final taxonomy will be constrained by the available data and evaluation evidence rather than arbitrary labels.

### 03 · Impact Scoring

Each detected event will receive a severity/impact signal on a `1–10` scale. The scoring layer is intended to combine model output with transparent financial evidence rather than treating generic sentiment as equivalent to financial impact.

### 04 · Entity & Exposure

The engine identifies the relevant company or organization and maps the event toward financial exposure.

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

> "This article is negative."

toward:

> "This event affects this entity, through this financial mechanism, with this level of portfolio exposure."

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

> **Every important risk signal should have evidence behind it.**

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
│   ├── raw/
│   │   ├── gdelt/
│   │   └── edgar/
│   ├── processed/
│   └── demo/
│
├── src/
│   ├── ingestion/
│   │   ├── edgar_loader.py
│   │   ├── gdelt_gkg_loader.py
│   │   ├── schema.py
│   │   └── test_edgar.py
│   │
│   ├── preprocessing/
│   │   ├── cleaner.py
│   │   ├── processor.py
│   │   ├── test_cleaner.py
│   │   └── test_processor.py
│   │
│   └── pipeline/
│       ├── __init__.py
│       └── unified.py
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
| Financial sentiment model | ⏳ |
| Event classifier | ⏳ |
| Impact scoring | ⏳ |
| Risk propagation | ⏳ |
| Portfolio stress testing | ⏳ |
| FastAPI service | ⏳ |
| Interactive dashboard | ⏳ |
| Evaluation & benchmarking | ⏳ |

> **Current milestone:** the repository has a working ingestion, cleaning and normalization foundation. The AI risk and downstream portfolio layers are being built incrementally.

---

# ◇ Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Data processing | pandas, NumPy |
| NLP | Transformers / financial-language models |
| ML | scikit-learn / PyTorch |
| API | FastAPI |
| Validation | Pydantic |
| Visualization | Streamlit / Plotly |
| Data format | JSON / CSV |
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
cd AI-Risk-Engine
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

### 4. Run the current processing pipeline

```bash
python -m src.preprocessing.test_processor
```

The application entry point will be added as the risk engine and downstream modules are completed.

---

# ◇ Data & Reproducibility

The project is designed around **public and reproducible financial information**. No confidential client information is required.

```text
data/
├── raw/
├── processed/
└── demo/
```

Large source archives should not be committed directly to Git if they exceed repository limits. The repository will document how to obtain or reproduce them where required.

---

# ◇ Planned API

The target API will expose structured risk signals similar to:

```json
{
  "source": "SEC_EDGAR",
  "timestamp": "2026-07-30",
  "entity": "Apple Inc.",
  "sentiment_score": -0.32,
  "event_class": "Earnings",
  "impact_score": 7,
  "risk_level": "HIGH"
}
```

The final schema will be frozen after the NLP and impact-scoring layers are implemented.

---

# ◇ Roadmap

```text
[✓] Data ingestion
       ↓
[✓] Source normalization
       ↓
[ ] Financial NLP
       ↓
[ ] Event classification
       ↓
[ ] Impact scoring
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

<div align="center">

## ◈ From documents to decisions

**AI Risk Engine** is an explainable bridge between
**unstructured financial information** and **structured portfolio risk analysis**.

<br/>

*Built for the S&P Global × CRISIL Campus Hackathon 2026*

</div>
