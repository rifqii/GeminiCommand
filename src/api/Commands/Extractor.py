import inspect
from .Commands import Commands

def get_commands_as_text() -> str:
    """Return the Commands class and get_methods_and_args function as raw text."""
    class_text = inspect.getsource(Commands)
    return f"{class_text}\n"


# def get_methods_and_args():
#     """Dynamically extract methods and their arguments from Commands class."""
#     commands = Commands()
#     methods = {}
    
#     for name, method in inspect.getmembers(commands, predicate=inspect.ismethod):
#         if not name.startswith("__"):
#             params = inspect.signature(method).parameters
#             methods[name] = {param: details.default if details.default is not inspect.Parameter.empty else None
#                              for param, details in params.items() if param != "self"}
    
#     return methods

# Example Usage:
if __name__ == "__main__":
    print(get_commands_as_text())