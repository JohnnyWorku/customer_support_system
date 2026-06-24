from back.state import SupportState

class TriagePrompt:
    def prompt_dumper(state: SupportState):
        json_format = """
            {
                "category": "<YOUR ANSWER>",
                "confidence": confidence must be a decimal number between 0 and 1,
                "reason": "<YOUR EVIDENCE, FOR CHOOSING THE CATEGORY AND SETTING THE CONFIDENCE, FROM THE MESSAGE>"
            }
        """
        
        prompt = f"""
            You are a support ticket classifier.

            Your task is to classify the customer's message into EXACTLY ONE category.

            Valid categories:

            * billing
            * technical_issue
            * feature_request
            * general_inquiry
            * account_management
            * escalation

            ---

            ## billing

            Use for:

            * Charges
            * Refunds
            * Payments
            * Invoices
            * Subscriptions
            * Pricing disputes

            Examples:

            ✓ "I was charged twice for my subscription."
            ✓ "My refund has not arrived."
            ✓ "Why was I billed after cancelling?"
            ✓ "My payment keeps failing."
            ✓ "Can I get an invoice for last month?"

            NOT billing:

            ✗ "I can't log in to my account." → account_management
            ✗ "The website crashes during checkout." → technical_issue
            ✗ "Can you add support for PayPal?" → feature_request

            ---

            ## technical_issue

            Use for:

            * Bugs
            * Errors
            * Crashes
            * Service outages
            * API failures
            * Features not working

            Examples:

            ✓ "The app crashes when I log in."
            ✓ "I get a 500 error."
            ✓ "File upload is not working."
            ✓ "The dashboard won't load."
            ✓ "The API returns an error."

            NOT technical_issue:

            ✗ "I forgot my password." → account_management
            ✗ "I want a dark mode feature." → feature_request
            ✗ "I was charged twice." → billing

            ---

            ## feature_request

            Use for:

            * New features
            * Product improvements
            * Enhancement requests

            Examples:

            ✓ "Please add dark mode."
            ✓ "Can you support PDF export?"
            ✓ "Please integrate with Slack."
            ✓ "I want scheduled reports."
            ✓ "Add two-factor authentication."

            NOT feature_request:

            ✗ "Dark mode is broken." → technical_issue
            ✗ "I can't access my account." → account_management
            ✗ "How does dark mode work?" → general_inquiry

            ---

            ## account_management

            Use for:

            * Login problems
            * Password resets
            * Account access
            * Profile updates
            * Permissions
            * Account deletion

            Examples:

            ✓ "I forgot my password."
            ✓ "Please delete my account."
            ✓ "I can't log in."
            ✓ "How do I change my email address?"
            ✓ "My account is locked."

            NOT account_management:

            ✗ "I was charged incorrectly." → billing
            ✗ "The login page crashes." → technical_issue
            ✗ "Can you add Google login?" → feature_request

            ---

            ## general_inquiry

            Use for:

            * Questions
            * Information requests
            * Documentation requests
            * Product understanding

            Examples:

            ✓ "How does your service work?"
            ✓ "Where can I find documentation?"
            ✓ "What plans do you offer?"
            ✓ "Do you support mobile devices?"
            ✓ "What features are included?"

            NOT general_inquiry:

            ✗ "Please add a new feature." → feature_request
            ✗ "The app crashes." → technical_issue
            ✗ "I forgot my password." → account_management

            ---

            ## escalation

            Use ONLY when:

            1. Human review is clearly required.
            2. The message is impossible to classify.
            3. The issue involves security, fraud, legal matters, or abuse.
            4. The message is too vague to route safely.

            Examples:

            ✓ "Someone hacked my account."
            ✓ "I found fraudulent transactions."
            ✓ "I am taking legal action."
            ✓ "An employee is harassing me."
            ✓ "Help."
            ✓ "Nothing works."
            ✓ "ajdhsjaj 7283 ???"

            NOT escalation:

            ✗ "I forgot my password." → account_management
            ✗ "I was charged twice." → billing
            ✗ "The app crashes." → technical_issue

            ---

            ## Special Rules

            If the customer reports:

            * Account takeover
            * Fraud
            * Security breach
            * Legal complaint
            * Threats
            * Harassment

            ALWAYS choose:

            "escalation"

            even if another category could apply.

            If the message is ambiguous:

            * Choose the closest category.
            * Reduce confidence.

            Examples:

            "I can't access my account."

            → account_management
            → confidence around 0.7–0.9

            "I need help."

            → escalation
            → confidence around 0.3–0.5

            ---

            ## Output Format

            Return ONLY valid JSON.

            {json_format}

            Requirements:

            * No markdown.
            * No backticks.
            * No extra text.
            * No explanations outside JSON.
            * Confidence must be between 0 and 1.
            * Category must exactly match one of the valid categories.
            - CAREFULLY THINK ON IT. BECAREFULL.

            Customer message:

            {state["message"]}
        """
        
        return prompt
        