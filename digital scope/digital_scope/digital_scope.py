import cv2
import numpy as np
import math
import pyttsx3
import threading
import time
import csv  # Added csv module import
from collections import deque

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Constants
KNOWN_WIDTH = 14.0  # Approximate width of human head in cm
INITIAL_DISTANCE = 50.0  # Initial distance to target in cm (for focal length calibration)
FRAME_WIDTH = 640  
FRAME_HEIGHT = 480  
CAMERA_FOV = 60  # Field of view of the camera in degrees
TARGET_ANGLE_RANGE = 1  # Precision targeting in degrees
MOVEMENT_THRESHOLD = 5  # Minimum pixel movement to consider the target alive
INACTIVE_TIME_THRESHOLD = 3  # Time in seconds to consider the target dead
FOCAL_LENGTH_HISTORY_SIZE = 10  # Number of measurements for dynamic focal length adjustment

# Global variables
lock_target = True  # Automatically lock target
focal_length = None  # Focal length will be calculated dynamically
focal_length_history = deque(maxlen=FOCAL_LENGTH_HISTORY_SIZE)  # Store focal length history
kalman_filter = None  # Kalman filter for smoother tracking
zoom_level = 1.0  # Default zoom level for the scope overlay
pulse_counter = 0  # Counter for pulsing effect
target_locked = False  # Track if the target is locked
target_present = False  # Track if the target is in the frame
last_target_position = None  # Track the last position of the target
last_active_time = time.time()  # Track the last time the target moved
target_status = "Alive"  # Track the target status (Alive or Dead)
target_priority = 0  # Track the priority of the target (e.g., closest target)
data_log = []  # Log target data for analysis

# Initialize webcam
webcam = cv2.VideoCapture(0)
webcam.set(3, FRAME_WIDTH)
webcam.set(4, FRAME_HEIGHT)

if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to speak asynchronously
def speak_async(text):
    """Speak text in a non-blocking manner using a separate thread."""
    def _speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

# Kalman filter initialization
def init_kalman_filter():
    """Initialize Kalman filter for smoother tracking."""
    kalman = cv2.KalmanFilter(4, 2)
    kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
    kalman.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
    kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.01  # Reduced noise for smoother tracking
    return kalman

kalman_filter = init_kalman_filter()

def update_kalman_filter(kalman, x, y):
    """Update Kalman filter with new measurements."""
    measurement = np.array([[np.float32(x)], [np.float32(y)]])
    kalman.correct(measurement)
    prediction = kalman.predict()
    return int(prediction[0]), int(prediction[1])

def calculate_focal_length(measured_width, known_width, known_distance):
    """Calculate focal length based on initial measurements."""
    return (measured_width * known_distance) / known_width

def calculate_distance(focal_length, known_width, perceived_width):
    """Calculate distance to the target."""
    return (known_width * focal_length) / perceived_width

def calculate_angle(offset_x, frame_width, camera_fov):
    """Calculate the angle offset from the center."""
    return (offset_x / frame_width) * camera_fov

def draw_reticle(frame, x, y, size, color, pulse_size):
    """Draw a pulsing reticle at the target position."""
    cv2.line(frame, (x - size, y), (x + size, y), color, 2)
    cv2.line(frame, (x, y - size), (x, y + size), color, 2)
    cv2.circle(frame, (x, y), size + pulse_size, color, 2)

def draw_scope_overlay(frame, mid_x, mid_y, zoom_level):
    """Draw a zooming scope overlay with a plus in the center."""
    overlay = np.zeros_like(frame, dtype=np.uint8)
    radius = int(200 / zoom_level)  # Adjust radius based on zoom level
    cv2.circle(overlay, (mid_x, mid_y), radius, (0, 0, 0), -1)  # Outer darkened area
    cv2.addWeighted(overlay, 0.4, frame, 1, 0, frame)

    # Draw a plus (+) in the center
    plus_size = 20
    cv2.line(frame, (mid_x - plus_size, mid_y), (mid_x + plus_size, mid_y), (255, 255, 255), 2)
    cv2.line(frame, (mid_x, mid_y - plus_size), (mid_x, mid_y + plus_size), (255, 255, 255), 2)

    return frame

def log_data(target_data):
    """Log target data to a CSV file."""
    with open("target_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(target_data)

def detect_eyes(face_roi):
    """Detect eyes within a face region."""
    eyes = eye_cascade.detectMultiScale(face_roi)
    return eyes

while True:
    ret, img = webcam.read()
    if not ret:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    mid_x, mid_y = FRAME_WIDTH // 2, FRAME_HEIGHT // 2
    status_text = "Not Locked"
    status_color = (0, 0, 255)  # Red (Not Aligned)
    
    # Select the nearest target (largest face, as it is closest to the camera)
    nearest_face = None
    max_area = 0

    for (x, y, w, h) in faces:
        area = w * h  # Area of the detected face
        if area > max_area:
            max_area = area
            nearest_face = (x, y, w, h)

    if nearest_face is not None:
        (x, y, w, h) = nearest_face

        # Calculate focal length on first detection
        if focal_length is None:
            focal_length = calculate_focal_length(w, KNOWN_WIDTH, INITIAL_DISTANCE)
        
        # Update focal length dynamically
        new_focal_length = calculate_focal_length(w, KNOWN_WIDTH, INITIAL_DISTANCE)
        focal_length_history.append(new_focal_length)
        focal_length = np.mean(focal_length_history)
        
        # Estimate distance
        distance = calculate_distance(focal_length, KNOWN_WIDTH, w)
        
        if lock_target:
            # Adjust targeting to the forehead (top 1/3 of the face)
            forehead_x = x + w // 2
            forehead_y = y + h // 3  

            # Detect eyes within the face region
            face_roi = gray[y:y+h, x:x+w]
            eyes = detect_eyes(face_roi)

            # If at least one eye is detected, lock onto the forehead
            if len(eyes) > 0:
                # Smooth movement using Kalman filter
                forehead_x, forehead_y = update_kalman_filter(kalman_filter, forehead_x, forehead_y)

                # Pulsing effect for lock-on
                pulse_size = int(5 + 5 * math.sin(pulse_counter * 0.1))
                pulse_counter += 1  # Increment pulse_counter for the next frame

                # Draw reticle with pulsing effect
                draw_reticle(img, forehead_x, forehead_y, 20, (0, 255, 0), pulse_size)

                # Angle offset
                offset_x = forehead_x - mid_x
                angle = calculate_angle(offset_x, FRAME_WIDTH, CAMERA_FOV)

                # Show guiding line
                cv2.line(img, (forehead_x, forehead_y), (mid_x, mid_y), (0, 0, 255), 2)

                # Scope HUD Text
                hud_text = f"Angle: {angle:.1f}°  |  Distance: {distance:.1f} cm  |  Status: {target_status}"
                cv2.putText(img, hud_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                # Check if "READY TO FIRE"
                if -TARGET_ANGLE_RANGE <= angle <= TARGET_ANGLE_RANGE:
                    status_text = "READY TO FIRE!"
                    status_color = (0, 255, 0)  # Green
                    
                    # Flashing alert inside the scope
                    flash_intensity = int(255 * abs(math.sin(pulse_counter * 0.2)))
                    cv2.putText(img, status_text, (mid_x - 80, mid_y + 100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (flash_intensity, 255, flash_intensity), 3)

                    # Voice feedback when ready to fire
                    if not target_locked:
                        speak_async("Ready to fire.")
                        target_locked = True
                else:
                    target_locked = False  # Reset target lock status

                # Track target movement
                current_position = (forehead_x, forehead_y)
                if last_target_position is not None:
                    movement = math.hypot(current_position[0] - last_target_position[0], 
                                          current_position[1] - last_target_position[1])
                    if movement > MOVEMENT_THRESHOLD:
                        last_active_time = time.time()
                        target_status = "Alive"
                    elif time.time() - last_active_time > INACTIVE_TIME_THRESHOLD:
                        target_status = "Dead"
                        speak_async("Target dead. Moving to next target.")
                        target_locked = False  # Release lock
                        nearest_face = None  # Reset target
                last_target_position = current_position

                # Log target data
                log_data([time.time(), forehead_x, forehead_y, distance, angle, target_status])

                # Voice feedback when target is locked (only when target re-enters the frame)
                if not target_present:
                    speak_async("Target locked.")
                    target_present = True
    else:
        target_present = False  # Target is not in the frame
        target_status = "Unknown"  # Reset target status

    # Add realistic scope overlay
    img = draw_scope_overlay(img, mid_x, mid_y, zoom_level)

    # Show the scope UI
    cv2.imshow("🔫 Aiming System", img)

    # Dynamic zoom control
    key = cv2.waitKey(10)
    if key == ord('+'):  # Press '+' to zoom in
        zoom_level = min(zoom_level + 0.1, 3.0)  # Limit max zoom level
    elif key == ord('-'):  # Press '-' to zoom out
        zoom_level = max(zoom_level - 0.1, 0.5)  # Limit min zoom level
    elif key == 27:  # Press 'ESC' to exit
        break

# Release resources
webcam.release()
cv2.destroyAllWindows()