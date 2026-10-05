from typing import Iterable


class GDELTContextAnalyzer:
    """
    Aggregate external financial context from GDELT GKG records.

    GDELT GKG does not provide article body text in our bulk dataset,
    so this module uses structured metadata such as:
    - organization mentions
    - financial domains
    - GDELT tone
    - article counts
    """

    def analyze(
        self,
        records: Iterable[dict],
        entity: str,
    ) -> dict:

        target = self._normalize_entity(entity)

        matching_records = []

        for record in records:
            organizations = record.get("organizations", [])

            normalized_organizations = {
                self._normalize_entity(org)
                for org in organizations
            }

            if target in normalized_organizations:
                matching_records.append(record)

        if not matching_records:
            return {
                "entity": entity,
                "records_found": 0,
                "article_count": 0,
                "average_tone": 0.0,
                "tone_score": 0.0,
                "financial_domains": [],
            }

        total_articles = sum(
            record.get("num_articles", 0)
            for record in matching_records
        )

        if total_articles == 0:
            total_articles = len(matching_records)

        weighted_tone = sum(
            record.get("tone", 0.0) * max(record.get("num_articles", 1), 1)
            for record in matching_records
        )

        average_tone = weighted_tone / total_articles

        domains = sorted({
            domain
            for record in matching_records
            for domain in record.get("financial_domains", [])
        })

        # GDELT tone is not a -1 to +1 sentiment score.
        # We expose a bounded contextual score separately.
        tone_score = max(-1.0, min(1.0, average_tone / 10.0))

        return {
            "entity": entity,
            "records_found": len(matching_records),
            "article_count": total_articles,
            "average_tone": round(average_tone, 4),
            "tone_score": round(tone_score, 4),
            "financial_domains": domains,
        }

    @staticmethod
    def _normalize_entity(entity: str) -> str:
        normalized = entity.lower().strip()
        normalized = normalized.replace(".", "")
        return " ".join(normalized.split())