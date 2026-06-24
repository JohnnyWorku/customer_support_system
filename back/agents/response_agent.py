# Generate the final response returned to the customer.
# The response should include:
# Resolution summary
# Recommended actions
# Escalation status (if applicable)
import os
import json
from dotenv import load_dotenv

from back.state import SupportState
from back.utils.groq.groq_provider import GroqProvider
from back.utils.evaluators.response_evaluator import ResponseEvaluatorAgent


load_dotenv()

class ResponseAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("RESPONSE_AGENT_MODEL_NAME")
        self.RESPONSE_LLM = GroqProvider(self.MODEL_NAME)
        self.EVALUATOR = ResponseEvaluatorAgent()
        
    def run(self, state: SupportState):
        customer_message = state["message"]
        category = state["category"]
        confidence = state["confidence"]
        agent_response = state["agent_response"]
        
        json_structure = {
            "category": "escalate",
            "reason": "your reason",
            "summary": "your summary"
        }
        
        prompt = f"""
            You are a professional customer support assistant.

            Your job is to generate a clear, helpful response to the customer based on internal analysis.

            ---

            Customer message:
            {customer_message}

            ---

            Internal classification:
            Category: {category}
            Confidence: {confidence}

            ---

            Agent analysis / internal resolution:
            {agent_response}

            ---

            Rules:
            - Write a natural, polite customer-facing message.
            - Include recommended actions.
            - Do NOT mention confidence values explicitly.
            - If confidence is low (<0.7), be cautious and suggest escalation or clarification.
            - If issue is resolved, clearly explain the resolution.
            - If information is missing, ask clarifying questions.
            - Keep response concise and professional.
            - Do not expose internal reasoning.

            ---

            Generate a professional customer-facing response.

            Structure the response as:

            1. Acknowledgement of the issue
            2. Resolution summary
            3. Recommended actions
            4. Escalation status (if applicable)
            5. Professional closing

            Do NOT return JSON unless escalation is required.
            Return plain text only.
            
            - Never claim to have checked, verified, reviewed, refunded, fixed, investigated, or modified anything unless explicitly stated in the internal agent analysis.
            - Do not invent actions that were not performed.
            - If information is unavailable, state that additional review may be required.
            
            If you think the response is not correct and it must be escalated to human support team add "reason" and "summary" to the json.
            
            Return ONLY valid JSON: {json_structure} if you think it must be escalated
            
            - No markdown.
            - No explanation.
            - No backticks.
            - Use lowercase true/false.
        """
        
        
        response = self.RESPONSE_LLM.generate_response(prompt)
        response_text = response.text
        
        state["generated_response"] = response_text
        
        evaluation = self.EVALUATOR.evaluator(customer_message, response_text, state)
        
        # print(f"evaluation -> {evaluation}")
        evaluation_data = json.loads(evaluation)
        
        if evaluation_data["approved"]:
                state["final_response"] = state["generated_response"]
                return state

        state["category"] = "escalation"
        state["escalation_required"] = True
        state["escalation_reason"] = evaluation_data["reason"]
        state["escalation_summary"] = evaluation_data["summary"]
        
        return state
