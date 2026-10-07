from pathlib import Path
from typing import Any, Literal

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.risk_engine.sentiment import FinancialSentimentAnalyzer
from src.risk_engine.event_classifier import FinancialEventClassifier
from src.risk_engine.impact_scorer import FinancialImpactScorer
from src.risk_engine.risk_signal import RiskSignalBuilder
from src.stress_testing.risk_stress import RiskSignalStressTester
from src.risk_engine.gdelt_context import GDELTContextAnalyzer
from src.risk_engine.combined_risk import CombinedRiskBuilder
from src.ingestion.gdelt_gkg_loader import read_gkg_records

app = FastAPI(
    title="AI Risk Engine",
    description="Financial NLP risk intelligence API",
    version="1.0.0",
)

sentiment_analyzer = FinancialSentimentAnalyzer()
event_classifier = FinancialEventClassifier()
impact_scorer = FinancialImpactScorer()
risk_signal_builder = RiskSignalBuilder()

portfolio_path = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "demo"
    / "portfolio.csv"
)

portfolio = pd.read_csv(portfolio_path)

stress_tester = RiskSignalStressTester(
    portfolio=portfolio,
    same_sector_factor=0.30,
)

gdelt_analyzer = GDELTContextAnalyzer()
combined_risk_builder = CombinedRiskBuilder()

class RiskRequest(BaseModel):
    entity: str
    text: str


class StressRequest(BaseModel):
    risk_signal: dict[str, Any]
    scenario: Literal["mild", "moderate", "severe"]

class CombinedRiskRequest(BaseModel):
    risk_signal: dict[str, Any]

@app.get("/")
def root():
    return {
        "service": "AI Risk Engine",
        "status": "running",
    }


@app.post("/risk")
def analyze_risk(request: RiskRequest):
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    sentiment = sentiment_analyzer.analyze(request.text)
    event = event_classifier.classify(request.text)

    impact = impact_scorer.calculate(
        event=event["event"],
        sentiment_score=sentiment["score"],
        event_confidence=event["confidence"],
    )

    risk_signal = risk_signal_builder.build(
        entity=request.entity,
        sentiment=sentiment,
        event=event,
        impact=impact,
    )

    return risk_signal


@app.post("/stress")
def stress_portfolio(request: StressRequest):
    try:
        return stress_tester.run(
            risk_signal=request.risk_signal,
            scenario=request.scenario,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@app.post("/combined-risk")
def combined_risk(request: CombinedRiskRequest):
    entity = request.risk_signal.get("entity")

    if not entity:
        raise HTTPException(
            status_code=400,
            detail="Risk signal must contain an entity.",
        )

    gdelt_context = gdelt_analyzer.analyze(
        records=read_gkg_records(),
        entity=entity,
    )

    return combined_risk_builder.build(
        risk_signal=request.risk_signal,
        gdelt_context=gdelt_context,
    )