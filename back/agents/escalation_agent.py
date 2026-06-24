# The system should determine whether the issue can be resolved automatically.
# Examples:
# Low confidence response
# Missing information
# Complex technical issue
# Account security concern
# If escalation is required:
# Route ticket to Escalation Agent
# Generate escalation notes
# Produce a summary for a human support representative (Sending it via email or Telegram is a plus )

from back.state import SupportState
from back.utils.tools.telegram_notifier import TelegramNotifier
class EsclationAgent:
    def __init__(self):
        self.telegram = (TelegramNotifier())

    def run(self, state: SupportState):

        summary = f"""
            🚨 Escalated Ticket

            Ticket:
            {state.get("ticket_id", "N/A")}

            Category:
            {state.get("category", "N/A")}

            Customer Issue:
            {state.get("message", "N/A")}

            AI Analysis:
            {state.get("agent_response", "No automated analysis available")}

            Escalation Reason:
            {state.get("escalation_reason", "Not specified")}
            
            Escalation Summary:
            {state.get("escalation_summary", "Not specified")}

            Recommended Action:
            Manual review required.
        """

        self.telegram.notify(summary)

        # state["escalation_summary"] = (summary)
        state["routing_path"].append("escalation_agent")
        state["tools_used"].append("telegram_notifier")
        
        return state