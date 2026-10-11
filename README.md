<div align="center">

# ◈ AI Risk Engine

### Financial Text → Risk Signals → Portfolio Stress

**An explainable AI/NLP risk intelligence engine for financial events**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Financial_Text-6C5CE7?style=for-the-badge)
![API](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Prototype_Complete-2E8B57?style=for-the-badge)

Turn unstructured financial information into structured, explainable risk signals for downstream portfolio stress analysis.

**Chinmayi Upadhyay · chinmayi.mitmpl2024@learner.manipal.edu · Manipal Institute of Technology, Manipal**  
**S&P Global × CRISIL Campus Hackathon 2026**

</div>

---

## 🎥 Demo and submission links

- **Demo video:** [Watch the AI Risk Engine demo](https://youtu.be/g3wXb1_eD0M)
- **Slide deck:** [View the presentation PDF](docs/presentation.pdf)
- **Source code:** [GitHub repository](https://github.com/Trackon24/AI-Risk-Engine)

### Demo chapters

| Timestamp | Topic |
|---|---|
| [00:00](https://youtu.be/g3wXb1_eD0M?t=0) | Introduction and problem statement |
| [01:22](https://youtu.be/g3wXb1_eD0M?t=82) | Live risk analysis: Apple Inc. |
| [02:34](https://youtu.be/g3wXb1_eD0M?t=154) | External market context with GDELT |
| [03:37](https://youtu.be/g3wXb1_eD0M?t=217) | Portfolio stress testing |
| [05:17](https://youtu.be/g3wXb1_eD0M?t=317) | System architecture and implementation |
| [06:07](https://youtu.be/g3wXb1_eD0M?t=367) | Results, limitations and conclusion |

---

## 1. Project Overview / Problem Statement & Approach

Financial risk rarely arrives as a neat number. It appears in earnings announcements, regulatory filings, geopolitical developments, supply-chain disruptions and macroeconomic signals. Analysts must interpret unstructured information, determine which events may matter to a company, and reason about how that risk could affect a portfolio.

**AI Risk Engine** transforms public financial disclosures into structured, explainable risk signals and connects company-level risk to portfolio exposure and hypothetical stress scenarios. SEC EDGAR provides the primary company-disclosure evidence. FinBERT estimates financial sentiment, a transparent rule-based classifier identifies potential event categories, and an impact scorer produces a bounded 1–10 score with supporting evidence. GDELT GKG contributes supplementary structured news metadata when a local archive is available. The system then maps risk to a sample portfolio and compares mild, moderate and severe scenario shocks.

The prototype is designed to support review and scenario analysis, not to predict market movements or provide financial advice. Its outputs are accompanied by explicit assumptions and limitations.

### Day-by-day implementation log

The day labels describe the development sequence; they are not intended as independently timestamped activity records.

**Day 1 · Project foundation and ingestion**
- Set up the repository and Python project structure.
- Implemented ingestion of public company filings through SEC EDGAR.
- Extracted filing metadata and available 8-K filing/exhibit text.
- Added bulk GDELT GKG ingestion for supplementary news metadata.
- Created a shared `FinancialDocument` schema and unified document-saving flow.

**Day 2 · Cleaning and data validation**
- Implemented text cleaning and preprocessing for filing content.
- Tested SEC extraction and GDELT financial-theme filtering.
- Preserved source metadata such as organizations, themes, URLs, domains and tone.
- Added raw and processed data paths and checked records against the shared schema.
- Investigated GDELT rate limits and used bulk archives rather than depending on repeated live queries.

**Day 3 · NLP and company-level risk signals**
- Integrated ProsusAI/FinBERT for financial sentiment analysis.
- Added chunking for long filing documents.
- Implemented rule-based financial event classification with keyword evidence.
- Added a bounded 1–10 impact score and human-readable explanations.
- Validated the risk pipeline against an Apple Inc. 8-K example.

**Day 4 · External context and portfolio stress testing**
- Added the sample portfolio and portfolio validation/loading.
- Implemented direct entity exposure mapping and same-sector risk propagation.
- Added mild, moderate and severe hypothetical shock scenarios.
- Connected company-level risk to portfolio stress analysis.
- Integrated the bounded GDELT tone adjustment into combined risk scoring.
- Tested the SEC-to-GDELT-to-combined-risk-to-stress workflow.

**Day 5 · API integration**
- Exposed the analysis workflow through FastAPI.
- Implemented the root/health response and the `/risk`, `/combined-risk` and `/stress` endpoints.
- Added request/response validation and API documentation through FastAPI’s `/docs` page.
- Checked endpoint behavior, including the case where a local GDELT archive is unavailable.

**Day 6 · Interactive dashboard**
- Built the Streamlit interface for running and inspecting risk analysis.
- Connected dashboard views to company-level risk, available external context and portfolio stress scenarios.
- Added visual presentation of risk scores and scenario impacts.
- Prepared the demo workflow around an Apple Inc. filing and the sample portfolio.

**Day 7 · Evaluation, testing and presentation**
- Ran the project test suite; the recorded repository check passed with `3 passed`.
- Performed small manually labelled sanity checks for sentiment and event classification.
- Documented evaluation limitations and the difference between unavailable GDELT data and zero news risk.
- Prepared the presentation PDF and recorded demo, with chapter timestamps linked above.
- Reviewed fresh-clone behavior and documented the optional local GDELT archive requirement.

---

## 2. Architecture & Tech Stack

### Architecture

```text
             PUBLIC FINANCIAL SOURCES
                 ┌─────────┴─────────┐
                 │                   │
             SEC EDGAR            GDELT GKG
             filing text       news metadata
                 │                   │
                 └─────────┬─────────┘
                           ▼
                INGESTION + NORMALIZATION
                           │
                           ▼
                 FinancialDocument schema
                           │
                           ▼
                      AI RISK ENGINE
                 ┌─────────┼─────────┐
                 ▼         ▼         ▼
              FinBERT    Event      Impact
             sentiment classifier  scoring
                 └─────────┼─────────┘
                           ▼
                  Unified risk signal
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
        Bounded GDELT context   Explainable evidence
                └──────────┬──────────┘
                           ▼
                   Portfolio exposure
                           │
                           ▼
                    Sector propagation
                           │
                           ▼
                Mild / Moderate / Severe
                    stress scenarios
```

If the repository contains `docs/architecture.png`, it can be embedded here as an image. The architecture above is retained as a readable text diagram so the README remains useful even if the image file is not present.

### Technology stack

| Layer | Technology |
|---|---|
| Language | Python |
| Data processing | pandas, NumPy |
| Financial NLP | Hugging Face Transformers, ProsusAI/FinBERT |
| ML utilities | PyTorch, scikit-learn |
| API | FastAPI, Pydantic, Uvicorn |
| Dashboard | Streamlit |
| Data formats | JSON, CSV |
| Public data sources | SEC EDGAR, GDELT GKG |

---

## 3. Dataset Used

### SEC EDGAR: primary disclosure evidence

The ingestion pipeline works with public company filings, including 8-K reports and available filing/exhibit text. Extracted text is cleaned and passed to the NLP pipeline. The Apple Inc. filing used in the demonstration is an example input for the end-to-end workflow.

### GDELT GKG: supplementary external context

The GDELT Global Knowledge Graph contributes structured metadata such as organization mentions, themes, source information, URLs, article counts and tone. The GKG records used here do **not** provide full article body text, so the pipeline does not invent or infer missing article text.

### Sample portfolio

The demo portfolio is stored in `data/demo/portfolio.csv`. It is a sample portfolio for demonstrating exposure mapping and hypothetical stress scenarios, not a representation of real client holdings.

### Data assumptions and availability

- SEC EDGAR provides the primary company-disclosure signal.
- GDELT provides supplementary external context, not a replacement for filing evidence.
- GDELT context is applied as a bounded adjustment to the company impact score.
- Large GDELT bulk archives are excluded from Git to keep the repository manageable.
- The GDELT archive is not included in this repository. Without a locally available archive, the GDELT analyzer returns no records and the combined-risk endpoint uses a zero external adjustment. This means external context is **unavailable**, not that the company has no external news risk.
- To reproduce an archive-backed GDELT result, obtain the relevant public GDELT GKG bulk archive and place it at the path expected by the loader.

---

## 4. Quickstart & Installation

### Requirements

- Python 3.10 or a compatible Python version for the installed dependencies
- Git
- Internet access on the first run if the FinBERT model needs to be downloaded

### 1. Clone the repository

```bash
git clone https://github.com/Trackon24/AI-Risk-Engine.git
cd AI-Risk-Engine
```

If the GitHub repository has been renamed, use the repository’s current clone URL in the command above.

### 2. Create and activate a virtual environment

**Windows CMD:**

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The first FinBERT inference may take longer while the model is downloaded and initialized.

### 4. Run the API

```cmd
python -m uvicorn src.api.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to inspect and test the API endpoints.

### 5. Run the dashboard

Open a **second CMD window**, navigate to the cloned repository, activate the same environment, and run:

```cmd
.venv\Scripts\activate
python -m streamlit run dashboard/app.py
```

Streamlit prints the local dashboard URL in the terminal, typically `http://localhost:8501`.

### 6. Run tests

From the repository root, with the environment activated:

```cmd
python -m pytest -q
```

Some GDELT-dependent results require the optional local GDELT bulk archive described above. The code can handle the archive being absent, but the external-context panel will have no records in that case.

---

## 5. Key Results & Domain Impact

### Illustrative Apple Inc. dashboard run

| Signal | Displayed result |
|---|---:|
| SEC-derived company impact | 6.13 / 10 |
| GDELT records matched | 6 |
| Average GDELT tone | +0.05 |
| External-context adjustment | Approximately +0.02 |
| Combined impact | 6.15 / 10 |
| Risk band | Medium |

These figures describe the illustrated dashboard run and should not be assumed to reproduce on a fresh clone without the same local GDELT archive and inputs.

### Portfolio stress testing

The downstream module maps an entity-level risk signal to the sample portfolio, calculates direct exposure, applies a configurable same-sector propagation factor, and compares counterfactual shock scenarios.

| Scenario | Entity shock | Direct impact | Indirect impact | Portfolio impact |
|---|---:|---:|---:|---:|
| Mild | -4% | -1.00% | -0.42% | -1.42% |
| Moderate | -8% | -2.00% | -0.84% | -2.84% |
| Severe | -15% | -3.75% | -1.58% | -5.32% |

The baseline uses a same-sector propagation factor of `0.30`. These are **hypothetical scenario outputs under explicit assumptions**, not realized losses, causal estimates or market forecasts. The propagation factors and shocks are transparent prototype assumptions, not empirically calibrated relationships.

### Validation checks

| Check | Result | Interpretation |
|---|---|---|
| FinBERT sentiment evaluation | 13/15 correct, 86.67% accuracy; macro F1 0.8611 | Small manually labelled check, not a broad benchmark |
| Rule-based event classification | 20/20 correct on the checked examples | Small sanity check, not evidence of generalization |
| Impact scorer and stress-engine checks | Pass | Checks score bounds, scenario ordering and exposure reconciliation |
| Repository test suite | 3 passed in the recorded check | Test result from the recorded project state |

These checks help catch implementation errors, but the evaluation sets are small and do not establish production-grade predictive performance.

### Domain impact

The prototype demonstrates a traceable path from public financial disclosures to structured risk signals and portfolio-level scenario analysis. It aims to make the reasoning inspectable by exposing event evidence, sentiment interpretation, impact components and explicit stress assumptions instead of presenting a score without context.

---

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Service health/root response |
| `POST` | `/risk` | Analyze an entity and financial text |
| `POST` | `/combined-risk` | Combine a risk signal with available GDELT context |
| `POST` | `/stress` | Run a portfolio stress scenario |

Interactive API documentation is available at `/docs` after the API starts.

---

## Limitations and responsible interpretation

- The event classifier is rule-based and can miss events or trigger on ambiguous wording.
- The sentiment and event sanity-check datasets are small and manually labelled.
- The event confidence score is an evidence ratio, not a calibrated probability.
- GDELT provides metadata in this implementation, not full article text. External context is unavailable if the local bulk archive is absent.
- The sample portfolio, shock sizes and sector propagation factor are assumptions for counterfactual analysis.
- Stress outputs are not market predictions, financial advice or realized-loss estimates.
- The prototype has not been established as a production risk system; broader datasets, out-of-sample evaluation and calibration would be required.

---

## Repository structure

```text
AI-Risk-Engine/
├── dashboard/
│   └── app.py
├── data/
│   ├── demo/
│   │   └── portfolio.csv
│   ├── evaluation/
│   ├── processed/
│   └── raw/
│       ├── edgar/
│       └── gdelt/          # bulk archives excluded from Git
├── docs/
│   ├── architecture.png    # include if this file exists in the repository
│   └── presentation.pdf
├── src/
│   ├── api/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── risk_engine/
│   └── stress_testing/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ◇ Design principles

1. **Evidence first:** Preserve the source and evidence behind a signal.
2. **Financial context over generic sentiment:** Negative language is not automatically a high-impact financial event.
3. **Explainable outputs:** Show why a signal was generated.
4. **Scenario, not prophecy:** Explore hypothetical shocks without claiming to predict markets.
5. **Reproducibility:** Use public data and document assumptions and unavailable inputs.

---

<div align="center">

## ◈ From documents to decisions

**AI Risk Engine** connects unstructured financial disclosures to explainable risk signals and hypothetical portfolio stress analysis.

Built for the **S&P Global × CRISIL Campus Hackathon 2026**.

</div>
