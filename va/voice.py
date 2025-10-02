import cv2
import mediapipe as mp
import numpy as np
import math
import pyttsx3
import threading
import time
import os
import datetime
import subprocess
import sys
import pywhatkit 
import pygame 
import speech_recognition as sr

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Constants for hand gesture detection
FRAME_WIDTH = 800  
FRAME_HEIGHT = 600  
INACTIVE_TIME_THRESHOLD = 3
SILENCE_TIMEOUT = 120  # 2 minutes

# Color Scheme
COLORS = {
    'primary': (0, 255, 255),    # Cyan
    'secondary': (255, 105, 180), # Pink
    'accent': (50, 205, 50),     # Lime Green
    'warning': (0, 165, 255),    # Orange
    'success': (0, 255, 127),    # Spring Green
}

# Global variables for voice assistant
response_given = False
pulse_effect = 0
wake_word_activated = False
last_voice_time = time.time()
voice_assistant_active = False
greeting_played = False
audio_playing = False  # New flag to track audio playback

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
    "sleep": "sleep.mp3",
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
}

# Initialize webcam
webcam = cv2.VideoCapture(0)
webcam.set(3, FRAME_WIDTH)
webcam.set(4, FRAME_HEIGHT)

if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize pyttsx3 engine (for fallback only)
engine = pyttsx3.init()

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.last_x = None
        self.movement_buffer = []
        self.wave_detected = False
        self.wave_cooldown = 0
    
    def find_hands(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS
                )
        return img
    
    def get_wrist_position(self):
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]
            wrist = hand.landmark[0]
            return wrist.x, wrist.y
        return None
    
    def detect_wave(self):
        """Detect wave gesture using MediaPipe"""
        wrist_pos = self.get_wrist_position()
        
        if wrist_pos:
            current_x, current_y = wrist_pos
            
            if self.last_x is not None:
                movement = current_x - self.last_x
                self.movement_buffer.append(movement)
                
                # Keep only recent movements
                if len(self.movement_buffer) > 8:
                    self.movement_buffer.pop(0)
                
                # Detect wave pattern
                if len(self.movement_buffer) >= 6 and self.wave_cooldown <= 0:
                    # Check for significant left-right movement
                    total_movement = sum(abs(m) for m in self.movement_buffer)
                    direction_changes = sum(1 for i in range(1, len(self.movement_buffer)) 
                                          if self.movement_buffer[i-1] * self.movement_buffer[i] < 0)
                    
                    if total_movement > 0.3 and direction_changes >= 2:
                        self.wave_detected = True
                        self.wave_cooldown = 30
                        self.movement_buffer.clear()
                        return True
            
            self.last_x = current_x
        
        # Cooldown management
        if self.wave_cooldown > 0:
            self.wave_cooldown -= 1
        
        return False

def play_audio_file_non_blocking(keyword):
    """Play audio file in a separate thread without blocking"""
    def audio_player(keyword):
        global audio_playing, last_voice_time
        audio_playing = True
        
        file_path = audio_data.get(keyword)
        if file_path and os.path.exists(file_path):
            try:
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                print(f"🔊 Playing audio: {keyword}")
                
                # Wait for audio to finish playing without blocking main thread
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                    # Update last voice time during playback to prevent sleep
                    last_voice_time = time.time()
                
            except Exception as e:
                print(f"Error playing audio: {e}")
            finally:
                audio_playing = False
        else:
            print(f"Audio file not found: {file_path}")
            audio_playing = False
    
    # Start audio playback in a separate thread
    audio_thread = threading.Thread(target=audio_player, args=(keyword,), daemon=True)
    audio_thread.start()
    return True

def speak_audio_only(text):
    """Speak using only audio files - no TTS"""
    print(f"🤖 SAARA: {text}")
    
    # Update last voice time
    global last_voice_time
    last_voice_time = time.time()
    
    # Convert text to lowercase for matching
    text_lower = text.lower()
    
    # Check if any audio file keyword exists in the text
    matched_keyword = None
    for keyword in sorted(audio_data.keys(), key=lambda x: -len(x)):
        if keyword in text_lower:
            matched_keyword = keyword
            break
    
    # If audio file exists, play it in non-blocking mode
    if matched_keyword:
        return play_audio_file_non_blocking(matched_keyword)
    else:
        # Fallback to not_understood audio
        return play_audio_file_non_blocking("not_understood")

def draw_clean_visuals(frame, tracker, voice_active):
    """Draw only visual elements without any text"""
    global pulse_effect, audio_playing
    
    pulse_effect = (pulse_effect + 0.1) % (2 * math.pi)
    pulse_value = int(30 + 20 * math.sin(pulse_effect))
    
    # Draw hand landmarks if detected
    if tracker.results.multi_hand_landmarks:
        # Get wrist position for visualization
        wrist_pos = tracker.get_wrist_position()
        if wrist_pos:
            h, w, c = frame.shape
            cx, cy = int(wrist_pos[0] * w), int(wrist_pos[1] * h)
            
            # Draw wrist point
            cv2.circle(frame, (cx, cy), 15, COLORS['secondary'], -1, cv2.LINE_AA)
            cv2.circle(frame, (cx, cy), 8, (255, 255, 255), -1, cv2.LINE_AA)
            
            # Draw wave detection indicator
            if tracker.wave_detected:
                cv2.circle(frame, (cx, cy), 25, COLORS['success'], 3, cv2.LINE_AA)
    
    # Status indicator
    if audio_playing:
        status_text = "Playing Audio..."
        status_color = COLORS['warning']
    elif voice_active:
        status_text = "Voice Active"
        status_color = COLORS['accent']
    else:
        status_text = "Wave to Activate"
        status_color = COLORS['primary']
        
    cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
    
    # Wave detection status
    if tracker.wave_detected:
        cv2.putText(frame, "WAVE DETECTED!", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, COLORS['success'], 2)
    
    # Countdown timer display when voice assistant is active
    if voice_active and not audio_playing:
        time_remaining = SILENCE_TIMEOUT - (time.time() - last_voice_time)
        if time_remaining > 0:
            countdown_text = f"Sleep in: {int(time_remaining)}s"
            cv2.putText(frame, countdown_text, (10, 90), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS['warning'], 2)
    
    # Audio playing indicator
    if audio_playing:
        cv2.putText(frame, "Audio Playing...", (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLORS['secondary'], 2)
    
    return frame

def open_software(software_name):
    software_name_lower = software_name.lower()
    
    if 'chrome' in software_name_lower:
        speak_audio_only("Opening Chrome")
        program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        subprocess.Popen([program])

    elif 'microsoft edge' in software_name_lower:
        speak_audio_only("Opening Microsoft Edge")
        program = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        subprocess.Popen([program])

    elif 'play' in software_name_lower:
        query = software_name_lower.replace('play', '').strip()
        if query:
            speak_audio_only(f'Playing {query} on YouTube')
            pywhatkit.playonyt(query)
        else:
            speak_audio_only("What would you like me to play on YouTube?")

    elif 'notepad' in software_name_lower:
        speak_audio_only('Opening Notepad')
        subprocess.Popen(['notepad.exe']) 
        
    elif 'calculator' in software_name_lower:
        speak_audio_only('Opening Calculator')
        subprocess.Popen(['calc.exe'])
        
    else:
        speak_audio_only(f"I couldn't find the software {software_name}")

def close_software(software_name):
    software_name_lower = software_name.lower()
    
    if 'chrome' in software_name_lower:
        speak_audio_only('Closing Chrome')
        os.system("taskkill /f /im chrome.exe")

    elif 'microsoft edge' in software_name_lower:
        speak_audio_only('Closing Microsoft Edge')
        os.system("taskkill /f /im msedge.exe")

    elif 'notepad' in software_name_lower:
        speak_audio_only('Closing Notepad')
        os.system("taskkill /f /im notepad.exe")
        
    elif 'calculator' in software_name_lower:
        speak_audio_only('Closing Calculator')
        os.system("taskkill /f /im calculator.exe")
        
    else:
        speak_audio_only(f"I couldn't find any open software named {software_name}")

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

def process_question(command):
    """Process questions and provide appropriate responses"""
    command_lower = command.lower()
    
    # Check for question patterns and provide appropriate responses
    for question_pattern, response in QUESTION_RESPONSES.items():
        if question_pattern in command_lower:
            if response in audio_data:  # If response is an audio file key
                speak_audio_only(f"Let me tell you about {response}")
                if play_audio_file_non_blocking(response):
                    return True
                else:
                    speak_audio_only(f"I have information about {response}")
                    return True
            else:  # If response is a text response
                speak_audio_only(response)
                return True
    
    return False

def get_voice_command():
    """Listen for voice command and return text"""
    global audio_playing
    
    # Don't listen if audio is currently playing
    if audio_playing:
        return None
        
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('\n🎤 Listening for your command...')
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        
        try:
            recorded_audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            text = recognizer.recognize_google(recorded_audio, language='en_US')
            text = text.lower()
            print(f'👤 You said: {text}')
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("🔇 Could not understand audio")
            return None
        except Exception as ex:
            print(f"Error: {ex}")
            return None

def process_command(text):
    """Process the command and provide intelligent responses"""
    if not text:
        return True
    
    text_lower = text.lower()
    print(f"🎯 Processing: {text_lower}")
    
    # Update last voice time
    global last_voice_time
    last_voice_time = time.time()
    
    # First, try to process as a question
    if process_question(text):
        return True
    
    # Check for direct audio file keywords
    audio_match = find_best_audio_match(text)
    if audio_match:
        speak_audio_only(f"Let me provide information about {audio_match}")
        if play_audio_file_non_blocking(audio_match):
            return True
    
    # Process other commands
    if any(word in text_lower for word in ['stop', 'exit', 'goodbye', 'bye', 'quit']):
        play_audio_file_non_blocking("goodbye")
        return False
        
    elif 'open' in text_lower:
        software_name = text_lower.replace('open', '').strip()
        open_software(software_name)
        
    elif 'close' in text_lower:
        software_name = text_lower.replace('close', '').strip()
        close_software(software_name)
        
    elif 'time' in text_lower:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak_audio_only(f"The current time is {current_time}")
        
    elif 'date' in text_lower:
        current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
        speak_audio_only(f"Today is {current_date}")
        
    elif 'who is god' in text_lower:
        speak_audio_only('Ajitheyyy Kadavuleyy')
        
    else:
        # If no specific command matched
        play_audio_file_non_blocking("not_understood")
    
    return True

def check_silence_timeout():
    """Check if voice assistant should go to sleep due to silence"""
    global last_voice_time, voice_assistant_active, greeting_played, audio_playing
    
    # Don't sleep if audio is currently playing
    if audio_playing:
        return False
        
    if voice_assistant_active and (time.time() - last_voice_time > SILENCE_TIMEOUT):
        print("⏰ 2 minutes of silence detected - going to sleep")
        play_audio_file_non_blocking("sleep")
        voice_assistant_active = False
        greeting_played = False
        return True
    return False

def voice_assistant_mode():
    """Run the voice assistant after wake word activation"""
    global wake_word_activated, voice_assistant_active, greeting_played, audio_playing
    
    voice_assistant_active = True
    greeting_played = True
    
    print("\n" + "=" * 60)
    print("🎓 SAARA - Voice Assistant Activated")
    print("=" * 60)
    print("💡 You can ask me about:")
    print("• College courses and departments")
    print("• Campus facilities") 
    print("• Opening applications")
    print("• Time and date")
    print("⏰ I will automatically sleep after 2 minutes of silence")
    print("🔊 I will listen for next question after audio finishes")
    print("=" * 60)
    
    # Play greeting audio only once when activated
    play_audio_file_non_blocking("greeting")
    
    while voice_assistant_active and wake_word_activated:
        # Check for silence timeout
        if check_silence_timeout():
            break
        
        # Don't listen for commands while audio is playing
        if audio_playing:
            time.sleep(0.5)
            continue
            
        command = get_voice_command()
        if command:
            if not process_command(command):
                voice_assistant_active = False
                break
        else:
            # If no command received, continue listening
            # Show time remaining until sleep
            time_remaining = SILENCE_TIMEOUT - (time.time() - last_voice_time)
            if time_remaining % 30 == 0 and time_remaining > 30:  # Print every 30 seconds
                print(f"⏰ {int(time_remaining)} seconds until sleep...")
            time.sleep(0.5)

    # When exiting voice mode, reset states
    voice_assistant_active = False
    greeting_played = False
    print("🔇 Voice assistant going to sleep...")

# Initialize MediaPipe hand tracker
hand_tracker = HandTracker()

print("🤖 Hand Gesture System Started")
print("👉 Show your hand to the camera") 
print("👋 Wave your hand to activate SAARA voice assistant!")
print("⏰ Voice assistant will sleep after 2 minutes of silence")
print("🔊 Assistant will listen for next question after each audio finishes")

# Main loop
while True:
    ret, img = webcam.read()
    if not ret:
        break

    img = cv2.flip(img, 1)
    
    # Detect hands using MediaPipe
    img = hand_tracker.find_hands(img)
    
    # Detect wave gesture
    wave_detected = hand_tracker.detect_wave()
    
    # Handle wake word activation via waving
    if wave_detected and not voice_assistant_active:
        print("🎉 Wave detected! Activating SAARA voice assistant...")
        wake_word_activated = True
        # Start voice assistant in a separate thread to not block camera
        assistant_thread = threading.Thread(target=voice_assistant_mode, daemon=True)
        assistant_thread.start()
    
    # Check silence timeout in voice assistant mode
    if voice_assistant_active:
        check_silence_timeout()
    
    # Draw clean visuals with status indicator
    img = draw_clean_visuals(img, hand_tracker, voice_assistant_active)
    
    # Show camera feed
    cv2.imshow("SAARA - Wave to Activate", img)
    
    # Key controls
    key = cv2.waitKey(10) & 0xFF
    if key == 27:  # ESC to exit
        print("👋 Exiting application...")
        break
    elif key == ord('r'):  # Reset detection
        wake_word_activated = False
        voice_assistant_active = False
        greeting_played = False
        print("🔄 Detection reset")

# Cleanup
webcam.release()
cv2.destroyAllWindows()
print("✅ Application closed")