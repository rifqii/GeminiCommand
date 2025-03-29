from dataclasses import dataclass, field
from ..Commands.Extractor import get_commands_as_text


@dataclass
class PromptConstructor:

    def __post_init__(self) -> None:
        pass

    def construct_prompt(self, prompt: str) -> str:
        prompt = f"""
        I have a user input (this might be transcribed, so it probably not perfect prompt, try to understand if the prompt doesn't makes sense with phonetically similar words or person if there is a person name specified.):
        {prompt}

        Can you choose the proper methods on this class to execute with this criteria?   
        1. omit the args if its not specified.
        2. User input might be comes from an audio transcriber, if the prompt doesn't makes sense, try to fix them by analyzing the common words where it phonetically similar
        3. Response should NOT exceeds 2000 characters!
        4. return None if you can't figure out the function.
        5. if params name is "ask_ai", please generate an answer based on the documentation on the respective method
        6. I need you to answer with only dictionary in format like this:

        {{
            "function_name": fn_name,
            "function_args": {{
                fn_args1: "args1 value",
                fn_args2: "args2 value"
            }}
        }}



        and here is the Commands class:
        {get_commands_as_text()}
        """

        return prompt
