import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import whisper
import streamlit as st

# Initialize the speech engine
engine = pyttsx3.init()

# Setup voice for speech
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

def talk(text):
    """Function to make the assistant speak."""
    engine.say(text)
    engine.runAndWait()

def transcribe_audio():
    """Function to transcribe audio using Whisper."""
    model = whisper.load_model("base")  # You can choose other models: tiny, small, medium, large
    st.write("Please speak into your microphone...")
    
    # Using Streamlit's audio uploader
    audio_file = st.file_uploader("Upload your audio file", type=["mp3", "wav"])
    if audio_file is not None:
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_file.read())
        # Transcribe the audio
        result = model.transcribe("temp_audio.wav")
        return result["text"].strip()
    return ""

def run_emma(command):
    """Main function to process the command."""
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)
        st.write(f'Playing {song} on YouTube...')
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {current_time}')
        st.write(f'Current time is {current_time}')
    elif 'who is' in command or 'what is' in command:
        topic = command.replace('who is', '').replace('what is', '').strip()
        try:
            info = wikipedia.summary(topic, 1)
            talk(info)
            st.write(f'Info: {info}')
        except wikipedia.exceptions.DisambiguationError:
            talk("There are multiple results for that query. Please be more specific.")
            st.write("Multiple results found, please be more specific.")
        except wikipedia.exceptions.PageError:
            talk("I couldn't find any information on that topic.")
            st.write("Couldn't find any information.")
        except Exception as e:
            talk("There was an error retrieving information.")
            st.write(f"Error: {str(e)}")
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)
        st.write(f'Joke: {joke}')
    elif 'open' in command:
        website = command.replace('open', '').strip()
        url = f"https://{website}" if not website.startswith('http') else website
        talk(f'Opening {website}')
        webbrowser.open(url)
        st.write(f'Opening {website}')
    elif 'search for' in command:
        search_query = command.replace('search for', '').strip()
        url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        talk(f'Searching for {search_query} on Google')
        webbrowser.open(url)
        st.write(f'Searching for {search_query} on Google...')
    elif 'calculate' in command:
        expression = command.replace('calculate', '').strip()
        try:
            result = eval(expression)  # Basic eval for calculation, ensure safety if using in production
            talk(f'The result is {result}')
            st.write(f'Result: {result}')
        except Exception as e:
            talk("There was an error calculating the expression.")
            st.write(f"Error: {str(e)}")
    else:
        talk('Please say the command again.')
        st.write('Please enter a valid command.')

# Streamlit UI
st.title("Emma - Your Virtual Assistant")

st.write("Type a command below and see Emma in action!")
command = st.text_input("Enter your command:", '')

if st.button('Run Emma'):
    if command:
        run_emma(command.lower())
    else:
        st.write("Please enter a command.")

# Additional functionality for audio input
if st.button('Transcribe Audio'):
    transcribed_command = transcribe_audio()
    if transcribed_command:
        st.write(f"Transcribed Command: {transcribed_command}")
        run_emma(transcribed_command.lower())

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

