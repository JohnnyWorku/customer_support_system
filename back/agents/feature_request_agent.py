# Each agent should:
# Analyze the issue
# Gather additional information if necessary
# Produce a recommended response
import os
import json
from dotenv import load_dotenv

from back.state import SupportState
from back.utils.groq.groq_provider import GroqProvider
from utils.prompts.feature_prompt import FeaturePrompt

class FeatureRequestAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("FEATURE_AGENT_MODEL_NAME")
        self.BILLING_LLM = GroqProvider(self.MODEL_NAME)
    
    def run(self, state: SupportState):
        prompt = FeaturePrompt.prompt_dumper(state)
        
        response = self.BILLING_LLM.generate_response(prompt)
        data = json.loads(response.text)

        state["confidence"] = data["confidence"]
        state["agent_response"] = data["resolution_summary"]
        state["escalation_required"] = data["escalation_required"]
        state["escalation_reason"] = data["escalation_reason"]
        state["escalation_summary"] = data["escalation_summary"]
        state["routing_path"].append("feature_agent")
        
        return state