from src.ingestion.gdelt_gkg_loader import read_gkg_records
from src.stress_testing.gdelt_context import GDELTContextAnalyzer


def main():
    records = read_gkg_records()

    analyzer = GDELTContextAnalyzer()

    context = analyzer.analyze(
        records=records,
        entity="Apple Inc.",
    )

    print("GDELT EXTERNAL CONTEXT")
    print("-" * 40)
    print(f"Entity          : {context['entity']}")
    print(f"Records found   : {context['records_found']}")
    print(f"Article count   : {context['article_count']}")
    print(f"Average tone    : {context['average_tone']:+.4f}")
    print(f"Tone score      : {context['tone_score']:+.4f}")
    print(f"Financial areas : {context['financial_domains']}")


if __name__ == "__main__":
    main()