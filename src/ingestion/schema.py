from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FinancialDocument:
    source: str
    timestamp: str
    title: str
    text: str
    url: str

    entity: Optional[str] = None
    document_type: Optional[str] = None

    text_available: bool = False

    metadata: dict = field(default_factory=dict)