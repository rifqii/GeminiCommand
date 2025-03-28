
import argparse
import inspect
# from ..Discord.Webhook import DiscordWebhook
from src.api.Discord.Webhook import DiscordWebhook

class Commands:

    def __init__(self):
        pass
    
    """
    This method is for making coffee.
    """
    def make_coffee(self, cup_size: str ="L", coffee_type: str="Arabica"):
        print(f"Coffee {coffee_type} with {cup_size} Size is ready")


    def ask_discord_milosAI_qna(self, question: str, ask_ai:str):
        """
        method for sending message to discord using webhook
        params:
            question: question based on user input.
            ask_ai: 
                please generate this answer by you(AI), please make a humorous and comedic answer. 
                be straight forward and avoid over-analyzing / self-aware / self-explaining answer. 
                add some memes reference but not all, like from islamic/muslim meme, dota, twitch.tv meme, weebs, 
                genshin, marvel rivals, wuthering waves, and how Yusril always lying to the group.

                Here are discord group members:
                - Rifqi/Iking
                - Yusril
                - Rian/Ryan
                - Jordy / Jordoggy
                - Adi
                - Aldo / Aldoggy
                - Rudi / Rudy
        """

        message = f'''
        __**:kaaba:  AI-Milos  :kaaba:**__
        > **Question: **
        ```{question}```
        > **Answer by AI-Milos:**
        ```{ask_ai}```
        '''

        DiscordWebhook().post(message)
        return

def get_methods_and_args():
    """Dynamically extract methods and their arguments from Commands class."""
    commands = Commands()
    methods = {}
    
    for name, method in inspect.getmembers(commands, predicate=inspect.ismethod):
        if not name.startswith("__"):
            params = inspect.signature(method).parameters
            methods[name] = {param: details.default if details.default is not inspect.Parameter.empty else None
                             for param, details in params.items() if param != "self"}
    
    return methods

def main():
    methods = get_methods_and_args()

    parser = argparse.ArgumentParser(description="Execute Commands methods dynamically")
    parser.add_argument("method", type=str, choices=methods.keys(), help="Method to execute")
    
    # Dynamically add arguments based on the selected method
    args, unknown = parser.parse_known_args()
    method_name = args.method

    method_parser = argparse.ArgumentParser()
    
    for arg_name, default_value in methods[method_name].items():
        if isinstance(default_value, int):
            method_parser.add_argument(f"--{arg_name}", type=int, default=default_value, help=f"{arg_name} (default: {default_value})")
        else:
            method_parser.add_argument(f"--{arg_name}", type=str, default=default_value, help=f"{arg_name} (default: {default_value})")

    final_args = method_parser.parse_args(unknown)
    
    # Execute the selected method with extracted arguments
    commands = Commands()
    method = getattr(commands, method_name)
    method(**vars(final_args))

if __name__ == "__main__":
    main()