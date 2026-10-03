from .processor import process_edgar_file


process_edgar_file(
    input_file="data/raw/edgar/apple_8k.json",
    output_file="data/processed/edgar_documents.json",
)