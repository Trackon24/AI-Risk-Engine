# AI Risk Engine

An AI/NLP-based financial risk intelligence system that converts
unstructured financial text into structured risk signals and
evaluates their potential portfolio impact.

## Problem

Financial risk information is scattered across news articles,
market commentary, and other unstructured text sources.

The goal of this project is to transform this information into
machine-readable risk signals containing:

- Sentiment score
- Event classification
- Impact score

The system will also use these signals for downstream portfolio
stress testing.

## Planned Architecture

Financial Text Sources
        ↓
Data Ingestion
        ↓
Text Preprocessing
        ↓
Entity Extraction
        ↓
Sentiment Analysis
        ↓
Event Classification
        ↓
Impact Scoring
        ↓
Structured Risk Signal
        ↓
Risk Propagation
        ↓
Portfolio Stress Testing

## Project Status

Day 1: Data ingestion and project foundation

## Tech Stack

- Python
- Pandas
- NumPy
- Transformers
- Scikit-learn
- FastAPI
- Streamlit
- Plotly

## Repository Structure

```text
data/          Public and demo datasets
src/           Application source code
experiments/   Model experiments
tests/         Tests
docs/          Architecture and presentation