import re


def clean_sec_text(text: str) -> str:
    """
    Clean SEC filing or exhibit text while preserving
    financially meaningful information.
    """

    if not text:
        return ""

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove common SEC checkbox symbols
    text = re.sub(r"☐|☒|□|■", " ", text)

    # Remove signature section
    signature_match = re.search(
        r"\bSIGNATURES?\b",
        text,
        flags=re.IGNORECASE,
    )

    if signature_match:
        text = text[:signature_match.start()].strip()

    # Normalize whitespace again
    text = re.sub(r"\s+", " ", text).strip()

    return text


def get_primary_text(filing: dict) -> str:
    """
    Select the most financially informative text from an SEC filing.

    Exhibit 99.x is preferred because it commonly contains
    the substantive press release or financial announcement.
    """

    exhibits = filing.get("exhibits", [])

    exhibit_texts = [
        exhibit.get("text", "")
        for exhibit in exhibits
        if exhibit.get("text")
    ]

    if exhibit_texts:
        return clean_sec_text(" ".join(exhibit_texts))

    return clean_sec_text(filing.get("text", ""))