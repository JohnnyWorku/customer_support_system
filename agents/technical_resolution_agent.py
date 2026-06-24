# Each agent should:
# Analyze the issue
# Gather additional information if necessary
# Produce a recommended response
import os
import json
from dotenv import load_dotenv

from state import SupportState
from utils.groq.groq_provider import GroqProvider

class TechnicalAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("TECHNICAL_RESOLUTION_AGENT_MODEL_NAME")
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
            You are a Technical Resolution Agent for a customer support system.

            Your job is to analyze technical issues and provide an INTERNAL resolution recommendation.

            You are NOT speaking directly to the customer.

            Technical issues may include:

            - Login failures
            - Application crashes
            - Website errors
            - API issues
            - Performance problems
            - Data synchronization failures
            - Mobile app bugs
            - Browser compatibility issues
            - Installation problems
            - Service outages

            Customer message:

            {state["message"]}

            Analyze the issue and determine:

            1. What technical problem is being reported.
            2. Whether sufficient information is available.
            3. The most likely cause of the issue.
            4. Recommended troubleshooting actions.
            5. Whether escalation is required.

            Return ONLY valid JSON:

            {json_format}

            Rules:

            - Return JSON only.
            - No markdown.
            - No explanations outside JSON.
            - Confidence must be between 0 and 1.
            - If information is missing, set resolved=false.
            - If additional customer information is required, include it in recommended_actions.
            - Never claim an issue has been fixed unless explicitly stated.
            - Never invent logs, diagnostics, or system information.
            - Escalate if:
                - System outage suspected
                - Data corruption suspected
                - Security issue suspected
                - Backend/server issue suspected
                - Multiple failed troubleshooting attempts
                - Access to internal systems is required
            - Be conservative when assigning high confidence.
        """
        
        response = self.BILLING_LLM.generate_response(prompt)
        data = json.loads(response.text)

        state["confidence"] = data["confidence"]
        state["agent_response"] = data["resolution_summary"]
        state["escalation_required"] = data["escalation_required"]
        state["escalation_reason"] = data["escalation_reason"]
        state["escalation_summary"] = data["escalation_summary"]
        state["routing_path"].append("technical_agent")
        
        return state
