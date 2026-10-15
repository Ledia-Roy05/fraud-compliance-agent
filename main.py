from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from backend.agents.risk_flagger import RiskFlaggerAgent
from backend.agents.risk_scorer import RiskScorerAgent
from backend.llm_service import OllamaLLMService

app = FastAPI(
    title="Agentic AI Financial Fraud & Compliance Audit System",
    description="Multi-agent automated transaction risk flagging, scoring, and offline LLM auditing.",
    version="1.0.0"
)

# Initialize Agents and Service
flagger_agent = RiskFlaggerAgent()
scorer_agent = RiskScorerAgent()
llm_service = OllamaLLMService(model_name="llama3")

# Define Request Schema using Pydantic
class TransactionSchema(BaseModel):
    transaction_id: str
    timestamp: str
    sender_account: str
    receiver_account: str
    amount_usd: float
    location: str
    device_id: str
    transaction_type: str
    account_age_days: int
    previous_fraud_flags: int

@app.get("/")
def read_root():
    return {"status": "Online", "system": "Agentic AI Compliance & Fraud Audit Backend"}

@app.post("/audit-transaction")
def audit_transaction(transaction: TransactionSchema):
    try:
        txn_dict = transaction.dict()

        # Step 1: Run Agent 1 (Risk Flagger)
        evaluation_result = flagger_agent.evaluate_transaction(txn_dict)

        # Step 2: Run Agent 2 (Risk Scorer)
        scoring_result = scorer_agent.calculate_score(evaluation_result)

        # Step 3: Generate Local LLM Compliance Narrative via Ollama
        llm_narrative = llm_service.generate_compliance_report(
            transaction=txn_dict,
            evaluation=evaluation_result,
            scoring=scoring_result
        )

        # Compile Full Audit Report
        audit_report = {
            "transaction_id": transaction.transaction_id,
            "evaluation": evaluation_result,
            "scoring": scoring_result,
            "compliance_audit_narrative": llm_narrative
        }

        return audit_report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))