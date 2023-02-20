import tkinter as tk
from tkinter import messagebox, filedialog
from src.SpeechRecognition import SpeechRecognition
from src.TextToSpeech import TextToSpeech
import json
import os


class SpeechGUI:
    blue = "#3392FF"
    purple = "#8B1EE5"
    yellow = "#3392FF"
    white = "#fff"

    def __init__(self, master):
        self.master = master
        master.title("Speech Recognition and Text Comparison")

        self.speech_recognizer = SpeechRecognition()
        self.text_to_speech = TextToSpeech()
        self.user_voice_text = ""
        self.audio_file_speaking = None

        # Instructions
        instructions = [
            "INSTRUCTIONS:",
            "1. Paste your lecture",
            '2. Press "Recognize Speech" and read the text',
            "3. After read the text make a silence for a few seconds to stop listen to you",
            '4. Press "Compare Texts" to see your results',
        ]
        for instruction in instructions:
            tk.Label(master, text=instruction).pack()

        # Create label and entry widgets for lecture text
        self.label_text_guide = tk.Label(master, text="Paste your lecture text:")
        self.label_text_guide.pack()
        self.entry_lecture = tk.Entry(master, width=50)
        self.entry_lecture.pack()

        # Create buttons for speech recognition and text comparison
        self.button_recognize_speech = tk.Button(
            master,
            text="Recognize Speech",
            bg=self.blue,
            fg=self.white,
            command=self.recognize_speech,
        )
        self.button_recognize_speech.pack()
        self.button_recognize_speech_audio_file = tk.Button(
            master,
            text="Load your audio file that matches with your lecture",
            command=self.load_audio_speaking,
            bg=self.purple,
            fg=self.white,
        )
        self.button_recognize_speech_audio_file.pack()

        # Create label widget for output
        self.label_output = tk.Label(master, text="")
        self.label_output.pack()

        # Create a menu bar
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # create file menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(
            label="Select directory to save corrections",
            command=self.select_audio_folder,
        )

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.exit_program)

        # add file menu to menu bar
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # configure root window with menu bar
        root.config(menu=menu_bar)

    def exit_program(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            root.destroy()

    def select_audio_folder(self):
        # Load the settings file, or create a new one if it doesn't exist
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
        except FileNotFoundError:
            settings = {}

        # Ask the user for a directory to save files
        audio_path_output = filedialog.askdirectory()

        # Check if the user selected a directory
        if audio_path_output:
            # Save the directory path in the settings file
            settings["audio_path"] = audio_path_output
            with open("settings.json", "w") as f:
                json.dump(settings, f)

            # Show a success message
            messagebox.showinfo("Success", f"Audio folder set to:\n{audio_path_output}")
        else:
            # Show a message if the user didn't select a directory
            messagebox.showerror("Error", "No audio folder selected")

    def recognize_speech(self):
        if self.entry_lecture.get():
            while True:
                self.label_output.config(text="🗣️ Listening... Please speak.")
                self.master.update()  # update the GUI to show the label change

                user_voice_text = self.speech_recognizer.recognize_speech(
                    self.audio_file_speaking
                )
                if user_voice_text:
                    self.label_output.config(text="✅ Speech recognized successfully.")
                    self.user_voice_text = user_voice_text
                    break
                else:
                    self.label_output.config(
                        text="❌ Speech recognition failed. Please speak again."
                    )

                    # messagebox.showinfo(title='Notification', message='Speech recognition failed. Please speak again.')
                    listening = messagebox.askretrycancel(
                        title="❌ Speech Recognition Error",
                        message="Sorry, I couldn't recognize your speech. Please speak clearly and make sure your microphone is working properly.",
                    )

                    print(listening)
                    if listening == False:
                        self.label_output.config(text="")
                        self.master.update()  # update the GUI to show the label change
                        break

            self.compare_texts()
        else:
            messagebox.showerror(
                title="❌ Error",
                message="Please enter lecture text and recognize speech first.",
            )

    def load_audio_speaking(self):
        # Specify the file types
        filetypes = (("Audio Files", ".wav .ogg .mp3"), ("All Files", "*.*"))

        # Show the open file dialog by specifying path
        path = filedialog.askopenfile(filetypes=filetypes)

        self.audio_file_speaking = path.name
        self.label_output.config(text="Audio updated")
        return path

    def compare_texts(self):
        text_guide = self.entry_lecture.get()

        if self.user_voice_text and text_guide:
            texts_cleaned = [
                self.speech_recognizer.clean_string(text)
                for text in [self.user_voice_text, text_guide]
            ]

            differ_words = self.speech_recognizer.compare_texts(
                texts_cleaned[0], texts_cleaned[1]
            )

            if len(differ_words) > 0:
                save_path = ""
                try:
                    with open("settings.json", "r") as f:
                        settings = json.load(f)
                        save_path = settings["audio_path"]
                except FileNotFoundError:
                    settings = {}
                    save_path = os.path.join(os.path.expanduser("~"), "Desktop")

                for word in differ_words:
                    self.text_to_speech.convert_text_to_speech(word[1], save_path)

                self.show_pronunciation_feedback(differ_words)
                self.label_output.config(
                    text=f"🔈 You can listen to the right pronunciations at {save_path}"
                )

            else:
                messagebox.showinfo(
                    title="🥳 Congratulations!",
                    message="Your speech matches lecture text exactly.",
                )
        else:
            messagebox.showerror(
                title="❌ Error",
                message="Please enter lecture text and recognize speech first.",
            )

    def show_pronunciation_feedback(self, differ_words):
        # Create a list of messages to display
        messages = [
            f"You pronounced '{word[0]}' instead of '{word[1]}'."
            for word in differ_words
        ]

        # Combine the messages into a single string
        message_text = "\n".join(messages)

        # Display the message using messagebox.showinfo
        messagebox.showinfo("📚 Pronunciation Feedback", message_text)


if __name__ == "__main__":
    root = tk.Tk()
    my_gui = SpeechGUI(root)
    root.mainloop()
