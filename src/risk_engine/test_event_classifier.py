import json

from src.risk_engine.event_classifier import FinancialEventClassifier


with open(
    "data/processed/edgar_documents.json",
    "r",
    encoding="utf-8",
) as f:
    documents = json.load(f)


document = documents[0]

classifier = FinancialEventClassifier()

result = classifier.classify(document["text"])

print("Document:", document["title"])
print("Entity:", document["entity"])
print("Event:", result["event"])
print("Confidence:", result["confidence"])
print("Matched keywords:", result["matched_keywords"])