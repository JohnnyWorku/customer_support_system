# Each agent should:
# Analyze the issue
# Gather additional information if necessary
# Produce a recommended response
import os
import json
from dotenv import load_dotenv

from back.state import SupportState
from back.utils.groq.groq_provider import GroqProvider

class KnowledgeAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("KNOWLEDGE_AGENT_MODEL_NAME")
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
            You are a Knowledge Resolution Agent for a customer support system.

            Your job is to analyze general customer inquiries and provide an INTERNAL answer recommendation.

            You are NOT speaking directly to the customer.

            Examples of inquiries include:

            - Product information
            - Service information
            - How-to questions
            - Policy questions
            - Pricing questions
            - General guidance
            - Frequently asked questions
            - Clarification requests

            Customer message:

            {state["message"]}

            Analyze the inquiry and determine:

            1. What information the customer is requesting.
            2. Whether the question is clear.
            3. Whether enough information is available to answer.
            4. What answer should be provided.
            5. Whether clarification is needed.
            6. Whether escalation is required.

            Return ONLY valid JSON:

            {json_format}

            Rules:

            - Return JSON only.
            - No markdown.
            - No explanations outside JSON.
            - Confidence must be between 0 and 1.
            - If the inquiry is unclear, set clarification_needed=true.
            - If the inquiry cannot be answered with available information, set escalation_required=true.
            - Never invent company policies, pricing, features, account information, or technical details.
            - If information is missing, state that clarification is required.
        """
        
        response = self.BILLING_LLM.generate_response(prompt)
        data = json.loads(response.text)

        state["confidence"] = data["confidence"]
        state["agent_response"] = data["resolution_summary"]
        state["escalation_required"] = data["escalation_required"]
        state["escalation_reason"] = data["escalation_reason"]
        state["escalation_summary"] = data["escalation_summary"]
        state["routing_path"].append("knowledge_agent")
        
        return state
