import tkinter as tk
from tkinter import messagebox, filedialog
from src.SpeechRecognition import SpeechRecognition
from src.TextToSpeech import TextToSpeech
import os
from src.utils import create_directory
import json


class SpeechGUI:
    blue = "#3392FF"
    purple = "#8B1EE5"
    yellow = "#3392FF"
    white = "#fff"

    def __init__(self, master):
        # master -> root
        self.master = master
        master.title("Speech Recognition and Text Comparison")

        self.speech_recognizer = SpeechRecognition()
        self.text_to_speech = TextToSpeech()
        self.user_voice_text = ""
        self.audio_file_speaking = None
        self.settings = self.load_settings()
        self.language = "en"
        self.lecture_file_loaded = None

        """   # Instructions
        self.display_instructions_widget() """

        self.create_text_guide_widget(master)

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

        if self.audio_file_speaking:
            self.button_reset_audio = tk.Button(
                master,
                text="Reset audio file",
                command=self.reset_audio_file,
                bg=self.yellow,
            )
            self.button_reset_audio.pack()
            self.master.update()

        # Create label widget for output
        self.label_output = tk.Label(master, text="")
        self.label_output.pack()

        # Create a menu bar
        menu_bar = tk.Menu(master)
        master.config(menu=menu_bar)

        # create file menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(
            label="Select directory to save corrections",
            command=self.select_audio_folder,
        )

        # create the language menu
        language_menu = tk.Menu(menu_bar, tearoff=0)
        language_menu.add_command(label="English", command=self.set_english_language)
        language_menu.add_command(label="Spanish", command=self.set_spanish_language)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.exit_program)

        # instructions menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(
            label="Instructions", command=self.display_instructions_widget
        )

        # add menus to menu bar
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Config", menu=edit_menu)
        menu_bar.add_cascade(label="Language", menu=language_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # configure root window with menu bar
        master.config(menu=menu_bar)

    @staticmethod
    def save_settings(settings):
        # Create Speech Recognizer folder in documents user folder
        folder_path = os.path.join(
            os.path.expanduser("~"), "Documents", "Speech Recognizer"
        )
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save the settings to the settings file
        settings_file = os.path.join(folder_path, "settings.json")
        with open(settings_file, "w") as f:
            json.dump(settings, f)

    @staticmethod
    def load_settings():
        """
        Load the user settings from the settings file.
        """
        documents_folder = os.path.expanduser("~/Documents")
        settings_folder = os.path.join(documents_folder, "Speech Recognizer")
        settings_file = os.path.join(settings_folder, "settings.json")

        # Create the settings folder if it doesn't exist
        create_directory(settings_folder)

        if not os.path.exists(settings_file):
            default_settings = {
                "corrections_audio_path": os.path.join(
                    settings_folder, "Corrections Audios"
                )
            }
            with open(settings_file, "w") as f:
                json.dump(default_settings, f, indent=4)

        with open(settings_file) as f:
            settings = json.load(f)
        return settings

    def exit_program(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.master.destroy()

    def load_lecture_file(self):
        filename = filedialog.askopenfilename(filetypes=(("text files", "txt"),))
        if filename:
            self.lecture_file_loaded = filename
            messagebox.showinfo(
                "File uploaded", "Your lecture was uploaded successfully"
            )
            self.create_text_guide_widget(self.master)
        else:
            messagebox.showerror(
                "File uploaded", "Your lecture was not uploaded successfully"
            )
        self.master.update()
        return filename

    def create_text_guide_widget(self, master):
        if self.lecture_file_loaded is None:
            # Create label and entry widgets for lecture text
            self.label_text_guide = tk.Label(master, text="Paste your lecture text:")
            self.label_text_guide.pack()
            self.entry_lecture = tk.Entry(master, width=50)
            self.entry_lecture.pack()

            or_label = tk.Label(text="Or")
            or_label.pack()
            self.button_load_lecture = tk.Button(
                master,
                text="Upload your lecture",
                bg=self.blue,
                fg=self.white,
                command=self.load_lecture_file,
            )
            self.button_load_lecture.pack()
        else:
            tk.Label(master, text=self.lecture_file_loaded).pack()

    def display_instructions_widget(self):
        # Instructions
        instructions = {
            "en": {
                "title": "Instructions",
                "content": """ 
                1. Paste your lecture 
                2. Press Recognize Speech and read the text 
                3. After read the text make a silence for a few seconds to stop listen to you 
                4. Wait your results 
                """,
            },
            "es": {
                "title": "Instrucciones",
                "content": """
                1. Pega tu lectura 
                2. Presiona "Recognize Speech" y lee tu texto
                3. Luego de leer el texto haz silencio para parar de escuchar
                4. Espera los resultados
                """,
            },
        }

        if self.language in instructions:
            messagebox.showinfo(
                title="None", message=instructions[self.language]["content"]
            )

        else:
            # Handle the case where the selected language is not available
            tk.Label(self.master, text="Selected language is not available.").pack()

        self.master.update()

    def set_english_language(self):
        self.language = "en"
        self.display_instructions_widget()

    def set_spanish_language(self):
        self.language = "es"
        self.display_instructions_widget()

    def select_audio_folder(self):
        # Ask the user for a directory to save files
        audio_path_output = filedialog.askdirectory()

        # Check if the user selected a directory
        if audio_path_output:
            # Save the directory path in the settings file
            self.settings["corrections_audio_path"] = audio_path_output
            self.save_settings(self.settings)

            # Show a success message
            messagebox.showinfo("Success", f"Audio folder set to:\n{audio_path_output}")
            self.master.update()
        else:
            settings = self.settings
            self.label_output.config(
                text=f"Your corrections are saving in: {settings['corrections_audio_path']}"
            )
            # Show a message if the user didn't select a directory
            messagebox.showerror("Error", "No audio folder selected")

    def recognize_speech(self):
        if self.entry_lecture.get() or self.load_lecture_file:
            waiting_message = (
                "🗣️ Listening your audio, please wait"
                if self.audio_file_speaking
                else '"🗣️ Listening... Please speak"'
            )
            while True:
                try:
                    self.label_output.config(text=waiting_message)
                    self.master.update()  # update the GUI to show the label change

                    user_voice_text = self.speech_recognizer.recognize_speech(
                        self.audio_file_speaking
                    )
                except:
                    messagebox.showerror(
                        "Error type", "Please upload a audio file with extension .wav"
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

    def reset_audio_file(self):
        self.audio_file_speaking = None
        messagebox.showinfo(
            "Audio file",
            "Last audio file deleted, speak to the app or update a new one file",
        )

    def load_audio_speaking(self):
        # Specify the file types
        filetypes = (("Audio Files", ".wav .ogg"), ("All Files", "*.*"))

        # Show the open file dialog by specifying path
        path = filedialog.askopenfile(filetypes=filetypes)

        if path:
            self.audio_file_speaking = path.name
            self.label_output.config(text="Audio updated")
        else:
            self.label_output.config(text="Audio not updated")
        return path

    def compare_texts(self):
        text_guide = ""

        if self.lecture_file_loaded:
            with open(self.lecture_file_loaded) as f:
                text_guide = f.read()
        else:
            text_guide = self.entry_lecture.get()

        print(text_guide)

        if self.user_voice_text and text_guide:
            texts_cleaned = [
                self.speech_recognizer.clean_string(text)
                for text in [self.user_voice_text, text_guide]
            ]

            differ_words = self.speech_recognizer.compare_texts(
                texts_cleaned[0], texts_cleaned[1]
            )

            if len(differ_words) > 0:
                save_path = self.settings["corrections_audio_path"]

                for word in differ_words:
                    self.text_to_speech.convert_text_to_speech(word[1], save_path)

                # write the recognized lecture to a txt file
                self.speech_recognizer.write_string_to_file(
                    self.user_voice_text, save_path
                )
                # write the lecture to a txt file
                self.speech_recognizer.write_string_to_file(
                    text_guide, save_path, lecture=True
                )

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
