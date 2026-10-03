import json
from pathlib import Path

from .edgar_loader import fetch_edgar_filings


filings = fetch_edgar_filings(
    cik="320193",
    forms=("8-K",),
    limit=10,
)

output_dir = Path("data/raw/edgar")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "apple_8k.json"

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(
        [filing.__dict__ for filing in filings],
        f,
        indent=2,
        ensure_ascii=False,
    )

print(f"Saved {len(filings)} filings to {output_file}")