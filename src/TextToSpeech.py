from gtts import gTTS
import os


class TextToSpeech:
    def __init__(self, lang="en"):
        self.lang = lang

    def convert_text_to_speech(self, text: str, save_path=""):
        # Set the default save path to the user's desktop directory if none is provided
        if not save_path:
            save_path = os.path.join(os.path.expanduser("~"), "Desktop")

        # Construct the full file path
        file_name = f"{text.capitalize()}.mp3"
        file_path = os.path.join(save_path, file_name)

        # Check if the file already exists
        if os.path.exists(file_path):
            # print(f"File {file_name} already exists, skipping...")
            return

        # Initialize the gTTS API with the language
        tts = gTTS(text=text, lang=self.lang)

        # Save the audio file
        tts.save(file_path)

        # Play the audio file
        # os.system("words/output.mp3")
