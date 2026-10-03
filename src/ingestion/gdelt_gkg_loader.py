import csv
import zipfile
from typing import Iterator, Dict
from .schema import FinancialDocument

ZIP_PATH = "data/raw/gdelt/20260930.gkg.csv.zip"


FINANCIAL_THEMES = {
    "markets": {
        "ECON_STOCKMARKET",
        "WB_332_CAPITAL_MARKETS",
    },
    "banking": {
        "WB_318_FINANCIAL_ARCHITECTURE_AND_BANKING",
        "WB_336_NON_BANK_FINANCIAL_INSTITUTIONS",
        "WB_337_INSURANCE",
    },
    "macro": {
        "ECON_INFLATION",
        "ECON_INTEREST_RATES",
        "ECON_CENTRALBANK",
        "ECON_DEBT",
        "ECON_TAXATION",
        "ECON_WORLDCURRENCIES",
    },
    "commodities": {
        "ECON_OILPRICE",
        "ECON_GASOLINEPRICE",
        "ECON_DIESELPRICE",
        "ECON_HEATINGOIL",
    },
    "housing": {
        "ECON_HOUSING_PRICES",
        "WB_612_HOUSING_FINANCE",
    },
    "trade": {
        "WB_698_TRADE",
    },
}


def parse_tone(tone: str) -> float:
    if not tone:
        return 0.0

    try:
        return float(tone.split(",")[0])
    except (ValueError, IndexError):
        return 0.0


def get_financial_domains(themes: str) -> list[str]:
    theme_set = set(
        theme
        for theme in themes.split(";")
        if theme
    )

    domains = []

    for domain, domain_themes in FINANCIAL_THEMES.items():
        if theme_set.intersection(domain_themes):
            domains.append(domain)

    return domains

def split_gdelt_field(value: str) -> list[str]:
    if not value:
        return []

    return [
        item.strip()
        for item in value.split("<UDIV>")
        if item.strip()
    ]

def read_gkg_records(
    zip_path: str = ZIP_PATH,
) -> Iterator[Dict]:

    with zipfile.ZipFile(zip_path, "r") as archive:

        csv_name = archive.namelist()[0]

        with archive.open(csv_name) as file:

            reader = csv.reader(
                (
                    line.decode("utf-8", errors="replace")
                    for line in file
                ),
                delimiter="\t",
            )

            next(reader)

            for row in reader:

                if len(row) < 11:
                    continue

                themes = row[3]
                organizations = [
                    org.strip()
                    for org in row[6].split(";")
                    if org.strip()
                ]

                financial_domains = get_financial_domains(themes)

                if not financial_domains:
                    continue

                yield {
                    "source": "GDELT",
                    "timestamp": row[0],
                    "num_articles": int(row[1]) if row[1].isdigit() else 0,
                    "themes": [
                        theme
                        for theme in themes.split(";")
                        if theme
                    ],
                    "financial_domains": financial_domains,
                    "organizations": organizations,
                    "tone": parse_tone(row[7]),
                    "sources": [
                      source.strip()
                      for source in row[9].split(";")
                      if source.strip()
                  ],
                  "source_urls": split_gdelt_field(row[10]),
                }
def to_document(record: Dict) -> FinancialDocument:
    organizations = record.get("organizations", [])
    source_urls = record.get("source_urls", [])

    return FinancialDocument(
        source="GDELT",
        timestamp=record.get("timestamp", ""),
        title="",
        text="",
        url=source_urls[0] if source_urls else "",
        entity=organizations[0] if organizations else None,
        document_type="news",
        text_available=False,
        metadata={
            "themes": record.get("themes", []),
            "financial_domains": record.get("financial_domains", []),
            "organizations": organizations,
            "tone": record.get("tone", 0.0),
            "num_articles": record.get("num_articles", 0),
            "sources": record.get("sources", []),
            "source_urls": source_urls,
        },
    )