from typing import Dict, Any, List

class RiskFlaggerAgent:
    """
    Agent 1: Responsible for inspecting transaction details, 
    evaluating behavioral heuristics, and flagging suspicious indicators.
    """
    
    def __init__(self):
        self.HIGH_AMOUNT_THRESHOLD = 10000.00
        self.NEW_ACCOUNT_THRESHOLD_DAYS = 30

    def evaluate_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        flags: List[str] = []
        risk_indicators_count = 0

        amount = transaction.get("amount_usd", 0.0)
        account_age = transaction.get("account_age_days", 365)
        prev_flags = transaction.get("previous_fraud_flags", 0)
        location = transaction.get("location", "Unknown")

        # Rule 1: High transaction amount check
        if amount > self.HIGH_AMOUNT_THRESHOLD:
            flags.append(f"High-value transaction detected: ${amount:,.2f}")
            risk_indicators_count += 2

        # Rule 2: New account velocity risk
        if account_age < self.NEW_ACCOUNT_THRESHOLD_DAYS:
            flags.append(f"Young account risk: Account is only {account_age} days old.")
            risk_indicators_count += 2

        # Rule 3: Historical fraud flags
        if prev_flags > 0:
            flags.append(f"History of suspicious activity: {prev_flags} prior flags recorded.")
            risk_indicators_count += 3

        # Rule 4: High-risk location heuristic
        high_risk_locations = ["Lagos, Nigeria", "Panama City, Panama", "Unknown"]
        if location in high_risk_locations:
            flags.append(f"Unusual or high-risk geographic location: {location}")
            risk_indicators_count += 1

        is_flagged = len(flags) > 0

        return {
            "transaction_id": transaction.get("transaction_id"),
            "is_flagged": is_flagged,
            "risk_indicator_count": risk_indicators_count,
            "flags": flags
        }