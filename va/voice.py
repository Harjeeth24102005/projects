import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import sys
import pywhatkit 
import pygame
import time

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Predefined audio file paths for responses
audio_data = {
    "exit": "goodbye.mp3",
    "eligibility": "eligibility.mp3",
    "iic": "iic.mp3",
    "robotics": "robotics.mp3",
    "physical": "physical.mp3",
    "me": "me.mp3",
    "medical": "me.mp3",
    "mba": "mba.mp3",
    "mechanical": "mechanical.mp3",
    "aids": "aids.mp3",
    "data science": "aids.mp3",
    "cyber security": "cyber security.mp3",
    "it": "it.mp3",
    "canteen": "canteen.mp3",
    "mess": "canteen.mp3",
    "transport": "transport.mp3",
    "hostel": "hostel.mp3",
    "campus life": "campus life.mp3",
    "ece": "ece.mp3",
    "cse": "cse.mp3",
    "cce": "cse.mp3",
    "biotechnology": "biotechnology.mp3",
    "csbs": "csbs.mp3",
    "machine learning": "aiml.mp3",
    "aiml": "aiml.mp3",
    "aeronautical": "aeronautical.mp3",
    "gojan": "about.mp3",
    "research": "r&d.mp3",
    "research and development": "r&d.mp3",
    "culturals": "culturals.mp3",
    "library": "library.mp3",
    "club": "club.mp3",
    "wake_word": "wake up.mp3",
    "greeting": "greeting.mp3",
    "not_understood": "not understanding.mp3",
    "service_error": "service error.mp3",
    "goodbye": "goodbye.mp3",
    "oops": "oops.mp3",
}

# Knowledge base for questions and responses
QUESTION_RESPONSES = {
    # College-related questions
    "what is eligibility": "eligibility",
    "tell me about eligibility": "eligibility",
    "admission eligibility": "eligibility",
    "eligibility criteria": "eligibility",
    
    "what is iic": "iic",
    "tell me about iic": "iic",
    "iic college": "iic",
    "institution innovation council": "iic",
    
    "robotics club": "robotics",
    "about robotics": "robotics",
    "tell me about robotics": "robotics",
    "robotics department": "robotics",
    
    "physical education": "physical",
    "sports facilities": "physical",
    "gym facilities": "physical",
    
    "mechanical engineering": "me",
    "about mechanical engineering": "me",
    "me department": "me",
    
    "medical facilities": "medical",
    "college hospital": "medical",
    "health center": "medical",
    
    "mba program": "mba",
    "business administration": "mba",
    "management studies": "mba",
    
    "aids department": "aids",
    "ai data science": "aids",
    "artificial intelligence": "aids",
    "data science course": "aids",
    
    "cyber security": "cyber security",
    "cybersecurity course": "cyber security",
    "information security": "cyber security",
    
    "it department": "it",
    "information technology": "it",
    
    "canteen facility": "canteen",
    "food court": "canteen",
    "college canteen": "canteen",
    
    "mess facility": "mess",
    "hostel mess": "mess",
    
    "transport facility": "transport",
    "college bus": "transport",
    "transportation": "transport",
    
    "hostel facility": "hostel",
    "accommodation": "hostel",
    "student hostel": "hostel",
    
    "campus life": "campus life",
    "life at campus": "campus life",
    "student life": "campus life",
    
    "ece department": "ece",
    "electronics engineering": "ece",
    "ece course": "ece",
    
    "cse department": "cse",
    "computer science": "cse",
    "cse course": "cse",
    "computer science engineering": "cse",
    
    "biotechnology": "biotechnology",
    "biotech department": "biotechnology",
    "biotechnology course": "biotechnology",
    
    "csbs department": "csbs",
    "computer science business": "csbs",
    "csbs course": "csbs",
    
    "machine learning": "machine learning",
    "ml course": "machine learning",
    "about machine learning": "machine learning",
    
    "aiml department": "aiml",
    "ai ml course": "aiml",
    "artificial intelligence machine learning": "aiml",
    
    "aeronautical engineering": "aeronautical",
    "aerospace engineering": "aeronautical",
    "aeronautical department": "aeronautical",
    
    "about college": "gojan",
    "about gojan": "gojan",
    "college information": "gojan",
    
    "research department": "research",
    "r&d": "research",
    "research facilities": "research",
    "research and development": "research",
    
    "culturals": "culturals",
    "cultural events": "culturals",
    "college fest": "culturals",
    
    "library facility": "library",
    "college library": "library",
    "library resources": "library",
    
    "student clubs": "club",
    "college clubs": "club",
    "technical clubs": "club",
    
    # General questions
    "what is your name": "My name is Jarvis, your voice assistant for Gojan Educational Institution.",
    "who are you": "I am Jarvis, an AI assistant created to help you with information about Gojan College.",
    "how are you": "I'm functioning perfectly! How can I assist you today?",
    "what can you do": "I can provide information about courses, facilities, events, and help with various tasks.",
}

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 160)  # Slightly slower for better clarity
recognizer = sr.Recognizer()

def play_audio_file(keyword):
    """Play audio file based on keyword"""
    file_path = audio_data.get(keyword)
    if file_path and os.path.exists(file_path):
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            print(f"🔊 Playing audio: {keyword}")
            # Wait for audio to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            return True
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
    else:
        print(f"Audio file not found: {file_path}")
        return False

def speak(text, use_audio=True):
    """Speak text using TTS or play audio file"""
    print(f"🤖 JARVIS: {text}")
    
    if not use_audio:
        engine.say(text)
        engine.runAndWait()
        return
    
    # Convert text to lowercase for matching
    text_lower = text.lower()
    
    # Check if any audio file keyword exists in the text
    matched_keyword = None
    for keyword in sorted(audio_data.keys(), key=lambda x: -len(x)):
        if keyword in text_lower:
            matched_keyword = keyword
            break
    
    # If audio file exists, play it instead of TTS
    if matched_keyword and play_audio_file(matched_keyword):
        return
    
    # Fallback to TTS if no audio file found or playback failed
    engine.say(text)
    engine.runAndWait()

def find_best_audio_match(command):
    """Find the best matching audio file for the command"""
    command_lower = command.lower()
    
    # First, check question responses
    for question, response in QUESTION_RESPONSES.items():
        if question in command_lower:
            if response in audio_data:  # If response is an audio file key
                return response
            else:  # If response is a text response
                return None
    
    # Then check direct audio file keywords
    matched_keyword = None
    longest_match = 0
    
    for keyword in audio_data.keys():
        if keyword in command_lower:
            if len(keyword) > longest_match:
                longest_match = len(keyword)
                matched_keyword = keyword
    
    return matched_keyword

def open_software(software_name):
    software_name_lower = software_name.lower()
    
    if 'chrome' in software_name_lower:
        speak('Opening Chrome...', use_audio=False)
        program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([program])

    elif 'microsoft edge' in software_name_lower:
        speak('Opening Microsoft Edge...', use_audio=False)
        program = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        subprocess.Popen([program])

    elif 'play' in software_name_lower:
        query = software_name_lower.replace('play', '').strip()
        if query:
            speak(f'Playing {query} on YouTube', use_audio=False)
            pywhatkit.playonyt(query)
        else:
            speak("What would you like me to play on YouTube?", use_audio=False)

    elif 'notepad' in software_name_lower:
        speak('Opening Notepad...', use_audio=False)
        subprocess.Popen(['notepad.exe']) 
        
    elif 'calculator' in software_name_lower:
        speak('Opening Calculator...', use_audio=False)
        subprocess.Popen(['calc.exe'])
        
    else:
        speak(f"I couldn't find the software {software_name}", use_audio=False)

def close_software(software_name):
    software_name_lower = software_name.lower()
    
    if 'chrome' in software_name_lower:
        speak('Closing Chrome...', use_audio=False)
        os.system("taskkill /f /im chrome.exe")

    elif 'microsoft edge' in software_name_lower:
        speak('Closing Microsoft Edge...', use_audio=False)
        os.system("taskkill /f /im msedge.exe")

    elif 'notepad' in software_name_lower:
        speak('Closing Notepad...', use_audio=False)
        os.system("taskkill /f /im notepad.exe")
        
    elif 'calculator' in software_name_lower:
        speak('Closing Calculator...', use_audio=False)
        os.system("taskkill /f /im calculator.exe")
        
    else:
        speak(f"I couldn't find any open software named {software_name}", use_audio=False)

def listen_for_wake_word():
    with sr.Microphone() as source:
        print('🔇 Listening for wake word "Jarvis"...')
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            try:
                recorded_audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                text = recognizer.recognize_google(recorded_audio, language='en_US')
                text = text.lower()
                print(f"👤 Heard: {text}")
                
                if 'jarvis' in text:
                    print('✅ Wake word detected!')
                    # Play greeting audio if available
                    if not play_audio_file("greeting"):
                        speak('Hello! I am Jarvis. How can I assist you today?', use_audio=False)
                    return True
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as ex:
                continue

def process_question(command):
    """Process questions and provide appropriate responses"""
    command_lower = command.lower()
    
    # Check for question patterns and provide appropriate responses
    for question_pattern, response in QUESTION_RESPONSES.items():
        if question_pattern in command_lower:
            if response in audio_data:  # If response is an audio file key
                speak(f"Let me tell you about {response}", use_audio=False)
                if play_audio_file(response):
                    return True
                else:
                    speak(f"I have information about {response}", use_audio=False)
                    return True
            else:  # If response is a text response
                speak(response, use_audio=False)
                return True
    
    return False

def process_command(text):
    """Process the command and provide intelligent responses"""
    if not text:
        return True
    
    text_lower = text.lower()
    print(f"🎯 Processing: {text_lower}")
    
    # First, try to process as a question
    if process_question(text):
        return True
    
    # Check for direct audio file keywords
    audio_match = find_best_audio_match(text)
    if audio_match:
        speak(f"Let me provide information about {audio_match}", use_audio=False)
        if play_audio_file(audio_match):
            return True
    
    # Process other commands
    if any(word in text_lower for word in ['stop', 'exit', 'goodbye', 'bye', 'quit']):
        if not play_audio_file("goodbye"):
            speak('Goodbye! Have a great day!', use_audio=False)
        sys.exit()
        
    elif 'open' in text_lower:
        software_name = text_lower.replace('open', '').strip()
        open_software(software_name)
        
    elif 'close' in text_lower:
        software_name = text_lower.replace('close', '').strip()
        close_software(software_name)
        
    elif 'time' in text_lower:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}", use_audio=False)
        
    elif 'date' in text_lower:
        current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        speak(f"Today is {current_date}", use_audio=False)
        
    elif 'who is god' in text_lower:
        speak('Ajitheyyy Kadavuleyy', use_audio=False)
        
    else:
        # If no specific command matched
        if not play_audio_file("not_understood"):
            speak("I'm not sure about that. You can ask me about college courses, facilities, or other information.", use_audio=False)
    
    return True

def get_voice_command():
    """Listen for voice command and return text"""
    with sr.Microphone() as source:
        print('\n🎤 Listening for your command...')
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        
        try:
            recorded_audio = recognizer.listen(source, timeout=8, phrase_time_limit=6)
            text = recognizer.recognize_google(recorded_audio, language='en_US')
            text = text.lower()
            print(f'👤 You said: {text}')
            return text
            
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.", use_audio=False)
            return None
        except sr.UnknownValueError:
            if not play_audio_file("not_understood"):
                speak("I couldn't understand that. Could you please repeat?", use_audio=False)
            return None
        except Exception as ex:
            print(f"Error: {ex}")
            if not play_audio_file("service_error"):
                speak("Sorry, I encountered an error. Please try again.", use_audio=False)
            return None

def main():
    print("=" * 60)
    print("🎓 JARVIS - Gojan College Voice Assistant")
    print("=" * 60)
    print("💡 You can ask me about:")
    print("• College courses and departments")
    print("• Campus facilities")
    print("• Opening applications")
    print("• Time and date")
    print("=" * 60)
    
    # Play wake word audio at start
    play_audio_file("wake_word")
    
    while True:
        if listen_for_wake_word():
            speak("I'm listening. What would you like to know?", use_audio=False)
            
            while True: 
                command = get_voice_command()
                if command:
                    process_command(command)
                    
                    # Ask if user needs more help
                    time.sleep(1)
                    speak("Is there anything else you'd like to know?", use_audio=False)
                    
if __name__ == "__main__":
    main()