import speech_recognition as sr
import pyttsx3

TEXT = 1
SPEECH = 2
DYNAMIC = 3

def setup_text_to_speech():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    return engine



def text_to_speech(engine, text):
    engine.say(text)
    engine.runAndWait()



def speech_to_text(listen_text):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print(f"{listen_text}")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return ""



def choose_input_mode():
    print("Choose your input mode:")
    print("  1. Text Input")
    print("  2. Voice Input")

    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if choice == 1:
                return TEXT
            elif choice == 2:
                return SPEECH
            else:
                print("Invalid choice. Please select 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")



def set_default_or_dynamic():
    print("\nChoose whether to use a default interaction mode, or have the option to switch between text or voice input each time you make a new query:")
    print("  1. Set a Default Input")
    print("  2. Choose a Different Input for Each Query")

    while True:
        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if choice == 1:
                return choose_input_mode()
            elif choice == 2:
                return DYNAMIC
            else:
                print("Invalid choice. Please select 1 or 2.")
        except ValueError:
            print("Please enter a valid number.")