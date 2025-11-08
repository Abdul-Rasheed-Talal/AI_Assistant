import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import requests
import json
import subprocess
import os
import threading
import time
from datetime import datetime
import logging
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class JarvisAssistant:
    def __init__(self, ai_api_key: str = None):
        """
        Initialize Jarvis AI Assistant
        """
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech with thread safety
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.8)
        
        # AI configuration
        self.ai_api_key = ai_api_key or os.getenv('HUGGINGFACE_API_KEY')
        
        # Command history logging
        self.setup_logging()
        
        # App paths (Windows)
        self.app_paths = {
            'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'file explorer': 'explorer.exe',
            'paint': 'mspaint.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe',
            'vlc': 'C:\\Program Files\\VideoLAN\\VLC\\vlc.exe',
            'spotify': 'spotify.exe'
        }
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Jarvis is ready!")
        
    def setup_logging(self):
        """Setup logging for commands and responses"""
        logging.basicConfig(
            filename='jarvis_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
    def speak(self, text: str):
        """
        Convert text to speech (thread-safe)
        """
        def speak_thread():
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except RuntimeError as e:
                if "run loop already started" in str(e):
                    self.tts_engine.endLoop()
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
        
        thread = threading.Thread(target=speak_thread)
        thread.daemon = True
        thread.start()
        thread.join(timeout=10)
        
    def listen(self) -> Optional[str]:
        """
        Listen to microphone and convert speech to text
        """
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=12)
            
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            self.speak("I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
            self.speak("There was an error with speech recognition service.")
            return None
            
    def get_ai_response(self, user_input: str) -> str:
        """
        Get intelligent response from Hugging Face Inference API
        """
        if not self.ai_api_key:
            return "I need a Hugging Face API key to provide AI responses. Please configure your API key in the .env file."
            
        try:
            return self._get_huggingface_response(user_input)
                
        except requests.exceptions.Timeout:
            return "The AI service is taking too long to respond. Please try again."
        except requests.exceptions.ConnectionError:
            return "I cannot connect to the AI service. Please check your internet connection."
        except Exception as e:
            print(f"Hugging Face API Error: {e}")
            return "I'm having trouble connecting to the AI service right now. Please try again later."
    
    def _get_huggingface_response(self, user_input: str) -> str:
        """Get response from Hugging Face using currently working models"""
        # Using models that are known to work with the inference API
        working_models = [
            "microsoft/DialoGPT-medium",  # Try this first
            "HuggingFaceH4/zephyr-7b-beta",  # Modern chat model
            "google/flan-t5-large",  # General purpose model
            "mistralai/Mistral-7B-Instruct-v0.1"  # Another good model
        ]
        
        for model in working_models:
            try:
                print(f"Trying model: {model}")
                API_URL = f"https://api-inference.huggingface.co/models/{model}"
                headers = {"Authorization": f"Bearer {self.ai_api_key}"}
                
                # Prepare payload based on model type
                if "zephyr" in model.lower() or "mistral" in model.lower() or "instruct" in model.lower():
                    # For instruction-tuned models
                    prompt = f"<|user|>\n{user_input}\n<|assistant|>\n"
                    payload = {
                        "inputs": prompt,
                        "parameters": {
                            "max_new_tokens": 100,
                            "temperature": 0.7,
                            "do_sample": True,
                            "return_full_text": False
                        }
                    }
                elif "dialo" in model.lower():
                    # For dialog models
                    payload = {
                        "inputs": user_input,
                        "parameters": {
                            "max_length": 100,
                            "temperature": 0.7,
                            "do_sample": True
                        }
                    }
                else:
                    # For general models
                    payload = {
                        "inputs": user_input,
                        "parameters": {
                            "max_length": 100,
                            "temperature": 0.7
                        }
                    }
                
                payload["options"] = {"wait_for_model": True, "use_cache": True}
                
                response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 503:
                    print(f"Model {model} is loading, waiting...")
                    time.sleep(20)
                    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    return self._parse_huggingface_response(result)
                else:
                    print(f"Model {model} returned status {response.status_code}")
                    continue
                    
            except Exception as e:
                print(f"Model {model} failed: {e}")
                continue
                
        # If all models fail, try a simple text generation approach
        return self._get_fallback_ai_response(user_input)
    
    def _parse_huggingface_response(self, result) -> str:
        """Parse different response formats from Hugging Face"""
        if isinstance(result, list) and len(result) > 0:
            if 'generated_text' in result[0]:
                return result[0]['generated_text']
            elif 'summary_text' in result[0]:
                return result[0]['summary_text']
            else:
                # Extract text from the first item
                return str(result[0]).strip('{}').split(':')[-1].strip('\"')
        elif isinstance(result, dict):
            if 'generated_text' in result:
                return result['generated_text']
            else:
                return str(result)
        else:
            return str(result)
    
    def _get_fallback_ai_response(self, user_input: str) -> str:
        """Use a simple, reliable text generation model"""
        try:
            # Use a very basic model that's almost always available
            API_URL = "https://api-inference.huggingface.co/models/gpt2"
            headers = {"Authorization": f"Bearer {self.ai_api_key}"}
            
            payload = {
                "inputs": user_input,
                "parameters": {
                    "max_length": 80,
                    "temperature": 0.8,
                    "do_sample": True
                },
                "options": {
                    "wait_for_model": True
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Remove the original input from the response
                    if user_input in generated_text:
                        return generated_text.replace(user_input, '').strip()
                    return generated_text
            return self.get_simple_ai_response(user_input)
            
        except Exception as e:
            print(f"Fallback AI also failed: {e}")
            return self.get_simple_ai_response(user_input)
            
    def open_application(self, app_name: str) -> bool:
        """
        Open desktop applications
        """
        try:
            app_name_lower = app_name.lower().strip()
            
            if app_name_lower in self.app_paths:
                subprocess.Popen(self.app_paths[app_name_lower])
                return True
            elif 'chrome' in app_name_lower:
                subprocess.Popen(['start', 'chrome'], shell=True)
                return True
            elif 'notepad' in app_name_lower:
                subprocess.Popen(['notepad'], shell=True)
                return True
            elif 'calculator' in app_name_lower or 'calc' in app_name_lower:
                subprocess.Popen(['calc'], shell=True)
                return True
            elif 'paint' in app_name_lower:
                subprocess.Popen(['mspaint'], shell=True)
                return True
            else:
                subprocess.Popen(f'start {app_name}', shell=True)
                return True
                
        except Exception as e:
            print(f"Error opening application {app_name}: {e}")
            return False
            
    def search_google(self, query: str):
        """Search Google for the given query"""
        try:
            pywhatkit.search(query)
            return True
        except Exception as e:
            print(f"Google search error: {e}")
            return False
            
    def play_on_youtube(self, query: str):
        """Play video on YouTube"""
        try:
            pywhatkit.playonyt(query)
            return True
        except Exception as e:
            print(f"YouTube error: {e}")
            return False
            
    def get_wikipedia_info(self, query: str) -> str:
        """Get Wikipedia summary"""
        try:
            wikipedia.set_lang("en")
            result = wikipedia.summary(query, sentences=3)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found for {query}. Please be more specific. Try: {', '.join(e.options[:3])}"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for {query}."
        except Exception as e:
            return f"Error accessing Wikipedia: {str(e)}"
            
    def get_time_date(self) -> str:
        """Get current time and date"""
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        current_date = now.strftime("%A, %B %d, %Y")
        return f"The current time is {current_time} and the date is {current_date}"
        
    def get_weather_info(self, location: str = "") -> str:
        """Get basic weather information"""
        if location:
            return f"I don't have weather integration set up yet for {location}. You can add a weather API like OpenWeatherMap."
        else:
            return "I need a location to check the weather. Please specify which city or location."
    
    def get_simple_ai_response(self, user_input: str) -> str:
        """Provide simple rule-based responses when API fails"""
        user_input_lower = user_input.lower()
        
        # Enhanced simple responses
        simple_responses = {
            'hello': "Hello! I'm Jarvis, your AI assistant. How can I help you today?",
            'hi': "Hi there! What can I do for you?",
            'how are you': "I'm functioning perfectly, thank you for asking! How can I assist you?",
            'what can you do': "I can open applications, search Google, play YouTube videos, tell time, search Wikipedia, and have conversations with you!",
            'thank you': "You're welcome! Is there anything else I can help with?",
            'your name': "I'm Jarvis, your personal AI assistant!",
            'who are you': "I'm Jarvis, an AI assistant designed to help you with various tasks and conversations.",
            'help': "I can help you with: opening apps, web searches, playing videos, telling time, Wikipedia searches, and answering questions.",
            'joke': "Why don't scientists trust atoms? Because they make up everything!",
            'time': self.get_time_date(),
            'date': self.get_time_date(),
            'weather': "I need a specific location to check the weather. Try saying 'weather in London'.",
            'who made you': "I was created by a developer using Python and various AI technologies!",
            'what is your purpose': "My purpose is to assist you with tasks, answer questions, and make your life easier!",
            'how old are you': "I'm an AI, so I don't have an age in the traditional sense. I was just created!",
            'where are you': "I'm right here in your computer, ready to help you!",
            'good morning': "Good morning! Hope you have a wonderful day ahead!",
            'good night': "Good night! Sleep well and see you tomorrow!",
            'how does this work': "I use speech recognition to understand you and text-to-speech to respond. For complex questions, I use AI models."
        }
        
        for key, response in simple_responses.items():
            if key in user_input_lower:
                return response
        
        # For questions starting with what, how, why, when
        if any(user_input_lower.startswith(word) for word in ['what', 'how', 'why', 'when', 'where', 'can you']):
            return "That's an interesting question! While my AI capabilities are currently limited, I'd be happy to help you search for that on Google or Wikipedia."
        
        return "I understand you're asking something, but my advanced AI features are currently unavailable. I can still help you with practical tasks like opening apps, searching the web, or looking up information!"
        
    def process_command(self, command: str) -> str:
        """
        Process natural language commands and execute appropriate actions
        """
        command_lower = command.lower()
        
        # Exit commands
        if any(word in command_lower for word in ['exit', 'stop', 'bye', 'goodbye', 'quit', 'shutdown']):
            return "Goodbye! It was a pleasure assisting you. Have a great day!"
            
        # Greeting responses
        if any(word in command_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm Jarvis, your AI assistant. How can I help you today?"
            
        # Open applications
        if 'open' in command_lower:
            app_name = command_lower.replace('open', '').strip()
            if app_name:
                if self.open_application(app_name):
                    return f"Opening {app_name} for you"
                else:
                    return f"Sorry, I couldn't open {app_name}. It might not be installed or I don't know how to open it."
            else:
                return "Please specify which application you'd like me to open."
                
        # Google search
        if 'search' in command_lower and 'google' in command_lower:
            query = command_lower.replace('search', '').replace('on google', '').replace('google', '').strip()
            if query:
                if self.search_google(query):
                    return f"Searching Google for {query}"
                else:
                    return f"Sorry, I couldn't search for {query} on Google"
            else:
                return "What would you like me to search on Google?"
                
        # YouTube
        if any(word in command_lower for word in ['play', 'watch']) and 'youtube' in command_lower:
            query = command_lower.replace('play', '').replace('watch', '').replace('on youtube', '').replace('youtube', '').strip()
            if query:
                if self.play_on_youtube(query):
                    return f"Playing {query} on YouTube for you"
                else:
                    return f"Sorry, I couldn't play {query} on YouTube"
            else:
                return "What would you like me to play on YouTube?"
                
        # Time and date
        if any(word in command_lower for word in ['time', 'date']):
            return self.get_time_date()
            
        # Wikipedia
        if 'wikipedia' in command_lower:
            query = command_lower.replace('wikipedia', '').replace('search', '').replace('on', '').strip()
            if query:
                result = self.get_wikipedia_info(query)
                return result
            else:
                return "What would you like me to search on Wikipedia?"
                
        # Weather
        if 'weather' in command_lower:
            location = command_lower.replace('weather', '').replace('in', '').replace('for', '').strip()
            return self.get_weather_info(location if location else "")
            
        # If no specific command matched, try AI or fallback
        if self.ai_api_key:
            ai_response = self.get_ai_response(command)
            return ai_response
        else:
            return self.get_simple_ai_response(command)
        
    def run(self):
        """Main loop for Jarvis assistant"""
        self.speak("Hello! I am Jarvis, your AI assistant. How can I help you today?")
        print("Jarvis is now active. Say 'stop', 'exit', or 'goodbye' to end the session.")
        
        while True:
            try:
                command = self.listen()
                
                if command:
                    logging.info(f"User: {command}")
                    print(f"Command received: {command}")
                    
                    response = self.process_command(command)
                    
                    logging.info(f"Jarvis: {response}")
                    print(f"Jarvis: {response}")
                    
                    self.speak(response)
                    
                    if any(word in command.lower() for word in ['exit', 'stop', 'bye', 'goodbye', 'quit']):
                        break
                else:
                    time.sleep(1)
                        
            except KeyboardInterrupt:
                self.speak("Goodbye! Shutting down.")
                print("\nJarvis shutdown initiated by user.")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.speak("I encountered an unexpected error. Let's continue.")
                
        print("Jarvis session ended.")

def main():
    """Main function to start Jarvis"""
    print("Initializing Jarvis AI Assistant...")
    print("=" * 50)
    
    HF_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    
    if not HF_API_KEY:
        print("Warning: HUGGINGFACE_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key.")
        print("Basic commands will work with simple rule-based responses.")
    
    jarvis = JarvisAssistant(ai_api_key=HF_API_KEY)
    
    print(f"Hugging Face API configured: {'Yes' if HF_API_KEY else 'No'}")
    print("Basic commands available: open apps, search Google, play YouTube, time/date, Wikipedia")
    print("Enhanced simple responses for common questions")
    print("=" * 50)
    
    jarvis.run()

if __name__ == "__main__":
    main()