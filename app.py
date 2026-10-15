import streamlit as st
import requests
import json

# Page Configuration
st.set_page_config(
    page_title="Agentic AI Financial Fraud & Compliance Audit",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Agentic AI Financial Fraud & Compliance Audit System")
st.markdown("Automated transaction processing, multi-agent risk assessment, and offline compliance auditing via local LLMs (Ollama).")

# Sidebar for Transaction Inputs
st.sidebar.header("Transaction Parameters")

transaction_id = st.sidebar.text_input("Transaction ID", value="TXN-98421")
timestamp = st.sidebar.text_input("Timestamp", value="2026-10-15T14:32:00Z")
sender_account = st.sidebar.text_input("Sender Account", value="ACC-40291")
receiver_account = st.sidebar.text_input("Receiver Account", value="ACC-88310")
amount_usd = st.sidebar.number_input("Amount (USD)", min_value=0.0, value=12500.00, step=100.0)
location = st.sidebar.selectbox("Location", ["Lagos, Nigeria", "New York, USA", "London, UK", "Panama City, Panama", "Kolkata, India"])
device_id = st.sidebar.text_input("Device ID", value="DEV-XYZ-99")
transaction_type = st.sidebar.selectbox("Transaction Type", ["Wire Transfer", "ACH", "Crypto Exchange", "POS Purchase"])
account_age_days = st.sidebar.number_input("Account Age (Days)", min_value=0, value=12)
previous_fraud_flags = st.sidebar.number_input("Previous Fraud Flags", min_value=0, value=0)

API_URL = "http://localhost:8000/audit-transaction"

if st.sidebar.button("Run Multi-Agent Audit", type="primary"):
    payload = {
        "transaction_id": transaction_id,
        "timestamp": timestamp,
        "sender_account": sender_account,
        "receiver_account": receiver_account,
        "amount_usd": amount_usd,
        "location": location,
        "device_id": device_id,
        "transaction_type": transaction_type,
        "account_age_days": account_age_days,
        "previous_fraud_flags": previous_fraud_flags
    }

    with st.spinner("Agents are analyzing transaction and querying Ollama..."):
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                
                # Layout results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🤖 Agent 1: Risk Flagger")
                    eval_res = result.get("evaluation", {})
                    if eval_res.get("is_flagged"):
                        st.error(f"Status: Flagged ({eval_res.get('risk_indicator_count')} indicators found)")
                    else:
                        st.success("Status: Clean")
                    
                    st.write("**Identified Flags:**")
                    for flag in eval_res.get("flags", []):
                        st.markdown(f"- {flag}")
                        
                with col2:
                    st.subheader("📊 Agent 2: Risk Scorer")
                    scoring_res = result.get("scoring", {})
                    score = scoring_res.get("risk_score")
                    
                    if score >= 70:
                        st.metric("Risk Score", f"{score}/100", delta="High Risk", delta_color="inverse")
                    elif score >= 30:
                        st.metric("Risk Score", f"{score}/100", delta="Medium Risk", delta_color="off")
                    else:
                        st.metric("Risk Score", f"{score}/100", delta="Low Risk", delta_color="normal")
                        
                    st.markdown(f"**Compliance Tier:** {scoring_res.get('compliance_tier')}")
                    st.markdown(f"**Human Review Required:** {scoring_res.get('requires_human_review')}")

                st.markdown("---")
                st.subheader("📜 Local LLM Audit Report (Ollama)")
                st.info(result.get("compliance_audit_narrative"))
                
            else:
                st.error(f"Error from Backend: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to FastAPI backend. Please ensure your backend is running (`uvicorn backend.main:app --reload`).")