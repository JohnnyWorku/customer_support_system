# Each agent should:
# Analyze the issue
# Gather additional information if necessary
# Produce a recommended response
import os
import json
from dotenv import load_dotenv

from back.state import SupportState
from back.utils.groq.groq_provider import GroqProvider


load_dotenv()

class AccountManagementResolutionAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("ACCOUNT_MANAGEMENT_RESOLUTION_AGENT")
        self.ACCOUNT_LLM = GroqProvider(self.MODEL_NAME)
    
    def run(self, state: SupportState):
        json_format = """
            {
            "resolved": true,
            "confidence": 0.95,
            "resolution_summary": "brief internal explanation and recommended actions with bullets",
            "escalation_required": false,
            "escalation_reason": null
            "escalation_summary": null,
            }
        """
        
        prompt = f"""
            You are an Account Management Resolution Agent for a customer support system.

            Your job is to analyze customer account-related issues and provide an internal resolution recommendation.

            You are NOT speaking directly to the customer.

            Possible account management issues include:

            * Login problems
            * Password reset requests
            * Email change requests
            * Profile update requests
            * Account lockouts
            * Account verification issues
            * Account deletion requests
            * Security concerns

            Customer message:
            {state["message"]}

            Analyze the issue and determine:

            1. What the customer is requesting.
            2. Whether sufficient information is available.
            3. Whether the issue can be resolved automatically.
            4. Whether escalation to a human support representative is required.

            Return ONLY valid JSON in the following format:

            {json_format}

            Rules:

            * Return JSON only.
            * No markdown.
            * No explanations outside JSON.
            * If information is missing, set resolved=false.
            * If the issue involves security concerns, identity verification, suspicious activity, account takeover, or sensitive account changes, set escalation_required=true.
            * Confidence must be between 0 and 1.
        """
        
        response = self.ACCOUNT_LLM.generate_response(prompt)
        data = json.loads(response.text)

        state["confidence"] = data["confidence"]
        state["agent_response"] = data["resolution_summary"]
        state["escalation_required"] = data["escalation_required"]
        state["escalation_reason"] = data["escalation_reason"]
        state["escalation_summary"] = data["escalation_summary"]
        state["routing_path"].append("billing_agent")
        
        return state
        
        return state
