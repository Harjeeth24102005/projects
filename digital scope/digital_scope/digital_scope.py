import cv2
import numpy as np
import speech_recognition as sr
import threading
import pyttsx3
import math
import time

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Constants
KNOWN_WIDTH = 14.0  # Approximate width of human head in cm
FOCAL_LENGTH = 500  # Estimated focal length (calibrated)
FRAME_WIDTH = 640  
FRAME_HEIGHT = 480  
CAMERA_FOV = 60  
TARGET_ANGLE_RANGE = 1  # Precision targeting

lock_target = False  
ready_to_fire_announced = False  

# Initialize webcam
webcam = cv2.VideoCapture(0)
webcam.set(3, FRAME_WIDTH)
webcam.set(4, FRAME_HEIGHT)

if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Speech recognition setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    """Speak text asynchronously."""
    def run():
        engine = pyttsx3.init()
        engine.setProperty("rate", 110)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()

def listen_for_command():
    """Listen for 'Lock Target' command."""
    global lock_target
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Noise cancellation
    while True:
        with mic as source:
            try:
                audio = recognizer.listen(source, timeout=5)  # Faster response
                command = recognizer.recognize_google(audio).lower()
                if "lock target" in command:
                    lock_target = True
                    speak("Target locked on forehead")
            except (sr.UnknownValueError, sr.RequestError):
                pass

# Start voice command listening in a separate thread
threading.Thread(target=listen_for_command, daemon=True).start()

# Variables for animations
prev_forehead_x, prev_forehead_y = FRAME_WIDTH // 2, FRAME_HEIGHT // 2
animation_speed = 0.2  # Smooth easing effect
pulse_counter = 0

while True:
    ret, img = webcam.read()
    if not ret:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6, minSize=(40, 40))  
    
    mid_x, mid_y = FRAME_WIDTH // 2, FRAME_HEIGHT // 2
    status_text = "Not Locked"
    status_color = (0, 0, 255)  # Red (Not Aligned)
    
    # Select the closest detected face
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    
    for (x, y, w, h) in faces[:1]:  # Only process the largest face
        # Estimate distance
        dynamic_focal_length = (FOCAL_LENGTH * (w / KNOWN_WIDTH))
        distance = (KNOWN_WIDTH * dynamic_focal_length) / w
        
        if lock_target:
            # Adjust targeting to the forehead (top 1/3 of the face)
            forehead_x = x + w // 2
            forehead_y = y + h // 3  

            # Smooth movement for reticle
            prev_forehead_x = int(prev_forehead_x + (forehead_x - prev_forehead_x) * animation_speed)
            prev_forehead_y = int(prev_forehead_y + (forehead_y - prev_forehead_y) * animation_speed)

            # Pulsing effect for lock-on
            pulse_size = int(5 + 5 * math.sin(pulse_counter * 0.1))
            pulse_counter += 1

            # Draw reticle (crosshair)
            cv2.line(img, (mid_x - 40, mid_y), (mid_x + 40, mid_y), (255, 255, 255), 2)
            cv2.line(img, (mid_x, mid_y - 40), (mid_x, mid_y + 40), (255, 255, 255), 2)

            # Target lock indicator
            cv2.circle(img, (prev_forehead_x, prev_forehead_y), 15 + pulse_size, (0, 255, 0), 2)

            # Angle offset
            offset_x = prev_forehead_x - mid_x
            angle = (offset_x / FRAME_WIDTH) * CAMERA_FOV  

            # Show guiding line
            cv2.line(img, (prev_forehead_x, prev_forehead_y), (mid_x, mid_y), (0, 0, 255), 2)

            # Scope HUD Text
            hud_text = f"Angle: {angle:.1f}°  |  Distance: {distance:.1f} cm"
            cv2.putText(img, hud_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Check if "READY TO FIRE"
            if -TARGET_ANGLE_RANGE <= angle <= TARGET_ANGLE_RANGE:
                if not ready_to_fire_announced:
                    speak("Ready to fire")
                    ready_to_fire_announced = True
                status_text = "READY TO FIRE!"
                status_color = (0, 255, 0)  # Green
                
                # Flashing alert inside the scope
                flash_intensity = int(255 * abs(math.sin(pulse_counter * 0.2)))
                cv2.putText(img, status_text, (mid_x - 80, mid_y + 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (flash_intensity, 255, flash_intensity), 3)
            else:
                ready_to_fire_announced = False  

    # Add realistic scope overlay
    overlay = np.zeros_like(img, dtype=np.uint8)
    cv2.circle(overlay, (mid_x, mid_y), 220, (0, 0, 0), -1)  # Outer darkened area
    cv2.addWeighted(overlay, 0.5, img, 1, 0, img)

    # Scope border effect
    cv2.circle(img, (mid_x, mid_y), 220, (255, 255, 255), 3)  
    cv2.line(img, (mid_x - 100, mid_y), (mid_x + 100, mid_y), (255, 255, 255), 2)
    cv2.line(img, (mid_x, mid_y - 100), (mid_x, mid_y + 100), (255, 255, 255), 2)

    # Show the scope UI
    cv2.imshow("🔫 Aiming System", img)

    if cv2.waitKey(10) == 27:  # Press 'ESC' to exit
        break

# Release resources
webcam.release()
cv2.destroyAllWindows()
