import requests
from typing import List
from bs4 import BeautifulSoup

from .schema import FinancialDocument


SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"

HEADERS = {
    "User-Agent": "AI-Risk-Engine waitaminute2024@gmail.com"
}


def extract_filing_text(url: str) -> str:
    """Download an SEC document and extract readable text."""

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup(["script", "style", "ix:header", "ix:hidden"]):
        element.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())

    return text


def get_filing_index_url(cik: str, accession: str) -> str:
    """Build the SEC filing index URL."""

    accession_clean = accession.replace("-", "")

    return (
        f"https://www.sec.gov/Archives/edgar/data/"
        f"{int(cik)}/{accession_clean}/"
        f"{accession}-index.html"
    )


def fetch_edgar_filings(
    cik: str,
    forms: tuple = ("8-K",),
    limit: int = 10,
) -> List[FinancialDocument]:

    cik = cik.zfill(10)

    response = requests.get(
        SEC_SUBMISSIONS_URL.format(cik=cik),
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    recent = data["filings"]["recent"]

    documents = []

    for i, form in enumerate(recent["form"]):

        if form not in forms:
            continue

        accession = recent["accessionNumber"][i]
        filing_date = recent["filingDate"][i]
        primary_document = recent["primaryDocument"][i]

        accession_clean = accession.replace("-", "")

        filing_url = (
            f"https://www.sec.gov/Archives/edgar/data/"
            f"{int(cik)}/{accession_clean}/{primary_document}"
        )

        index_url = get_filing_index_url(cik, accession)

        print(f"Downloading filing: {primary_document}")

        filing_text = extract_filing_text(filing_url)

        # Download the filing index so we can inspect
        # attached exhibits and other documents.
        index_response = requests.get(
            index_url,
            headers=HEADERS,
            timeout=30,
        )

        index_response.raise_for_status()

        index_soup = BeautifulSoup(
            index_response.text,
            "html.parser"
        )

        print("\nSEC INDEX LINKS:")

        for link in index_soup.find_all("a", href=True):
            print(
                "TEXT:",
                link.get_text(" ", strip=True),
                "| HREF:",
                link["href"]
            )

        exhibits = []

        for link in index_soup.find_all("a", href=True):

            href = link["href"]
            link_text = link.get_text(" ", strip=True)

            combined = f"{link_text} {href}".upper()

            if "EX-99" in combined or "EX99" in combined:
                exhibits.append({
                    "name": link_text,
                    "url": href,
                })

        exhibit_data = []

        for exhibit in exhibits:
            print("  ", exhibit["name"], "->", exhibit["url"])

            exhibit_url = exhibit["url"]

            if exhibit_url.startswith("/"):
                exhibit_url = "https://www.sec.gov" + exhibit_url

            print(f"Downloading exhibit: {exhibit['name']}")

            exhibit_text = extract_filing_text(exhibit_url)

            print(f"Exhibit text length: {len(exhibit_text)}")

            exhibit_data.append({
                "name": exhibit["name"],
                "url": exhibit_url,
                "text": exhibit_text,
            })

        print(f"Found {len(exhibits)} exhibits")

        document = FinancialDocument(
          source="SEC_EDGAR",
          timestamp=filing_date,
          title=f"{form} filing - {primary_document}",
          text=filing_text,
          url=filing_url,
          entity=data["name"],
          document_type=form,
          exhibits=exhibit_data,
      )

        documents.append(document)

        if len(documents) >= limit:
            break

    return documents