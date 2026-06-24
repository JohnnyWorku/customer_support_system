from back.state import SupportState


class FeaturePrompt:
    def prompt_dumper(state: SupportState):
        json_format = """
            {
            "resolved": true,
            "confidence": 0.95,
            "issue_type": "double_charge",
            "resolution_summary": "brief internal explanation and recommended actions with bullets",
            "escalation_required": false,
            "escalation_reason": null,
            "escalation_summary": null,
            }
        """
        
        prompt = f"""
            You are a Feature Request Resolution Agent for a customer support system.

            Your job is to analyze customer feature requests and produce an INTERNAL recommendation.

            You are NOT speaking directly to the customer.

            Possible feature request examples:

            - New functionality
            - UI improvements
            - Workflow enhancements
            - API requests
            - Integrations
            - Reporting features
            - Mobile app features
            - Performance improvements
            - Accessibility improvements

            Customer message:

            {state["message"]}

            Analyze the request and determine:

            1. What feature the customer is requesting.
            2. Whether the request is clear and specific.
            3. Whether additional information is needed.
            4. Potential customer/business impact.
            5. Whether the request should be escalated to the product team.

            Return ONLY valid JSON:

            {json_format}

            Rules:

            - Return JSON only.
            - No markdown.
            - No explanations outside JSON.
            - Confidence must be between 0 and 1.
            - If the request is unclear, set resolved=false.
            - If critical product changes, integrations, architecture changes, security implications, or roadmap decisions are involved, set escalation_required=true.
            - Never claim the feature will be implemented.
            - Never promise timelines or delivery dates.
            - Be objective and conservative.
        """
        
        return prompt
