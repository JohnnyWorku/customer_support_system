import os

import requests
from dotenv import load_dotenv


load_dotenv()


class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        
    def notify(self, text):
        url = (
            f"https://api.telegram.org/bot"
            f"{self.bot_token}/sendMessage"
        )
        
        payload = {
            "chat_id": self.chat_id,
            "text": text
        }
        
        response = requests.post(
            url,
            json=payload
        )

        return response.json()
        
