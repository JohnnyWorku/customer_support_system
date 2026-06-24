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
from utils.prompts.response_prompt import ResponsePrompt


load_dotenv()

class ResponseAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("RESPONSE_AGENT_MODEL_NAME")
        self.RESPONSE_LLM = GroqProvider(self.MODEL_NAME)
        self.EVALUATOR = ResponseEvaluatorAgent()
        
    def run(self, state: SupportState):
        prompt = ResponsePrompt.prompt_dumper(state)
        
        
        response = self.RESPONSE_LLM.generate_response(prompt)
        response_text = response.text
        
        state["generated_response"] = response_text
        
        evaluation = self.EVALUATOR.evaluator(state)
        
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
