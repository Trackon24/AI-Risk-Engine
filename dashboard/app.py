import json
from pathlib import Path
import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "edgar_documents.json"
)

st.set_page_config(
    page_title="AI Risk Engine",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 8% 8%, rgba(70,125,255,0.12), transparent 28%), radial-gradient(circle at 92% 18%, rgba(0,214,170,0.08), transparent 25%), radial-gradient(circle at 50% 100%, rgba(120,70,255,0.07), transparent 30%), #080c12;
    }
    .stApp::before {
        content: ""; position: fixed; inset: 0; pointer-events: none; opacity: 0.22;
        background-image: linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
        background-size: 42px 42px; mask-image: linear-gradient(to bottom, black, transparent 82%);
    }
    .block-container { max-width: 1500px; padding-top: 1.5rem; padding-bottom: 4rem; }
    h1, h2, h3 { letter-spacing: -0.03em; }
    .hero {
        position: relative; overflow: hidden; padding: 2rem 2.2rem; border: 1px solid rgba(105,130,170,0.22); border-radius: 24px;
        background: linear-gradient(135deg, rgba(18,27,40,0.96), rgba(10,16,25,0.96));
        box-shadow: 0 24px 70px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,255,255,0.04); margin-bottom: 1.8rem;
    }
    .hero::after {
        content: ""; position: absolute; width: 260px; height: 260px; right: -80px; top: -120px; border-radius: 50%; background: rgba(76,132,255,0.16); filter: blur(20px);
    }
    .hero-top { display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.75rem; color: #7fa7ff; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.16em; text-transform: uppercase; }
    .hero-dot { width: 8px; height: 8px; border-radius: 50%; background: #43e0aa; box-shadow: 0 0 16px rgba(67,224,170,0.8); }
    .hero-title { font-size: 2.55rem; font-weight: 800; line-height: 1.05; margin-bottom: 0.5rem; }
    .hero-subtitle { color: #8d9bad; font-size: 1rem; }
    .hero-chips { display: flex; flex-wrap: wrap; gap: 0.55rem; margin-top: 1.35rem; }
    .hero-chip { padding: 0.42rem 0.72rem; border: 1px solid rgba(125,150,190,0.18); border-radius: 999px; background: rgba(255,255,255,0.035); color: #aeb9c8; font-size: 0.76rem; }
    .section-label { display: flex; align-items: center; gap: 0.65rem; color: #7895bb; font-size: 0.72rem; font-weight: 800; letter-spacing: 0.16em; text-transform: uppercase; margin: 0.3rem 0 0.75rem; }
    .section-label::before { content: ""; width: 24px; height: 2px; border-radius: 2px; background: linear-gradient(90deg,#5d8cff,#43e0aa); box-shadow: 0 0 12px rgba(93,140,255,0.35); }
    .risk-card {
        position: relative; overflow: hidden; background: linear-gradient(145deg,rgba(17,25,36,0.96),rgba(12,18,27,0.96));
        border: 1px solid rgba(105,130,170,0.18); border-radius: 18px; padding: 1.15rem 1.25rem; min-height: 112px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.16), inset 0 1px 0 rgba(255,255,255,0.025); transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .risk-card:hover { transform: translateY(-2px); border-color: rgba(93,140,255,0.35); }
    .risk-card::after { content: ""; position: absolute; width: 90px; height: 90px; right: -45px; bottom: -55px; border-radius: 50%; background: rgba(93,140,255,0.08); filter: blur(6px); }
    .risk-card-title { color: #8191a7; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.55rem; }
    .risk-card-value { font-size: 1.38rem; font-weight: 750; }
    .status-pill { display: inline-block; margin-top: 0.45rem; padding: 0.3rem 0.7rem; border-radius: 999px; font-size: 0.72rem; font-weight: 750; background: rgba(42,190,116,0.16); color: #55d68a; border: 1px solid rgba(85,214,138,0.16); }
    .stress-card { position: relative; overflow: hidden; padding: 1.2rem 1.25rem; border-radius: 18px; background: linear-gradient(145deg,rgba(17,25,36,0.98),rgba(11,17,25,0.98)); border: 1px solid rgba(105,130,170,0.18); box-shadow: 0 14px 35px rgba(0,0,0,0.18); }
    .stress-card.mild { border-top: 2px solid #43e0aa; }
    .stress-card.moderate { border-top: 2px solid #e9b84f; }
    .stress-card.severe { border-top: 2px solid #ff5c67; }
    .stress-name { color: #9aa8ba; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 750; }
    .stress-value { margin-top: 0.35rem; font-size: 2rem; font-weight: 800; }
    .stress-shock { margin-top: 0.35rem; color: #68778b; font-size: 0.8rem; }
    .stButton > button { border-radius: 12px; font-weight: 750; min-height: 2.9rem; box-shadow: 0 10px 24px rgba(255,75,82,0.16); }
    .stSelectbox > div > div, .stTextInput > div > div, .stTextArea > div > div { border-radius: 12px; }
    div[data-testid="stMetric"] { background: linear-gradient(145deg,rgba(17,25,36,0.96),rgba(12,18,27,0.96)); border: 1px solid rgba(105,130,170,0.18); border-radius: 18px; padding: 1rem 1.1rem; box-shadow: 0 12px 30px rgba(0,0,0,0.14); }
    div[data-testid="stMetricLabel"] { color: #8191a7; }
    div[data-testid="stMetricValue"] { font-weight: 750; }
    div[data-testid="stDataFrame"] { border: 1px solid rgba(105,130,170,0.2); border-radius: 16px; overflow: hidden; box-shadow: 0 12px 30px rgba(0,0,0,0.15); }
    hr { border-color: rgba(105,130,170,0.16); }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero">
        <div class="hero-top"><span class="hero-dot"></span> Risk Intelligence System</div>
        <div class="hero-title">AI Risk Engine</div>
        <div class="hero-subtitle">Financial Risk Intelligence · External Market Context · Portfolio Stress Testing</div>
        <div class="hero-chips">
            <span class="hero-chip">SEC EDGAR</span>
            <span class="hero-chip">GDELT Context</span>
            <span class="hero-chip">FinBERT</span>
            <span class="hero-chip">Risk Propagation</span>
            <span class="hero-chip">Counterfactual Stress</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


with open(DATA_PATH, "r", encoding="utf-8") as file:
    documents = json.load(file)

documents = [
    document
    for document in documents
    if document.get("text_available") and document.get("text")
]

documents = sorted(
    documents,
    key=lambda document: document.get("timestamp", ""),
    reverse=True,
)
st.divider()
left, right = st.columns([1, 1], gap="medium")
with left:
    st.subheader("Financial Evidence")
    input_mode = st.radio(
        "Input source",
        ["SEC EDGAR", "Manual Text"],
        horizontal=True,
    )
    if input_mode == "SEC EDGAR":
        document_options = [
            f"{document['timestamp']} | {document['title']}"
            for document in documents
        ]
        selected_document = st.selectbox(
            "SEC filing",
            document_options,
        )
        selected_index = document_options.index(selected_document)
        document = documents[selected_index]
        entity = document.get("entity", "Unknown")
        text = document["text"]
        st.caption(
            f"Source: {document['source']} | Type: {document.get('document_type', 'Unknown')}"
        )
        with st.expander("View filing text"):
            st.text_area(
                "Filing",
                text,
                height=220,
                disabled=True,
                label_visibility="collapsed",
            )
    else:
        entity = st.text_input(
            "Entity",
            value="Apple Inc.",
        )
        text = st.text_area(
            "Financial text",
            value="Apple reported strong quarterly revenue growth and higher earnings, exceeding expectations.",
            height=220,
        )
    analyze = st.button(
        "Analyze Risk",
        type="primary",
        use_container_width=True,
    )

with right:
    st.subheader("Portfolio Stress Testing")
    scenario = st.selectbox(
        "Scenario",
        ["mild", "moderate", "severe"],
    )
    st.info(
        "Stress scenarios are counterfactual estimates based on configured portfolio exposure and propagation assumptions."
    )
if analyze:
    if not entity.strip() or not text.strip():
        st.error("Entity and financial text are required.")
        st.stop()
    with st.spinner("Running financial risk analysis..."):
        risk_response = requests.post(
            f"{API_URL}/risk",
            json={
                "entity": entity,
                "text": text,
            },
            timeout=300,
        )
    if risk_response.status_code != 200:
        st.error(risk_response.text)
        st.stop()
    risk_signal = risk_response.json()

    with st.spinner("Analyzing external market context..."):
      combined_response = requests.post(
          f"{API_URL}/combined-risk",
          json={"risk_signal": risk_signal},
          timeout=300,
      )
    if combined_response.status_code != 200:
        st.error(combined_response.text)
        st.stop()
    combined_risk = combined_response.json()

    with st.spinner("Running portfolio stress scenarios..."):
        stress_results = {}
        for current_scenario in ["mild", "moderate", "severe"]:
            response = requests.post(
                f"{API_URL}/stress",
                json={
                    "risk_signal": risk_signal,
                    "scenario": current_scenario,
                },
                timeout=60,
            )
            if response.status_code != 200:
                st.error(response.text)
                st.stop()
            stress_results[current_scenario] = response.json()["stress_test"]

    st.session_state["risk_signal"] = risk_signal
    st.session_state["combined_risk"] = combined_risk
    st.session_state["stress_results"] = stress_results
    st.session_state["entity"] = entity

if "risk_signal" in st.session_state:
    risk_signal = st.session_state["risk_signal"]
    combined_risk = st.session_state["combined_risk"]
    stress_results = st.session_state["stress_results"]
    entity = st.session_state["entity"]

    st.divider()

    st.markdown(
        '<div class="section-label">Risk Overview</div>',
        unsafe_allow_html=True,
    )

    sentiment = risk_signal["sentiment"]
    event = risk_signal["event"]
    impact = risk_signal["impact"]

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-card-title">Sentiment</div>
                <div class="risk-card-value">{sentiment['score']:+.2f}</div>
                <span class="status-pill">{sentiment['label'].title()}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-card-title">Detected Event</div>
                <div class="risk-card-value">{event['type'].replace('_', ' ').title()}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-card-title">Impact Score</div>
                <div class="risk-card-value">{impact['score']:.2f}<span style="font-size:0.8rem;color:#718096"> / 10</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-card-title">Risk Level</div>
                <div class="risk-card-value">{risk_signal['risk_level'].title()}</div>
                <span class="status-pill">{risk_signal['risk_level'].upper()}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-label">Risk Evidence</div>',
        unsafe_allow_html=True,
    )

    evidence_col1, evidence_col2 = st.columns([2, 1], gap="medium")

    with evidence_col1:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-card-title">Matched Event Keywords</div>
                <div class="risk-card-value" style="font-size:1rem;line-height:1.8">
                    {", ".join(event["matched_keywords"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with evidence_col2:
        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-card-title">Event Confidence</div>
                <div class="risk-card-value">{event['confidence']:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-label">External Market Context</div>',
        unsafe_allow_html=True,
    )

    external = combined_risk["external_context"]

    context_col1, context_col2, context_col3, context_col4 = st.columns(
        4,
        gap="medium",
    )

    with context_col1:
        st.metric("GDELT Records", external["records_found"])

    with context_col2:
        st.metric("Articles", external["article_count"])

    with context_col3:
        st.metric("Market Tone", f"{external['tone_score']:+.2f}")

    with context_col4:
        st.metric("Combined Risk", f"{combined_risk['combined_impact']:.2f}/10")

    st.caption(
        f"External adjustment: {combined_risk['external_adjustment']:+.2f}"
    )

    st.write(
        f"Financial domains: {', '.join(external['financial_domains'])}"
    )

    st.divider()

    st.subheader("Portfolio Stress Scenarios")

    scenario_cols = st.columns(3, gap="medium")

    for column, current_scenario in zip(
        scenario_cols,
        ["mild", "moderate", "severe"],
    ):
        result = stress_results[current_scenario]

        with column:
            st.markdown(
                f"""
                <div class="stress-card {current_scenario}">
                    <div class="stress-name">{current_scenario.title()} Scenario</div>
                    <div class="stress-value">{result['total_portfolio_impact'] * 100:.2f}%</div>
                    <div class="stress-shock">Portfolio shock · {result['shock'] * 100:.0f}%</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    selected_result = stress_results[scenario]

    st.subheader(f"{scenario.title()} Scenario Exposure")

    holdings = pd.DataFrame(selected_result["affected_holdings"])

    holdings["portfolio_contribution_pct"] = (
        holdings["portfolio_contribution"] * 100
    )

    display_holdings = holdings[
        [
            "entity",
            "ticker",
            "sector",
            "weight",
            "propagation_factor",
            "portfolio_contribution_pct",
        ]
    ].copy()

    display_holdings.columns = [
        "Entity",
        "Ticker",
        "Sector",
        "Portfolio Weight",
        "Propagation Factor",
        "Portfolio Impact (%)",
    ]

    display_holdings["Portfolio Weight"] = display_holdings[
        "Portfolio Weight"
    ].map(lambda value: f"{value * 100:.2f}%")

    display_holdings["Propagation Factor"] = (
        display_holdings["Propagation Factor"].round(2)
    )

    display_holdings["Portfolio Impact (%)"] = (
        display_holdings["Portfolio Impact (%)"].round(2)
    )

    st.dataframe(
        display_holdings,
        use_container_width=True,
        hide_index=True,
    )

    direct = selected_result["direct_impact"] * 100
    indirect = selected_result["indirect_impact"] * 100
    total = selected_result["total_portfolio_impact"] * 100

    impact_col1, impact_col2, impact_col3 = st.columns(3, gap="medium")

    with impact_col1:
        st.metric("Direct Impact", f"{direct:.2f}%")

    with impact_col2:
        st.metric("Indirect Impact", f"{indirect:.2f}%")

    with impact_col3:
        st.metric("Total Portfolio Impact", f"{total:.2f}%")

    st.divider()

    st.subheader("How the Risk Propagates")

    st.write(
        f"{entity} receives the full scenario shock. "
        "Other holdings in the same sector receive the configured propagation factor, "
        "while unrelated sectors receive no propagated shock."
    )
