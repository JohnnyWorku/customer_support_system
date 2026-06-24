# This is to evaluate the response of triage agent and to make sure the category is really correct
import os
import json
from dotenv import load_dotenv

from back.utils.groq.groq_provider import GroqProvider
from utils.prompts.triage_evaluator_prompt import TriageEvaluatorPrompt


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
        
        
    def evaluator(self, response, state):
        review_prompt = TriageEvaluatorPrompt.prompt_dumper(response, state)
        
        try: 
            review_response = self.TRIAGE_RESPONSE_EVALUATOR_LLM.generate_response(review_prompt)
            
            review_response_text = review_response.text
            
            return review_response_text
        
        except Exception as e:
            return str(e)
