from langgraph.graph import StateGraph, END

# state
from state import SupportState

# agents
from agents.account_management_resolution_agent import AccountManagementResolutionAgent
from agents.billing_resolution_agent import BillingResolutionAgent
from agents.escalation_agent import EsclationAgent
from agents.feature_request_agent import FeatureRequestAgent
from agents.knowledge_agent import KnowledgeAgent
from agents.response_agent import ResponseAgent
from agents.technical_resolution_agent import TechnicalAgent
from agents.triage_agent import TriageAgent


# Instantiating agents
account_agent = AccountManagementResolutionAgent()
billing_agent = BillingResolutionAgent()
escalation_agent = EsclationAgent()
feature_agent = FeatureRequestAgent()
knowledge_agent = KnowledgeAgent()
response_agent = ResponseAgent()
technical_agent = TechnicalAgent()
triage_agent = TriageAgent()


workflow = StateGraph(SupportState)

# adding nodes to the graph
workflow.add_node("account_agent", account_agent.run)

workflow.add_node("billing_agent", billing_agent.run)

workflow.add_node("escalation_agent", escalation_agent.run)

workflow.add_node("feature_agent", feature_agent.run)

workflow.add_node("knowledge_agent", knowledge_agent.run)

workflow.add_node("response_agent", response_agent.run)

workflow.add_node("technical_agent", technical_agent.run)

workflow.add_node("ticket_intake", triage_agent.intake_node)
workflow.add_node("triage", triage_agent.classify)

# Entry point
workflow.set_entry_point("ticket_intake")

# Edges
workflow.add_edge("ticket_intake", "triage")
