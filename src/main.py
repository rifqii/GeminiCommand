
# from src import GenAI, Commands, get_commands_as_text, PromptConstructor, MyListener, AudioRecorder, run_command
from src import GenAI, PromptConstructor, run_command, AudioRecorder
import json


# def main():

#     while True:
#         # user_input = "ask milos, can we agree Yusril is a scammer ?"
#         user_input: str = input("insert command prompt\n")

#         if user_input.lower() == "n":
#             return

#         prompt = PromptConstructor(user_input).construct_prompt()

#         response = GenAI(prompt).get_answer
#         with open('response.json','w', encoding='utf-8') as file:
#             json.dump(response, file, indent=4)

#         if response:
#             run_command(response['function_name'], **response['function_args'])

def main():
    model = 'gemini-2.0-flash'
    prompt_constructor = PromptConstructor()

    while True:
        user_input = input("Choose AI Input Mode: (mic(m) / typing(t)) \n")
        if user_input.lower() in ['mic', 'typing','m', 't', '1','2']:
            break

    if user_input.lower() in ['mic','m','1']:
        while True:
            lang_input = input(f"choose audio transcriber language: (en/id) \n")
            if lang_input.lower() in ['en', 'id','1','2']:
                if lang_input.lower() in ['1','2']:
                    if int(lang_input) == 1:
                        lang_input = 'en'
                    elif int(lang_input) == 2:
                        lang_input = 'id'

                break
            print(f"Language {lang_input} is not supported, try again")

        AudioRecorder(gemini_model=model, language=lang_input)

    elif user_input.lower() in ['typing','t','2']:
        gen_AI = GenAI('gemini-2.0-flash')
        while True:
            if user_input := input("Type prompt to generate: \n"):
                prompt = prompt_constructor.construct_prompt(user_input)
                if response := gen_AI.get_answer(prompt):
                    run_command(response['function_name'], **response['function_args'])
                else:
                    print("Command unrecognizable.")
            else:
                print("blank input. Try again")
                    




if __name__ == "__main__":
    main()
