

import json
from dataclasses import dataclass, field

@dataclass
class JSONLoader:
    json_path: str

    def __post_init__(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)  # Read existing JSON data
        except FileNotFoundError as e:
            print(f'JSONLoad:  {self.json_path} Error: {e}')
            self.data = {}  # Initialize with an empty dictionary if the file does not exist
        except json.JSONDecodeError as e:
            print(f'JSONLoad:  {self.json_path} Error: {e}.')
            self.data = {}  # Handle corrupted/empty JSON files
    
    def get(self) -> dict:
        return self.data

        