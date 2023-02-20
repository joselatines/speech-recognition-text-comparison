from SpeechRecognition import SpeechRecognition
from TextToSpeech import TextToSpeech


def main():
    speech_recognizer = SpeechRecognition()
    text_to_speech = TextToSpeech()

    text_guide = str(input("Paste your lecture text: "))
    user_voice_text = speech_recognizer.recognize_speech()

    if user_voice_text:
        texts_cleaned = [
            speech_recognizer.clean_string(text)
            for text in [user_voice_text, text_guide]
        ]
        differ_words = speech_recognizer.compare_texts(
            texts_cleaned[0], texts_cleaned[1]
        )

        if len(differ_words) > 0:
            print("You have a few pronunciation mistakes")
            for word in differ_words:
                print(f"You pronounced '{word[0]}' instead of '{word[1]}'")
                text_to_speech.convert_text_to_speech(word[1])
                print(
                    f"You can listen to the right pronunciation of '{word[1]}' in the 'words' folder"
                )


if __name__ == "__main__":
    main()
