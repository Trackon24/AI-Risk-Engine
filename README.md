<div align="center">

# ◈ AI Risk Engine

### Financial Text → Risk Signals → Portfolio Stress

**An explainable AI/NLP risk intelligence engine for financial events**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Financial_Text-6C5CE7?style=for-the-badge)
![API](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Prototype_Complete-2E8B57?style=for-the-badge)

Turn unstructured financial information into structured, explainable risk signals for downstream portfolio stress analysis.

**Chinmayi Upadhyay · Manipal Institute of Technology, Manipal**  
**S&P Global × CRISIL Campus Hackathon 2026**

</div>

---

## 🎥 Demo and presentation

- **Video demonstration:** [Watch the AI Risk Engine demo](https://youtu.be/g3wXb1_eD0M)
- **Presentation:** [View the presentation PDF](docs/presentation.pdf)
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

## ◇ Why this project?

Financial risk rarely arrives as a neat number. It appears in earnings announcements, regulatory filings, geopolitical developments, supply-chain disruptions and macroeconomic signals.

**AI Risk Engine** transforms public financial disclosures into structured risk signals while preserving evidence behind each result. It then connects company-level risk to portfolio exposure and hypothetical stress scenarios.

The system is designed to help answer four questions:

- **What happened?** Identify a potential financial event from disclosure text.
- **How significant is it?** Combine event severity, financial sentiment and evidence strength into a bounded impact score.
- **What external context is available?** Add a deliberately bounded signal from structured GDELT metadata when the data archive is available.
- **Who could be exposed?** Map the company-level signal to portfolio holdings and compare hypothetical stress scenarios.

## ◇ Day-by-day implementation log

This log summarizes the project’s implementation milestones, from data ingestion to the tested demo. The day labels describe the development sequence; they are not intended as independently timestamped activity records.

### Day 1 · Project foundation and ingestion

- Set up the repository and Python project structure.
- Implemented ingestion of public company filings through SEC EDGAR.
- Extracted filing metadata and available 8-K filing/exhibit text.
- Added bulk GDELT GKG ingestion for supplementary news metadata.
- Created a shared `FinancialDocument` schema and unified document-saving flow.

**Milestone:** Public-source records can enter a common ingestion pipeline.

### Day 2 · Cleaning and data validation

- Implemented text cleaning and preprocessing for filing content.
- Tested SEC extraction and GDELT financial-theme filtering.
- Preserved source metadata such as organizations, themes, URLs, domains and tone.
- Added raw and processed data paths and checked records against the shared schema.
- Investigated GDELT rate limits and used bulk archives rather than depending on repeated live queries.

**Milestone:** The two sources have distinct, documented roles and a consistent processing path.

### Day 3 · NLP and company-level risk signals

- Integrated ProsusAI/FinBERT for financial sentiment analysis.
- Added chunking for long filing documents.
- Implemented rule-based financial event classification with keyword evidence.
- Added a bounded 1–10 impact score and human-readable explanations.
- Validated the risk pipeline against an Apple Inc. 8-K example.

**Milestone:** Filing text becomes a structured, inspectable company-level risk signal.

### Day 4 · External context and portfolio stress testing

- Added the sample portfolio and portfolio validation/loading.
- Implemented direct entity exposure mapping and same-sector risk propagation.
- Added mild, moderate and severe hypothetical shock scenarios.
- Connected company-level risk to portfolio stress analysis.
- Integrated the bounded GDELT tone adjustment into combined risk scoring.
- Tested the SEC-to-GDELT-to-combined-risk-to-stress workflow.

**Milestone:** Company-level signals can be connected to portfolio exposures and counterfactual scenarios.

### Day 5 · API integration

- Exposed the analysis workflow through FastAPI.
- Implemented the root/health response and the `/risk`, `/combined-risk` and `/stress` endpoints.
- Added request/response validation and API documentation through FastAPI’s `/docs` page.
- Checked endpoint behavior, including the case where a local GDELT archive is unavailable.

**Milestone:** The risk engine can be exercised through documented HTTP endpoints.

### Day 6 · Interactive dashboard

- Built the Streamlit interface for running and inspecting risk analysis.
- Connected dashboard views to company-level risk, available external context and portfolio stress scenarios.
- Added visual presentation of risk scores and scenario impacts.
- Prepared the demo workflow around an Apple Inc. filing and the sample portfolio.

**Milestone:** The pipeline can be demonstrated through a user-facing interface as well as the API.

### Day 7 · Evaluation, testing and presentation

- Ran the project test suite; the recorded repository check passed with `3 passed`.
- Performed small manually labelled sanity checks for sentiment and event classification.
- Documented evaluation limitations, assumptions and the distinction between unavailable GDELT data and zero news risk.
- Prepared the presentation PDF and recorded demo, with chapter timestamps linked above.
- Reviewed fresh-clone behavior and documented the optional local GDELT archive requirement.

**Milestone:** The prototype has a testable setup, a demo path and explicit limitations for reviewers.

> **Reproducibility note:** Evaluation figures and displayed risk scores are prototype results, not claims of general predictive accuracy. Exact combined-risk values can vary with the filing text, local GDELT archive and available records. The stress scenarios are hypothetical assumptions, not forecasts.

---

## ◇ Architecture

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
             sentiment  classifier  scoring
                 └─────────┼─────────┘
                           ▼
                    Unified risk signal
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
        Bounded GDELT context    Explainable evidence
               └───────────┬───────────┘
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

## ◇ Data sources and assumptions

### SEC EDGAR: primary disclosure evidence

The ingestion pipeline works with public company filings, including 8-K reports and available filing/exhibit text. The extracted text is cleaned and passed to the NLP pipeline.

### GDELT GKG: supplementary external context

The GDELT Global Knowledge Graph contributes structured metadata such as organization mentions, themes, source information, URLs, article counts and tone. The GKG records used here do **not** provide full article body text, so the pipeline does not invent or infer missing article text.

- SEC EDGAR provides the primary company-disclosure signal.
- GDELT provides supplementary external context, not a replacement for the filing evidence.
- GDELT context is applied as a bounded adjustment to the company impact score.
- Large GDELT bulk archives are excluded from Git to keep the repository manageable.

**Fresh-clone note:** The GDELT archive is not included in this repository. Without a locally available archive, the GDELT analyzer returns no records and the combined-risk endpoint uses a zero external adjustment. This means external context is **unavailable**, not that the company has no external news risk. To reproduce an archive-backed GDELT result, obtain the relevant public GDELT GKG bulk archive and place it at the path expected by the loader.

## ◇ Risk engine

### 1. Financial sentiment

The pipeline uses **ProsusAI/FinBERT** to estimate positive, neutral and negative financial sentiment. Long documents are split into model-compatible chunks, and the outputs are aggregated.

The sentiment score is bounded to `[-1, 1]`:

- Values closer to `+1` indicate positive sentiment.
- Values closer to `0` indicate neutral sentiment.
- Values closer to `-1` indicate negative sentiment.

Sentiment alone is not treated as financial impact.

### 2. Event classification

The current classifier is a transparent, rule-based baseline that uses domain-specific keyword evidence. Categories include:

- Earnings
- M&A
- Credit event
- Regulatory
- Geopolitical
- Macroeconomic
- Product/business
- Litigation
- Unknown

The classifier records matched keywords and an evidence-ratio confidence score. This confidence is **not a calibrated probability**.

### 3. Impact scoring

The impact scorer combines event-type severity, a sentiment adjustment and an evidence-strength adjustment. The final company impact score is clipped to the range `1–10`.

Risk bands are:

| Score | Risk band |
|---|---|
| 1.00–4.99 | Low |
| 5.00–7.99 | Medium |
| 8.00–10.00 | High |

### 4. Combined risk

When GDELT records are available, the engine combines the company impact score with a deliberately bounded external-context adjustment. The company filing remains the primary signal; GDELT tone is not treated as equivalent to FinBERT sentiment.

### 5. Explainability

Risk signals expose the detected event, matched keywords, sentiment interpretation, impact score and score components so a reviewer can inspect why the system produced a result.

## ◇ Portfolio stress testing

The downstream module maps an entity-level risk signal to the sample portfolio, calculates direct exposure, applies a configurable same-sector propagation factor, and compares counterfactual shock scenarios.

The demo portfolio is in `data/demo/portfolio.csv`. It is a sample portfolio, not a representation of real client holdings.

| Scenario | Entity shock |
|---|---:|
| Mild | -4% |
| Moderate | -8% |
| Severe | -15% |

The baseline uses a same-sector propagation factor of `0.30`. Holdings in unrelated sectors do not receive this same-sector propagated shock.

### Illustrative stress results

| Scenario | Direct impact | Indirect impact | Portfolio impact |
|---|---:|---:|---:|
| Mild | -1.00% | -0.42% | -1.42% |
| Moderate | -2.00% | -0.84% | -2.84% |
| Severe | -3.75% | -1.58% | -5.32% |

These are **hypothetical scenario outputs under explicit assumptions**, not realized losses, causal estimates or market forecasts. The propagation factors and shocks are transparent prototype assumptions, not empirically calibrated relationships.

## ◇ Demo results and validation

The presentation/dashboard illustrates an Apple Inc. prototype run. The dashboard screenshot reports:

| Signal | Displayed result |
|---|---:|
| SEC-derived company impact | 6.13 / 10 |
| GDELT records matched | 6 |
| Average GDELT tone | +0.05 |
| External-context adjustment | Approximately +0.02 |
| Combined impact | 6.15 / 10 |
| Risk band | Medium |

These figures describe the illustrated run and should not be assumed to reproduce on a fresh clone without the same local GDELT archive and inputs.

The repository also includes small manually labelled sanity-check sets:

| Check | Result | Interpretation |
|---|---:|---|
| FinBERT sentiment evaluation | 13/15 correct, 86.67% accuracy; macro F1 0.8611 | Small manually labelled check, not a broad benchmark |
| Rule-based event classification | 20/20 correct on the checked examples | Small sanity check, not evidence of generalization |
| Impact scorer and stress-engine checks | Pass | Checks score bounds, scenario ordering and exposure reconciliation |

These checks help catch implementation errors, but the evaluation sets are small and do not establish production-grade predictive performance.

## ◇ API endpoints

The FastAPI service exposes:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Service health/root response |
| `POST` | `/risk` | Analyze an entity and financial text |
| `POST` | `/combined-risk` | Combine a risk signal with available GDELT context |
| `POST` | `/stress` | Run a portfolio stress scenario |

Interactive API documentation is available at `/docs` after the API starts.

## ◇ Quick start

### Requirements

- Python 3.10 or a compatible Python version for the installed dependencies
- Git
- Internet access on the first run if the FinBERT model needs to be downloaded

### 1. Clone the repository

```bash
git clone https://github.com/Trackon24/AI-Risk-Engine.git
cd AI-Risk-Engine
```

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

In the activated environment, run:

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

Streamlit will print the local dashboard URL in the terminal, typically `http://localhost:8501`.

### 6. Run tests

From the repository root, with the environment activated:

```cmd
python -m pytest -q
```

Some GDELT-dependent results require the optional local GDELT bulk archive described above. The code can handle the archive being absent, but the external-context panel will have no records in that case.

## ◇ Repository structure

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

## ◇ Limitations and responsible interpretation

- The event classifier is rule-based and can miss events or trigger on ambiguous wording.
- The sentiment and event sanity-check datasets are small and manually labelled.
- The event confidence score is an evidence ratio, not a calibrated probability.
- GDELT provides metadata in this implementation, not full article text. External context is unavailable if the local bulk archive is absent.
- The sample portfolio, shock sizes and sector propagation factor are assumptions for counterfactual analysis.
- The stress outputs are not market predictions, financial advice or realized-loss estimates.
- The prototype has not been established as a production risk system; broader datasets, out-of-sample evaluation and calibration would be required.

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
