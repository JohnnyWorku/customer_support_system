from back.state import SupportState


class TraigeEvaluatorPrompt:
    def prompt_dumper(response, state: SupportState):
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
            {state["message"]}

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
        
        return review_prompt
