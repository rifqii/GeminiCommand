
from dataclasses import dataclass, field
from ...utils.JSONLoader import JSONLoader
import requests


@dataclass
class DiscordWebhook:
    
    def __post_init__(self):
        self.webhook_url = JSONLoader(
            "credentials/test_discord_webhook.json").get().get('HOOK_URL', None)


    def post(self, message: str):
        data = {
            "content": message
        }

        response = requests.post(self.webhook_url, json=data)
        if response.status_code == 204:
            print("Message sent successfully!")
        else:
            print(
                f"Failed to send message: {response.status_code}, {response.text}")
