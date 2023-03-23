import speech_recognition as sr
import os
import re


class SpeechRecognition:
    allowed_audio_extensions = [".wav", ".aiff", ".flac", ".mp3"]

    def __init__(self):
        self.recognizer = sr.Recognizer()

    @staticmethod
    def write_string_to_file(string, save_path, lecture=False):
        path = (
            f"{save_path}/your_lecture.txt"
            if lecture
            else f"{save_path}/audio_recognized.txt"
        )
        with open(path, "w") as file:
            file.write(string)

    def recognize_speech(self, audio_file=None):
        if audio_file:
            extension = os.path.splitext(audio_file)[1]

            if extension in self.allowed_audio_extensions:
                print("I am listen your audio, please wait...")
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
            else:
                print("Format invalid, please use this format files: WAV, AIFF, FLAC")
                return False

        else:
            with sr.Microphone() as source:
                print("Speak now!")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source)
                # Listen for audio input
                audio = self.recognizer.listen(source)

                if audio:
                    print("I am listening...")

        try:
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            return text

        except sr.UnknownValueError:
            print("Oops! Didn't catch that.")

        except sr.RequestError as e:
            print(
                f"Uh oh! Couldn't request results from Google Speech Recognition service: {e}"
            )

    @staticmethod
    def clean_string(text):
        # Remove all characters except letters and numbers using regular expressions
        cleaned_text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

        # Convert the cleaned text to uppercase
        cleaned_text = cleaned_text.upper()

        return cleaned_text

    @staticmethod
    def compare_texts(voice_text, text_guide):
        differ_words = []

        # Split the strings into words
        voice_words = voice_text.split()
        guide_words = text_guide.split()

        # Compare the words
        for i, (voice_word, guide_word) in enumerate(zip(voice_words, guide_words)):
            if voice_word != guide_word:
                differ_words.append((voice_word, guide_word))

        if len(differ_words) > 0:
            pass
            # print("Texts are not identical")
        else:
            pass
            # print("Strings are identical")

        return differ_words
