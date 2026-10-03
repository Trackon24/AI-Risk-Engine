import json
from pathlib import Path
from typing import Iterable

from src.ingestion.schema import FinancialDocument


def save_documents(
    documents: Iterable[FinancialDocument],
    output_file: str,
) -> None:
    documents = list(documents)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = [document.__dict__ for document in documents]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(data)} documents to {output_file}")