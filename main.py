import os
import subprocess
import ctypes
import datetime
import wikipedia
import speech_recognition as sr
import pygame
import openai
import pyttsx3

# The custom_voice module with the speak function
# from Assistant.Features.custom_voice import speak

# Global variables
r = sr.Recognizer()
MASTER = "KIRA"
brave_path = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Brave.lnk'

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices)
engine.setProperty('voice', voices[1].id)
# speak function  will pronounce the string which is passed to it
# def takecommand():
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Set your OpenAI API key
openai.api_key = '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'


# Function to wish based on the time
def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"GOOD MORNING {MASTER}")
    elif 12 <= hour < 18:
        speak(f"GOOD AFTERNOON {MASTER}")
    else:
        speak(f"GOOD EVENING {MASTER}")


# Function to handle voice input
def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, can you say that again?")
            print("Sorry, can you say that again?")
            return None
        except sr.RequestError as e:
            speak(f"Could not request results from Google Speech Recognition service: {e}")
            return None


# Function to generate and speak a response using GPT-3
def listen_and_respond(query):
    try:
        # Generate a response using GPT-3
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=query,
            max_tokens=100
        )

        # Speak the response
        response_text = response.choices[0].text.strip()
        print(f"Assistant: {response_text}")
        speak(response_text)

    except Exception as e:
        print(f"Error in generating response: {e}")


# Main code
print("INITIALIZING DARK_ARRAY!!!!")
wish_me()

while True:
    query = take_command()

    if query is not None:
        if 'wikipedia' in query:
            speak("Searching in Wikipedia")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            print(results)
            speak(results)
        elif 'youtube' in query:
            speak("Opening Youtube, my master")
            url = 'https://www.youtube.com'
            subprocess.Popen([brave_path, url], shell=True)
        elif 'try hack me' in query:
            speak("Opening Your battleground, master")
            url = 'https://tryhackme.com/'
            subprocess.Popen([brave_path, url], shell=True)
        elif 'spotify' in query:
            speak("Opening Your songs, master ")
            app = r"C:\Users\myhea\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Brave Apps\Spotify.lnk"
            try:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", app, None, None, 1)
                print(f"Opened {app} successfully")
            except Exception as e:
                print(f"Error in opening Spotify {app}: {e}")
        elif 'chat gpt' in query:
            speak("Opening Chat GPT")
            url = 'https://chat.openai.com/'
            subprocess.Popen([brave_path, url], shell=True)
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif 'open mail' in query:
            url = 'https://mail.google.com/mail/u/0/#inbox'
            subprocess.Popen([brave_path, url], shell=True)
        elif 'whatsapp' in query:
            speak("Opening WhatsApp")
            url = 'https://web.whatsapp.com'
            subprocess.Popen([brave_path, url], shell=True)
        elif 'open vs code' in query or 'open Visual Studio code' in query:
            speak("Opening VS code, master")
            Vs_code = r"C:\\Users\myhea\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            subprocess.Popen([Vs_code], shell=True)
        elif 'exit' in query:
            speak("Goodbye Master")
            print("Goodbye Master-sama ;)")
            pygame.mixer.quit()
            break
        else:
            listen_and_respond(query)
