# Each agent should:
# Analyze the issue
# Gather additional information if necessary
# Produce a recommended response
import os
import json
from dotenv import load_dotenv

from utils.prompts.account_prompt import AccountPrompt
from back.state import SupportState
from back.utils.groq.groq_provider import GroqProvider


load_dotenv()

class AccountManagementResolutionAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("ACCOUNT_MANAGEMENT_RESOLUTION_AGENT")
        self.ACCOUNT_LLM = GroqProvider(self.MODEL_NAME)
    
    def run(self, state: SupportState):
        
        prompt = AccountPrompt.prompt_dumper(state)
        
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
