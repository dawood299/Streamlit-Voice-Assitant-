import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser

listener = sr.Recognizer()
engine = pyttsx3.init()

# Setup voice for speech
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ''
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)  # Adjust once for ambient noise
            print('Listening...')
            voice = listener.listen(source)  # Remove timeout and phrase_time_limit
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'emma' in command:
                command = command.replace('emma', '').strip()
                print(f"Command received: {command}")
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError:
        print("Sorry, there's an issue with the speech recognition service.")
    return command

def run_emma():
    command = take_command()
    if command:
        if 'play' in command:
            song = command.replace('play', '').strip()
            talk(f'Playing {song}')
            pywhatkit.playonyt(song)
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f'Current time is {current_time}')
        elif 'who is' in command:
            person = command.replace('who is', '').strip()
            try:
                info = wikipedia.summary(person, 1)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError:
                talk("There are multiple results for that query. Please be more specific.")
            except wikipedia.exceptions.PageError:
                talk("I couldn't find any information on that topic.")
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        elif 'open' in command:
            website = command.replace('open', '').strip()
            url = f"https://{website}" if not website.startswith('http') else website
            talk(f'Opening {website}')
            webbrowser.open(url)
        elif 'search for' in command:
            search_query = command.replace('search for', '').strip()
            url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            talk(f'Searching for {search_query} on Google')
            webbrowser.open(url)
        elif 'what is' in command:
            search = command.replace('what is', '').strip()
            try:
                info = wikipedia.summary(search, 1)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError:
                talk("There are multiple results for that query. Please be more specific.")
            except wikipedia.exceptions.PageError:
                talk("I couldn't find any information on that topic.")
        else:
            talk('Please say the command again.')
    else:
        talk('I did not hear any command. Please try again.')

while True:
    run_emma()

