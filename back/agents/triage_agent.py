import os
import json
from dotenv import load_dotenv

from back.state import SupportState
from back.utils.groq.groq_provider import GroqProvider
from back.utils.evaluators.triage_agent_reponse_evaluator import TriageAgentResponseEvaluator

load_dotenv()

class TriageAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("TRAIGE_AGENT_MODEL_NAME")
        self.TRIAGE_LLM = GroqProvider(self.MODEL_NAME)
        self.EVALUATOR = TriageAgentResponseEvaluator()

    # to take the ticket and initialize the state
    def intake_node(self, state: SupportState):
        state["category"] = None
        state["agent_response"] = None
        state["confidence"] = None
        state["escalation_required"] = False
        state["escalation_reason"] = None
        state["escalation_summary"] = None
        state["tools_used"] = []
        state["routing_path"] = ["ticket_intake"]
        state["generated_response"] = None
        state["final_response"] = None
        
        return state


    def classify(self, state: SupportState):
        message = state["message"]
        state["routing_path"].append("triaging_issue")
        
        json_format = """
            {
                "category": "<YOUR ANSWER>",
                "confidence": confidence must be a decimal number between 0 and 1,
                "reason": "<YOUR EVIDENCE, FOR CHOOSING THE CATEGORY AND SETTING THE CONFIDENCE, FROM THE MESSAGE>"
            }
        """
        
        prompt = f"""
        You are a support ticket classifier.

        Classify the customer message into EXACTLY one of:

        - billing
        - technical_issue
        - feature_request
        - general_inquiry
        - account_management
        - escalation

        Rules:
        - Return only VALID JSON. In the form of {json_format}
        - No markdown.
        - No explanation.
        - No backticks.
        - Use lowercase true/false.
        - Do not create new categories.
        - If the situation is one of:
            uncertain
            unclear
            non sensical
            Missing information
            Complex technical issue
            Account security concern
            
            choose the closest category and lower confidence.
            
            if you choose escalation:
                - add "summary" key in the json  -- DON'T FORGET THIS.


        Customer message:
        {message}
        """
        
        for _ in range(3):
            response = self.TRIAGE_LLM.generate_response(prompt)
            response_text = response.text
            
            # print(f"response -> {response_text}")

            valid, result = self.EVALUATOR.validate_response(response_text)
            
            # print(f"validity -> {valid}")
            # print(f"result -> {result}")

            if not valid:
                continue

            evaluation = self.EVALUATOR.evaluator(
                message,
                response_text
            )

            evaluation_data = json.loads(evaluation)
            
            # print(f"evaluation_data -> {repr(evaluation_data)}")

            if evaluation_data["approved"]:
                state["category"] = result["category"]
                
                if state["category"] == "escalation":
                    state["escalation_reason"] = evaluation_data["reason"]
                    state["escalation_summary"] = evaluation_data["summary"]
                    
                return state

        state["category"] = "escalation"
        state["escalation_required"] = True
        state["escalation_reason"] = evaluation_data["reason"]
        state["escalation_summary"] = evaluation_data["summary"]
        
        return state
