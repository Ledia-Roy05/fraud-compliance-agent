from typing import Dict, Any

class RiskScorerAgent:
    """
    Agent 2: Responsible for calculating a quantitative risk score (0-100) 
    and assigning a compliance risk tier based on Agent 1's findings.
    """

    def calculate_score(self, evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
        indicator_count = evaluation_result.get("risk_indicator_count", 0)
        
        # Calculate raw score (scaling each indicator weight up)
        # Max expected indicators roughly around 8-10 translates to ~100 score
        raw_score = indicator_count * 12.5
        risk_score = min(max(raw_score, 0.0), 100.0)

        # Determine compliance tier
        if risk_score >= 70.0:
            tier = "HIGH RISK (Immediate Review / Blocked)"
        elif risk_score >= 30.0:
            tier = "MEDIUM RISK (Manual Compliance Audit Required)"
        else:
            tier = "LOW RISK (Approved)"

        return {
            "transaction_id": evaluation_result.get("transaction_id"),
            "risk_score": round(risk_score, 2),
            "compliance_tier": tier,
            "requires_human_review": risk_score >= 30.0
        }