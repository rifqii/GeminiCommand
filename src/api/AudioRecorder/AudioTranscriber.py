import time
import pynput
import audiomath as am
import whisper
import json

from ..genai.PromptConstructor import PromptConstructor
from ..genai.GenAI import GenAI
from ..Commands.Executor import run_command
from dataclasses import dataclass, field


@dataclass
class AudioRecorder:
    gemini_model: str
    buffer_length_seconds: float = 20
    model_size: str = 'base'
    language: str ='en'

    def __post_init__(self):
        """
        Initialize AudioRecorder
        
        :param gemini_model: default= gemini-2.0-flash
        :param buffer_length_seconds: Length of audio buffer
        :param model_size: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        :param language: Language code for transcription (e.g., 'en', 'es', 'fr', 'de')
        """
        # Initialize Whisper model with specified size
        self.whisper_model = whisper.load_model(self.model_size)
        self.gen_AI = GenAI(model=self.gemini_model)
        
        
        # Tracking recording state
        self.key_pressed = False
        self.transcriptions = []
        
        # Create a new buffer and recorder method
        self.create_new_buffer()
        self.initialize()

    def create_new_buffer(self):
        """
        Create a fresh audio buffer and recorder
        Ensures each recording starts from a clean slate
        """
        # Create new Sound buffer
        self.buffer = am.Sound(
            self.buffer_length_seconds, 
            nChannels=2,   # Stereo audio
            fs=44100       # Sample rate (44.1 kHz)
        )
        
        # Create new Recorder with the fresh buffer
        self.recorder = am.Recorder(
            self.buffer,   
            loop=True,     # Continuously overwrite oldest audio
            recording=False
        )

    def transcribe_audio(self):
        """
        Transcribe the audio buffer using Whisper
        
        Returns:
        - Transcription text
        - Detected language
        """
        try:
            # Convert AudioMath Sound to a temporary WAV file
            temp_wav = "assets/temp/temp_recording.wav"
            self.buffer.Write(temp_wav)
            
            # Transcribe using Whisper with specified language
            result = self.whisper_model.transcribe(
                temp_wav, 
                language=self.language,  # Specify language
                fp16=False  # Ensure compatibility with different systems
            )
            
            return {
                "text": result["text"],
                "language": result["language"],
                "confidence": result.get("confidence", None)
            }
        except Exception as e:
            print(f"Transcription error: {e}")
            return None

    def initialize(self):
        # Create keyboard listener for recording
        # Example: Spanish language, base model
        # recorder = AudioRecorder(language="en")
        
        def on_press(key):
            try:
                # if key.char == 'r' and not self.key_pressed:
                if key == pynput.keyboard.Key.shift_r and not self.key_pressed:
                    # Create a new buffer each time recording starts
                    self.create_new_buffer()
                    
                    print('Recording started...')
                    self.recorder.Record()
                    self.key_pressed = True
            except AttributeError:
                pass

        def on_release(key):
            try:
                if key == pynput.keyboard.Key.shift_r and self.key_pressed:
                    print('Recording stopped.')
                    self.recorder.Stop()
                    
                    # Attempt transcription
                    transcription = self.transcribe_audio()
                    if transcription:
                        print("\n--- Transcription ---")
                        print(f"Text: {transcription['text']}")
                        print(f"Language: {transcription['language']}")

                        if response := self.gen_AI.get_answer(prompt= transcription['text']):
                            run_command(response['function_name'], **response['function_args'])
                        else:
                            print("Unrecognizable command.")

                    else:
                        print('Whisper: no sound detected')
                    
                    self.key_pressed = False

            except AttributeError:
                pass

        # Set up listener
        with pynput.keyboard.Listener(on_press=on_press, on_release=on_release):
            print("Press 'shift_right' to start/stop recording. Press Ctrl+C to exit.")
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\nExiting...")

    def get_answer(self, prompt):
        if not prompt:
            print("No Prompt inputted.")
            return 
        prompt = PromptConstructor().construct_prompt(prompt)
        print(prompt)
        
        # response = GenAI(model= self.gemini_model).get_answer(prompt)

        # with open('response.json', 'w', encoding='utf-8') as file:
        #     json.dump(response, file, indent=4)
        # if response:
        #     run_command(response['function_name'], **response['function_args'])

        # else:
        #     print('unrecognized command please reenter another prompt')

def main():
    # Create keyboard listener for recording
    # Example: Spanish language, base model
    recorder = AudioRecorder(language="en")
    
    def on_press(key):
        try:
            if key.char == 'r' and not recorder.key_pressed:
                # Create a new buffer each time recording starts
                recorder.create_new_buffer()
                
                print('Recording started...')
                recorder.recorder.Record()
                recorder.key_pressed = True
        except AttributeError:
            pass

    def on_release(key):
        try:
            if key.char == 'r' and recorder.key_pressed:
                print('Recording stopped.')
                recorder.recorder.Stop()
                
                # Attempt transcription
                transcription = recorder.transcribe_audio()
                if transcription:
                    print("\n--- Transcription ---")
                    print(f"Text: {transcription['text']}")
                    print(f"Language: {transcription['language']}")
                    get_answer(transcription['text'])


                
                else:
                    print('no sound')
                
                recorder.key_pressed = False

        except AttributeError:
            pass
    

    def get_answer(prompt):
        prompt = PromptConstructor(prompt)

        response = GenAI('gemini-2.0-flash').get_answer(prompt)
        with open('response.json', 'w', encoding='utf-8') as file:
            json.dump(response, file, indent=4)

        if response:
            run_command(response['function_name'], **response['function_args'])

        else:
            print('unrecognized command please reenter another prompt')

    # Set up listener
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release):
        print("Press 'r' to start/stop recording. Press Ctrl+C to exit.")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nExiting...")

if __name__ == "__main__":
    main()