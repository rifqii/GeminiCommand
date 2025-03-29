
from dataclasses import dataclass, field

from src.config.CredentialsLoader import CredentialsLoader

from google import genai
from google.genai.types import GenerateContentResponse
import json

from .PromptConstructor import PromptConstructor


@dataclass
class GenAI:
    model: str = 'gemini-2.0-flash'

    def __post_init__(self):
        self.credentials = CredentialsLoader()
        self.client = genai.Client(api_key=self.credentials.genai['API_KEY'])
        self.prompt_constructor = PromptConstructor()
        # self.post(self.prompt)

    def post(self, prompt: str) -> GenerateContentResponse:

        self.response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
    

    @property
    def get_response(self) -> GenerateContentResponse:
        return self.response
    
    def get_answer(self, prompt: str) -> dict:
        prompt = self.prompt_constructor.construct_prompt(prompt)
        self.post(prompt)
        return self.sanitize_answer(self.response.text) 

    @staticmethod
    def sanitize_answer(response: str) -> dict:
        """
        Sanitize AI response and return a dictionary.
        Handles responses with triple backticks and JSON formatting.

        :param response: AI response as a string.
        :return: Parsed dictionary or an empty dict if invalid.
        """
        try:
            # Remove triple backticks
            response = response.replace('```json', '').replace('```', '').strip()

            # Attempt to parse the JSON
            return json.loads(response)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error parsing AI response: {e}")
            return {}