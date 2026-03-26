import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import sys
import pywhatkit
import webbrowser
import requests
import json
import wikipedia
import threading
import time
from typing import Optional
import urllib.parse

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)  # Slightly faster speaking rate
recognizer = sr.Recognizer()

# Software paths configuration (easily modifiable)
SOFTWARE_PATHS = {
    'chrome': r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    'microsoft edge': r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    'notepad': 'notepad.exe',
    'calculator': 'calc.exe'
}

class AssistantCore:
    def __init__(self):
        self.is_listening = False
        self.is_speaking = False
        self.stop_speaking = False
        
    def speak(self, text: str) -> None:
        """Convert text to speech and display in terminal"""
        print(f"JARVIS: {text}")
        self.is_speaking = True
        self.stop_speaking = False
        
        # Break text into smaller chunks for interruptibility
        sentences = text.split('. ')
        for sentence in sentences:
            if self.stop_speaking:
                break
            if sentence.strip():  # Only speak non-empty sentences
                engine.say(sentence)
                engine.runAndWait()
        
        self.is_speaking = False
        
    def listen_for_wake_word(self) -> bool:
        """Listen for the wake word 'Jarvis'"""
        print("Listening for wake word... (Say 'Jarvis')")
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                # Listen with timeout to prevent hanging
                recorded_audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                text = recognizer.recognize_google(recorded_audio, language='en_US').lower()
                
                if 'jarvis' in text:
                    print("Wake word detected!")
                    self.speak('Yes sir? How can I help you?')
                    return True
                    
            except sr.WaitTimeoutError:
                pass  # No speech detected, continue listening
            except sr.UnknownValueError:
                pass  # Audio couldn't be understood
            except Exception as e:
                print(f"Error in wake word detection: {e}")
                
            return False
        
    def get_audio_input(self) -> Optional[str]:
        """Capture and convert audio input to text"""
        print("Listening...")
        
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = recognizer.recognize_google(audio, language='en_US').lower()
                print(f"You: {text}")
                
                # Check for stop command while speaking
                if self.is_speaking and 'jarvis stop' in text:
                    self.stop_speaking = True
                    engine.stop()
                    print("Stopping speech...")
                    return None
                    
                return text
            except sr.WaitTimeoutError:
                self.speak("I didn't hear anything. Please try again.")
            except sr.UnknownValueError:
                self.speak("I couldn't understand that. Could you please repeat?")
            except Exception as e:
                print(f"Error in audio input: {e}")
                self.speak("Sorry, I encountered an error. Please try again.")
            
            return None
            
    def voice_command(self):
        """Process voice command"""
        command = self.get_audio_input()
        if command:
            self.process_command(command)
        
    def open_software(self, software_name: str) -> None:
        """Open the requested software"""
        software_name = software_name.lower()
        
        if 'play' in software_name:
            query = software_name.replace('play', '').strip()
            if query:
                self.speak(f'Playing {query} on YouTube')
                pywhatkit.playonyt(query)
            else:
                self.speak("What would you like me to play on YouTube?")
                query = self.get_audio_input()
                if query:
                    pywhatkit.playonyt(query)
            return
            
        # Check for matches in our software paths
        for key in SOFTWARE_PATHS:
            if key in software_name:
                self.speak(f'Opening {key.title()}...')
                try:
                    subprocess.Popen(SOFTWARE_PATHS[key])
                except Exception as e:
                    print(f"Error opening {key}: {e}")
                    self.speak(f"Sorry, I couldn't open {key}.")
                return
        
        # If no match found
        self.speak(f"I'm not sure how to open {software_name}. Please check if it's configured.")

    def search_in_chrome(self, query: str) -> None:
        """Search the given query in Chrome browser"""
        if not query:
            self.speak("What would you like me to search for?")
            query = self.get_audio_input()
            if not query:
                return
        
        self.speak(f"Searching for {query} in Chrome")
        
        try:
            # Encode the query for URL
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            # Open Chrome with the search URL
            if os.path.exists(SOFTWARE_PATHS['chrome']):
                subprocess.Popen([SOFTWARE_PATHS['chrome'], search_url])
            else:
                # Fallback to default browser if Chrome path is not found
                webbrowser.open(search_url)
                self.speak("Opening in your default browser")
                
        except Exception as e:
            print(f"Error opening Chrome: {e}")
            self.speak("Sorry, I couldn't open Chrome. Please try again.")

    def close_software(self, software_name: str) -> None:
        """Close the requested software"""
        software_name = software_name.lower()
        closed = False
        
        if 'chrome' in software_name:
            os.system("taskkill /f /im chrome.exe")
            closed = True
        elif 'edge' in software_name or 'microsoft edge' in software_name:
            os.system("taskkill /f /im msedge.exe")
            closed = True
        elif 'notepad' in software_name:
            os.system("taskkill /f /im notepad.exe")
            closed = True
        elif 'calculator' in software_name:
            os.system("taskkill /f /im calculator.exe")
            closed = True
            
        if closed:
            self.speak(f'Closing {software_name}...')
        else:
            self.speak(f"I don't know how to close {software_name}.")

    def get_time(self) -> None:
        """Get and speak the current time"""
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        self.speak(f"The current time is {current_time}")

    def get_date(self) -> None:
        """Get and speak the current date"""
        current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        self.speak(f"Today is {current_date}")

    def search_web(self, query: str) -> None:
        """Search the web and display results in terminal and speak them"""
        if not query:
            self.speak("What would you like me to search for?")
            query = self.get_audio_input()
            if not query:
                return
                
        self.speak(f"Searching for {query}")
        
        try:
            # Try to get Wikipedia summary first
            try:
                wiki_summary = wikipedia.summary(query, sentences=2)
                print(f"\nAccording to Wikipedia:\n{wiki_summary}\n")
                # Speak the Wikipedia summary
                self.speak(f"According to Wikipedia: {wiki_summary}")
            except:
                print(f"\nSearch results for '{query}':\n")
                
            # Get additional context from web search API
            try:
                # Using DuckDuckGo API for instant answers
                ddg_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
                response = requests.get(ddg_url)
                data = response.json()
                
                if data['Abstract']:
                    abstract_text = f"From DuckDuckGo: {data['Abstract']}"
                    print(abstract_text + "\n")
                    self.speak(abstract_text)
                elif data['Answer']:
                    answer_text = f"Answer: {data['Answer']}"
                    print(answer_text + "\n")
                    self.speak(answer_text)
                    
                if data['RelatedTopics']:
                    related_text = "Related topics:"
                    print(related_text)
                    self.speak(related_text)
                    
                    for topic in data['RelatedTopics'][:3]:
                        if 'Text' in topic:
                            topic_text = f"- {topic['Text']}"
                            print(topic_text)
                            self.speak(topic_text)
            except:
                # Fallback to Google search if API fails
                fallback_text = f"For more detailed information, I would typically open a browser to search for '{query}'."
                print(fallback_text)
                self.speak(fallback_text)
                
        except Exception as e:
            print(f"Error during web search: {e}")
            self.speak("Sorry, I encountered an error while searching. Please try again.")

    def tell_joke(self) -> None:
        """Tell a random joke"""
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            joke = response.json()
            self.speak(joke['setup'])
            time.sleep(1)  # Pause for comedic effect
            self.speak(joke['punchline'])
        except:
            self.speak("Why don't scientists trust atoms? Because they make up everything!")

    def answer_question(self, question: str) -> None:
        """Answer general knowledge questions using web search"""
        self.search_web(question)

    def process_command(self, command: str) -> bool:
        """Process the user's command"""
        if not command:
            return True
            
        command = command.lower()
        
        if any(word in command for word in ['bye', 'goodbye', 'exit', 'quit']):
            self.speak('Goodbye sir! Have a great day!')
            os._exit(0)
            
        elif any(word in command for word in ['stop', 'shut down']):
            if 'jarvis' in command:
                self.speak('Stopping now.')
                return False
            
        elif 'open' in command:
            software_name = command.replace('open', '').strip()
            self.open_software(software_name)
            
        elif 'search' in command:
            # Extract the search query from the command
            query = command.replace('search', '').replace('for', '').strip()
            if query:
                self.search_in_chrome(query)
            else:
                self.speak("What would you like me to search for?")
                query = self.get_audio_input()
                if query:
                    self.search_in_chrome(query)
            
        elif 'close' in command or 'shut' in command:
            software_name = command.replace('close', '').replace('shut', '').strip()
            self.close_software(software_name)
            
        elif 'time' in command:
            self.get_time()
            
        elif 'date' in command or 'day' in command:
            self.get_date()
            
        elif any(word in command for word in ['what is', 'who is', 'how to', 'when is', 'where is']):
            query = command
            for word in ['what', 'who', 'how', 'when', 'where']:
                query = query.replace(word, '')
            query = query.strip()
            self.answer_question(query)
            
        elif 'joke' in command:
            self.tell_joke()
            
        elif 'who is god' in command:
            self.speak('Ajitheyyy Kadavuleyy')
            
        elif 'what is your name' in command:
            self.speak('My name is Jarvis, your personal assistant')
            
        elif 'how are you' in command:
            self.speak('I am functioning optimally, thank you for asking. How are you today?')
            
        else:
            # For any other command, try to answer as a question
            self.answer_question(command)
            
        return True

    def run(self):
        """Main function to run the voice assistant"""
        self.speak("JARVIS initialized and ready. Say my name to activate.")
        
        while True:
            try:
                # Wait for wake word
                if self.listen_for_wake_word():
                    # Continue processing commands until told to stop
                    while True:
                        command = self.get_audio_input()
                        if command is None:  # Command was interrupted
                            continue
                        if not self.process_command(command):
                            break
                        self.speak("Anything else I can help with?")
            except KeyboardInterrupt:
                self.speak("Shutting down by user request. Goodbye!")
                os._exit(0)
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.speak("I encountered an error. Restarting my listening function.")

# Run the assistant
if __name__ == "__main__":
    assistant = AssistantCore()
    assistant.run()   