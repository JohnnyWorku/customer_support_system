# This is to evaluate the response of triage agent and to make sure the category is really correct
import os
import json
from dotenv import load_dotenv

from back.utils.groq.groq_provider import GroqProvider

load_dotenv()

class TriageAgentResponseEvaluator:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("TRAIGE_AGENT_RESPONSE_EVALUATOR_MODEL_NAME")
        self.TRIAGE_RESPONSE_EVALUATOR_LLM = GroqProvider(self.MODEL_NAME)
          
        
    def validate_response(self, response):
        VALID_CATEGORIES = {
            "billing",
            "technical_issue",
            "feature_request",
            "general_inquiry",
            "account_management"
        }
        
        try:
            data = json.loads(response)

            if data["category"] not in VALID_CATEGORIES:
                return False, "Invalid category"

            confidence = float(data["confidence"])

            if confidence < 0 or confidence > 1:
                return False, "Invalid confidence"

            return True, data

        except Exception as e:
            return False, str(e)
        
        
    def evaluator(self, message, response):
        json_format = """
            {
                "approved": true,
                "confidence": confidence must be a decimal number between 0 and 1,
                "reason": "..."
            }
        """
        
        
        review_prompt = f"""
            You are triage agent response reviewer.
            
            possible_categories = [
                "billing",
                "technical_issue",
                "feature_request",
                "general_inquiry",
                "account_management"
            ]
            
            Customer Message:
            {message}

            Classification:
            {response}

            Determine whether the classification is correct (in possible categories and correspondant with the message).

            Return ONLY VALID JSON like: {json_format}
            
            - No markdown.
            - No explanation.
            - No backticks.
            - Use lowercase true/false.
            
            If the response is not right and you think it needs escalation:
                - add "summary" key in the json and put your summary there.
        """
        
        try: 
            review_response = self.TRIAGE_RESPONSE_EVALUATOR_LLM.generate_response(review_prompt)
            
            review_response_text = review_response.text
            
            return review_response_text
        
        except Exception as e:
            return str(e)
