import json
from pathlib import Path

from .cleaner import get_primary_text


input_file = Path("data/raw/edgar/apple_8k.json")

with open(input_file, "r", encoding="utf-8") as f:
    filings = json.load(f)


for filing in filings[:5]:

    primary_text = get_primary_text(filing)

    print("=" * 80)
    print("TITLE:", filing["title"])
    print("ENTITY:", filing["entity"])
    print("EXHIBITS:", len(filing.get("exhibits", [])))
    print("PRIMARY TEXT LENGTH:", len(primary_text))
    print()
    print("PRIMARY TEXT:")
    print(primary_text[:2000])
    print()