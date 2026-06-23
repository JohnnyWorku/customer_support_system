import os
import json
from dotenv import load_dotenv

from state import SupportState
from utils.groq_provider import GroqProvider
from utils.triage_agent_reponse_evaluator import TriageAgentResponseEvaluator

load_dotenv()

class TriageAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("TRAIGE_AGENT_MODEL_NAME")
        self.TRIAGE_LLM = GroqProvider(self.MODEL_NAME)
        self.EVALUATOR = TriageAgentResponseEvaluator()

    # to take the ticket and initialize the state
    def intake_node(self, state: SupportState):
        state["routing_path"] = ["ticket_intake"]
        state["tools_used"] = []
        return state


    def classify(self, message):
        prompt = f"""
        You are a support ticket classifier.

        Classify the customer message into EXACTLY one of:

        - billing
        - technical_issue
        - feature_request
        - general_inquiry
        - account_management

        Rules:
        - Return only JSON. In the form of '{
            "catagory": "<YOUR ANSWER>",
            "confidence": "<YOUR ANSWER>",
            "reason": "<YOUR EVIDENCE, FOR CHOOSING THE CATEGORY AND SETTING THE CONFIDENCE, FROM THE MESSAGE>"
        }'
        - Do not create new categories.
        - If uncertain, choose the closest category and lower confidence.
        - If the situation is one of:
            Missing information
            Complex technical issue
            Account security concern
            
            make the category one of the with valid reason and confidence.


        Customer message:
        {message}
        """
        
        for _ in range(3):
            response = self.TRIAGE_LLM.generate_response(prompt)

            valid, result = self.EVALUATOR.validate_response(response)

            if not valid:
                continue

            evaluation = self.EVALUATOR.evaluator(
                message,
                response
            )

            evaluation_data = json.loads(evaluation)

            if evaluation_data["approved"]:
                return {
                    "status": "classified",
                    "result": result
                }

        return {
            "status": "escalate",
            "reason": "Unable to confidently classify ticket"
        }
