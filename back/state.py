from typing import TypedDict, Optional, List

class SupportState(TypedDict, total=False):
    ticket_id: str
    customer_id: str
    message: str
    
    category: Optional[str]
    agent_response: Optional[str]
    confidence: Optional[float]
    escalation_required: bool
    escalation_reason: Optional[str]
    escalation_summary: Optional[str]
    tools_used: List[str]
    routing_path: List[str]
    generated_response: Optional[str]
    final_response: Optional[str]
    