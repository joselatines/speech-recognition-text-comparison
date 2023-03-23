from gtts import gTTS
import os
from src.utils import create_directory


class TextToSpeech:
    def __init__(self, lang="en"):
        self.lang = lang

    def convert_text_to_speech(self, text: str, save_path: str = "") -> None:
        """
        Convert text to speech and save the audio file.

        Args:
            text (str): The text to be converted to speech.
            save_path (str): The path where the audio file will be saved. If not provided, the default path is used.
        """
        # Set the default save path to the user's Speech Recognizer folder in Documents if none is provided
        if not save_path:
            save_path = os.path.join(
                os.path.expanduser("~/Documents/Speech Recognizer"),
                "Corrections Audios",
            )

        # Create the directory if it doesn't exist
        create_directory(save_path)

        # Construct the full file path
        file_name = f"{text.capitalize()}.mp3"
        file_path = os.path.join(save_path, file_name)

        # Check if the file already exists
        if os.path.exists(file_path):
            return

        # Initialize the gTTS API with the language
        tts = gTTS(text=text, lang=self.lang)

        # Save the audio file
        tts.save(file_path)
