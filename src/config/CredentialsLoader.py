
from dataclasses import dataclass, field
from ..utils.JSONLoader import JSONLoader


@dataclass
class CredentialsLoader:

    def __post_init__(self):
        self.genai = JSONLoader('credentials/genai.json').get()
