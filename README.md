# Speech Recognition and Text Comparison GUI

## List of contents
[Explanations](SpeechRecognitionandTextComparisonGUI) 
[About](AboutMyProject) 
[How to use](Howtouse) 
[Project files](Filesintheproject) 
[Requirements](Requirements) 
[Credits](Credits)

This program is a GUI application built using Python `tkinter` module, that allows the user to do speech recognition and text comparison. The user is required to paste their lecture text in the text box, and then click on "Recognize Speech" button and read the text. After reading the text, wait for a few seconds of silence to stop listening to the speech, and then the program will show the results.

The user can also load their audio file to compare it with the lecture text by clicking on the "Load your audio file that matches with your lecture" button. The program will create a new folder named "Corrections Audios" in the Documents folder by default to save audio files, but the user can select another folder to save audio files.

The program also supports multiple languages, including English and Spanish.

## About My Project
As a non-native English speaker, I found it challenging to improve my English pronunciation without having native speakers around me to practice with. So, I decided to create an app to help me with this task.

## How to use

1.  Clone the repository to your local machine.
2.  Open the command prompt and navigate to the project directory.
3.  Install the required modules by running `pip install -r requirements.txt` in the command prompt.
4.  Run the program by executing `python main.py` in the command prompt.
5.  Paste your lecture text in the text box provided.
6.  Click on the "Recognize Speech" button and read the text.
7.  Wait for a few seconds of silence to stop listening to the speech.
8.  The program will display the results.

## Files in the project

*   `gui.py`: The gui file that contains the GUI class.
*   `main.py`: The main is the one which runs the app.
*   `SpeechRecognition.py`: A module that provides the speech recognition functionality.
*   `TextToSpeech.py`: A module that provides the text to speech functionality.
*   `settings.json`: A JSON file that stores the program settings, including the directory where audio files are saved.
*   `requirements.txt`: A file that contains the required modules to run the program.

## Requirements

*   Python 3.x
*   tkinter
*   SpeechRecognition
*   pyaudio
*   TextBlob
*   googletrans==4.0.0-rc1
*   pathlib


## Credits
I developed this app on my own, using Python and several speech recognition and text-to-speech libraries. It was entirely a personal project, and no external contributions were made.
