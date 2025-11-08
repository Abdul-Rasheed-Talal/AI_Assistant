import os
import platform
import datetime
import webbrowser
import pyttsx3
import speech_recognition as sr
import pywhatkit
import wikipedia
import requests

# ---------------- TTS Engine ----------------
engine = pyttsx3.init()
engine.setProperty("rate", 180)

def speak(text):
    print(f"🤖 Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# ---------------- Speech Recognition ----------------
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio, language="en-US")
        print("🗣️ You said:", query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Speech service error.")
        return ""

# ---------------- AI Response (Hugging Face API) ----------------
HUGGINGFACE_API_TOKEN = "YOUR_HUGGINGFACE_API_KEY"  # Replace with your token

def ai_response(query):
    url = "https://api-inference.huggingface.co/models/gpt2"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    try:
        response = requests.post(url, headers=headers, json={"inputs": query})
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and "generated_text" in data[0]:
                return data[0]["generated_text"]
            return str(data)
        else:
            return f"API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error contacting AI: {e}"

# ---------------- Desktop / App Control ----------------
def open_app(app_name):
    system = platform.system()
    if system == "Windows":
        if "notepad" in app_name:
            os.system("start notepad")
        elif "chrome" in app_name:
            os.system("start chrome")
        elif "calculator" in app_name:
            os.system("start calc")
        else:
            speak(f"Sorry, I don't know how to open {app_name}.")

def google_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Searching Google for {query}")

def play_youtube(song):
    pywhatkit.playonyt(song)
    speak(f"Playing {song} on YouTube")

def tell_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def wikipedia_search(topic):
    speak("Searching Wikipedia...")
    try:
        result = wikipedia.summary(topic, sentences=2)
        speak(result)
    except:
        speak("Sorry, I couldn't find that on Wikipedia.")

# ---------------- Command Handler ----------------
def handle_command(query):
    if any(word in query for word in ["open", "launch"]):
        for app in ["chrome", "notepad", "calculator"]:
            if app in query:
                open_app(app)
                return True
    elif "search" in query:
        google_search(query.replace("search", "").strip())
        return True
    elif "play" in query:
        play_youtube(query.replace("play", "").strip())
        return True
    elif "time" in query:
        tell_time()
        return True
    elif "wikipedia" in query:
        wikipedia_search(query.replace("wikipedia", "").strip())
        return True
    else:
        # Anything else → AI
        speak(ai_response(query))
        return True

# ---------------- Main Loop ----------------
def main():
    speak("Hello, I am Jarvis, your personal AI assistant. How can I help you?")
    while True:
        query = listen()
        if query == "":
            continue
        if any(word in query for word in ["exit", "stop", "bye"]):
            speak("Goodbye!")
            break
        handle_command(query)

if __name__ == "__main__":
    main()
