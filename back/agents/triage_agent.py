import os
import json
from dotenv import load_dotenv

from back.state import SupportState
from back.utils.groq.groq_provider import GroqProvider
from back.utils.evaluators.triage_agent_reponse_evaluator import TriageAgentResponseEvaluator
from back.utils.prompts.triage_prompt import TriagePrompt
from neural_nets.predictor import TicketClassifier

load_dotenv()

class TriageAgent:
    def __init__(self):
        self.MODEL_NAME = os.environ.get("TRAIGE_AGENT_MODEL_NAME")
        self.TRIAGE_LLM = GroqProvider(self.MODEL_NAME)
        self.EVALUATOR = TriageAgentResponseEvaluator()
        self.classifier = TicketClassifier()

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
        state["routing_path"].append("triage_agent")
        
        
        # From neural network
        prediction = self.classifier.predict(message)

        category = prediction["category"]
        confidence = prediction["confidence"]

        print(f"NN Prediction: {category} ({confidence:.4f})")

        if confidence > 0.85:
            state["category"] = category
            state["confidence"] = confidence
            return state

        # fallback to LLM
        prompt = TriagePrompt.prompt_dumper(state)

        for _ in range(3):
            response = self.TRIAGE_LLM.generate_response(prompt)
            response_text = response.text

            valid, result = self.EVALUATOR.validate_response(response_text)

            if not valid:
                continue

            evaluation = self.EVALUATOR.evaluator(
                response_text,
                state
            )

            evaluation_data = json.loads(evaluation)

            if evaluation_data["approved"]:
                state["category"] = result["category"]
                state["confidence"] = result["confidence"]

                if state["category"] == "escalation":
                    state["escalation_reason"] = evaluation_data.get("reason")
                    state["escalation_summary"] = evaluation_data.get("summary")

                return state

        state["category"] = "escalation"
        state["escalation_required"] = True
        state["escalation_reason"] = "Unable to classify ticket"
        state["escalation_summary"] = "Both neural network and LLM classification failed"

        return state