import json
from pathlib import Path

from src.ingestion.schema import FinancialDocument
from .cleaner import get_primary_text


def process_edgar_file(
    input_file: str,
    output_file: str,
) -> None:
    """
    Convert raw SEC filings into NLP-ready documents.
    """

    input_path = Path(input_file)
    output_path = Path(output_file)

    with open(input_path, "r", encoding="utf-8") as f:
        filings = json.load(f)

    processed_documents = []

    for filing in filings:

        analysis_text = get_primary_text(filing)

        if not analysis_text:
            continue

        document = FinancialDocument(
            source=filing["source"],
            timestamp=filing["timestamp"],
            title=filing["title"],
            text=analysis_text,
            url=filing["url"],
            entity=filing.get("entity"),
            document_type=filing.get("document_type"),
            text_available=bool(analysis_text),
            metadata={
                "text_length": len(analysis_text),
                "has_exhibit": bool(filing.get("exhibits")),
            },
        )

        processed_documents.append(document)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            [document.__dict__ for document in processed_documents],
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Processed {len(processed_documents)} documents "
        f"and saved to {output_path}"
    )