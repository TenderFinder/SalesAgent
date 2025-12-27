import json
from scorer import score_match


class TenderMatchingAgent:
    def __init__(self, product_file: str, tender_file: str):
        with open(product_file) as pf:
            self.offerings = json.load(pf)["offerings"]

        with open(tender_file) as tf:
            tender_data = json.load(tf)
            self.tenders = tender_data["services"]  # IMPORTANT

    def find_matches(self, min_score: float = 1.0):
        results = []

        for tender in self.tenders:
            for offering in self.offerings:
                score, reasons = score_match(offering, tender)

                if score >= min_score:
                    results.append({
                        "tender_id": tender["id"],
                        "tender_name": tender["display_name"],
                        "matched_offering": offering["name"],
                        "score": round(score, 2),
                        "reason": reasons,
                        "market_url": tender["market_url"]
                    })

        return results
