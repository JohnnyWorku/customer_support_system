# Each agent should:
# Analyze the issue
# Gather additional information if necessary
# Produce a recommended response
import os
import json
from dotenv import load_dotenv

from state import SupportState
from utils.groq.groq_provider import GroqProvider

class BillingResolutionAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("BILLING_AGENT_MODEL_NAME")
        self.BILLING_LLM = GroqProvider(self.MODEL_NAME)
    
    def run(self, state: SupportState):
        json_format = """
            {
            "resolved": true,
            "confidence": 0.95,
            "issue_type": "double_charge",
            "resolution_summary": "brief internal explanation and recommended actions with bullets",
            "escalation_required": false,
            "escalation_reason": null,
            "escalation_summary": null,
            }
        """
        
        prompt = f"""
            You are a Billing Resolution Agent for a customer support system.

            Your job is to analyze billing-related customer issues and provide an internal resolution recommendation.

            You are NOT speaking directly to the customer.

            Billing issue categories may include:

            * Double charges
            * Refund requests
            * Failed payments
            * Subscription cancellations
            * Missing invoices
            * Incorrect billing amounts
            * Payment method updates
            * Plan upgrades or downgrades
            * Unexpected charges

            Customer message:
            {state["message"]}

            Analyze the issue and determine:

            1. What billing problem the customer is reporting.
            2. Whether sufficient information is available.
            3. Whether the issue can be resolved automatically.
            4. Whether escalation to a human billing specialist is required.

            Return ONLY valid JSON:

            {json_format}

            Rules:

            * Return JSON only.
            * No markdown.
            * No explanations outside JSON.
            * Confidence must be between 0 and 1.
            * If information is missing, set resolved=false.
            * If a refund requires manual approval, financial investigation, disputed charge, chargeback, fraud concern, or payment processor review, set escalation_required=true.
            * Be conservative when handling money-related issues.
        """
        
        response = self.BILLING_LLM.generate_response(prompt)
        data = json.loads(response.text)

        state["confidence"] = data["confidence"]
        state["agent_response"] = data["resolution_summary"]
        state["escalation_required"] = data["escalation_required"]
        state["escalation_reason"] = data["escalation_reason"]
        state["escalation_summary"] = data["escalation_summary"]
        state["routing_path"].append("billing_agent")
        
        return state