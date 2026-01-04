import cv2
import numpy as np
import math
import pyttsx3
import threading
import time
import csv
from collections import deque

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Constants
KNOWN_WIDTH = 14.0  # Approximate width of human head in cm
INITIAL_DISTANCE = 50.0  # Initial distance to target in cm
FRAME_WIDTH = 640  
FRAME_HEIGHT = 480  
CAMERA_FOV = 60  # Field of view in degrees
TARGET_ANGLE_RANGE = 1  # Precision targeting in degrees
MOVEMENT_THRESHOLD = 5  # Minimum pixel movement
FOCAL_LENGTH_HISTORY_SIZE = 10

# Global variables
lock_target = True
focal_length = None
focal_length_history = deque(maxlen=FOCAL_LENGTH_HISTORY_SIZE)
kalman_filter = None
zoom_level = 1.0
pulse_counter = 0
target_locked = False
target_present = False
last_target_position = None
last_active_time = time.time()
target_status = "Tracking"
data_log = []

# Initialize webcam
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize pyttsx3 engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech rate

# Function to speak asynchronously
def speak_async(text):
    """Speak text in a non-blocking manner."""
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
    kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.008  # Adjusted for smoother tracking
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
    if perceived_width > 0:
        return (known_width * focal_length) / perceived_width
    return 0

def calculate_angle(offset_x, frame_width, camera_fov):
    """Calculate the angle offset from the center."""
    return (offset_x / frame_width) * camera_fov

def draw_advanced_reticle(frame, x, y, size, color, pulse_size, distance):
    """Draw an advanced pulsing reticle at the target position."""
    # Main crosshair
    cv2.line(frame, (x - size, y), (x + size, y), color, 2)
    cv2.line(frame, (x, y - size), (x, y + size), color, 2)
    
    # Outer pulsing circle
    cv2.circle(frame, (x, y), size + pulse_size, color, 1)
    
    # Inner circle (changes color based on distance)
    inner_color = (0, 255, 0) if distance > 100 else (0, 200, 255)  # Green for far, yellow for close
    cv2.circle(frame, (x, y), size // 2, inner_color, 2)
    
    # Corner indicators
    indicator_size = size // 3
    cv2.line(frame, (x - size - indicator_size, y - size), (x - size + indicator_size, y - size), color, 2)
    cv2.line(frame, (x + size - indicator_size, y - size), (x + size + indicator_size, y - size), color, 2)
    cv2.line(frame, (x - size - indicator_size, y + size), (x - size + indicator_size, y + size), color, 2)
    cv2.line(frame, (x + size - indicator_size, y + size), (x + size + indicator_size, y + size), color, 2)

def draw_modern_scope_overlay(frame, mid_x, mid_y, zoom_level, status_text, status_color):
    """Draw a modern scope overlay with grid lines."""
    overlay = np.zeros_like(frame, dtype=np.uint8)
    
    # Calculate scope radius based on zoom
    radius = int(200 / zoom_level)
    
    # Create circular mask for scope view
    mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
    cv2.circle(mask, (mid_x, mid_y), radius, 255, -1)
    
    # Apply vignette effect
    y_coords, x_coords = np.ogrid[:frame.shape[0], :frame.shape[1]]
    dist_from_center = np.sqrt((x_coords - mid_x)**2 + (y_coords - mid_y)**2)
    vignette = 1 - (dist_from_center / (radius * 1.5))
    vignette = np.clip(vignette, 0, 1)
    
    # Apply vignette to each channel
    for i in range(3):
        frame[:,:,i] = frame[:,:,i] * vignette
    
    # Draw scope ring
    cv2.circle(frame, (mid_x, mid_y), radius, (50, 50, 50), 3)
    cv2.circle(frame, (mid_x, mid_y), radius-1, (200, 200, 200), 1)
    
    # Draw grid lines
    grid_color = (100, 100, 100, 100)
    for i in range(-2, 3):
        if i != 0:
            offset = radius // 4 * i
            cv2.line(frame, (mid_x + offset, mid_y - 5), (mid_x + offset, mid_y + 5), grid_color, 1)
            cv2.line(frame, (mid_x - 5, mid_y + offset), (mid_x + 5, mid_y + offset), grid_color, 1)
    
    # Draw center plus
    plus_size = 15
    cv2.line(frame, (mid_x - plus_size, mid_y), (mid_x + plus_size, mid_y), (255, 255, 255), 2)
    cv2.line(frame, (mid_x, mid_y - plus_size), (mid_x, mid_y + plus_size), (255, 255, 255), 2)
    
    # Draw center dot
    cv2.circle(frame, (mid_x, mid_y), 3, (255, 255, 255), -1)
    
    # Status indicator
    cv2.rectangle(frame, (mid_x - 60, mid_y + radius - 30), (mid_x + 60, mid_y + radius - 10), (40, 40, 40), -1)
    cv2.putText(frame, status_text, (mid_x - 55, mid_y + radius - 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 2)
    
    return frame

def draw_hud_info(frame, x, y, distance, angle, target_status, fps):
    """Draw HUD information on the frame."""
    # Transparent background for HUD
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (400, 120), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # HUD text
    hud_text = [
        f"TARGET STATUS: {target_status}",
        f"DISTANCE: {distance:.1f} cm",
        f"ANGLE: {angle:+.1f}°",
        f"ZOOM: {zoom_level:.1f}x",
        f"FPS: {fps:.1f}"
    ]
    
    for i, text in enumerate(hud_text):
        y_pos = 40 + i * 20
        color = (0, 255, 0) if i == 0 and target_status == "LOCKED" else (255, 255, 255)
        cv2.putText(frame, text, (20, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    # Angle indicator bar
    bar_width = 200
    bar_height = 10
    bar_x = FRAME_WIDTH - bar_width - 20
    bar_y = 40
    
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
    
    # Center indicator
    center_x = bar_x + bar_width // 2
    cv2.line(frame, (center_x, bar_y - 5), (center_x, bar_y + bar_height + 5), (255, 255, 255), 2)
    
    # Current angle indicator
    angle_normalized = np.clip(angle / CAMERA_FOV, -1, 1)
    indicator_x = int(center_x + (angle_normalized * (bar_width // 2)))
    indicator_color = (0, 255, 0) if abs(angle) <= TARGET_ANGLE_RANGE else (0, 0, 255)
    cv2.circle(frame, (indicator_x, bar_y + bar_height // 2), 8, indicator_color, -1)
    
    cv2.putText(frame, f"{angle:+.1f}°", (bar_x + bar_width + 10, bar_y + bar_height + 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def log_data(timestamp, x, y, distance, angle, status):
    """Log target data to a CSV file."""
    with open("target_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, x, y, distance, angle, status])

def detect_eyes(face_roi):
    """Detect eyes within a face region."""
    eyes = eye_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20))
    return eyes

# FPS calculation variables
prev_time = time.time()
fps = 0

while True:
    ret, img = webcam.read()
    if not ret:
        print("Failed to grab frame")
        break
    
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if current_time != prev_time else 0
    prev_time = current_time
    
    # Flip frame horizontally for mirror effect
    img = cv2.flip(img, 1)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)  # Improve contrast for better detection
    
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=6, minSize=(40, 40))
    
    mid_x, mid_y = FRAME_WIDTH // 2, FRAME_HEIGHT // 2
    status_text = "SCANNING"
    status_color = (0, 200, 255)  # Yellow
    
    # Select the largest face (closest target)
    nearest_face = None
    max_area = 0
    
    for (x, y, w, h) in faces:
        area = w * h
        if area > max_area:
            max_area = area
            nearest_face = (x, y, w, h)
    
    if nearest_face is not None:
        (x, y, w, h) = nearest_face
        
        # Draw face bounding box (semi-transparent)
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 200, 255), 2)
        cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)
        
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
            # Target forehead position (top 1/3 of face)
            forehead_x = x + w // 2
            forehead_y = y + h // 4  # Adjusted to be higher on forehead
            
            # Detect eyes for better accuracy
            face_roi = gray[y:y+h, x:x+w]
            eyes = detect_eyes(face_roi)
            
            if len(eyes) > 0:
                # Smooth movement using Kalman filter
                forehead_x, forehead_y = update_kalman_filter(kalman_filter, forehead_x, forehead_y)
                
                # Pulsing effect
                pulse_size = int(5 + 5 * math.sin(pulse_counter * 0.1))
                pulse_counter += 1
                
                # Draw advanced reticle
                draw_advanced_reticle(img, forehead_x, forehead_y, 20, (0, 255, 0), pulse_size, distance)
                
                # Calculate angle offset
                offset_x = forehead_x - mid_x
                angle = calculate_angle(offset_x, FRAME_WIDTH, CAMERA_FOV)
                
                # Draw guiding line to center
                cv2.line(img, (forehead_x, forehead_y), (mid_x, mid_y), (0, 100, 255), 2)
                
                # Check if target is aligned
                if -TARGET_ANGLE_RANGE <= angle <= TARGET_ANGLE_RANGE:
                    status_text = "LOCKED"
                    status_color = (0, 255, 0)  # Green
                    
                    # Flashing "READY" indicator
                    flash_intensity = int(255 * abs(math.sin(pulse_counter * 0.3)))
                    ready_text = "READY"
                    text_size = cv2.getTextSize(ready_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 3)[0]
                    text_x = mid_x - text_size[0] // 2
                    text_y = mid_y + 80
                    
                    # Background for text
                    cv2.rectangle(img, (text_x - 10, text_y - 30), 
                                 (text_x + text_size[0] + 10, text_y + 10), (0, 0, 0), -1)
                    
                    # Flashing text
                    cv2.putText(img, ready_text, (text_x, text_y), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (flash_intensity, 255, flash_intensity), 3)
                    
                    # Voice feedback when first locked
                    if not target_locked:
                        speak_async("Target locked and ready")
                        target_locked = True
                else:
                    if target_locked:
                        speak_async("Target lost")
                    target_locked = False
                    status_text = "TRACKING"
                    status_color = (0, 200, 255)  # Yellow
                
                # Track target movement
                current_position = (forehead_x, forehead_y)
                if last_target_position is not None:
                    movement = math.hypot(current_position[0] - last_target_position[0], 
                                          current_position[1] - last_target_position[1])
                    if movement > MOVEMENT_THRESHOLD:
                        last_active_time = current_time
                        target_status = "ACTIVE"
                    else:
                        target_status = "STABLE"
                else:
                    target_status = "DETECTED"
                
                last_target_position = current_position
                
                # Log target data
                log_data(current_time, forehead_x, forehead_y, distance, angle, target_status)
                
                # Voice feedback for new target
                if not target_present:
                    speak_async("Target acquired")
                    target_present = True
            else:
                target_status = "NO EYES DETECTED"
                status_text = "SEARCHING"
                status_color = (0, 100, 255)  # Orange
        else:
            target_status = "MANUAL MODE"
            status_text = "MANUAL"
            status_color = (255, 100, 0)  # Blue
    else:
        target_present = False
        target_locked = False
        target_status = "NO TARGET"
        status_text = "SCANNING"
        status_color = (0, 200, 255)  # Yellow
    
    # Draw modern scope overlay
    img = draw_modern_scope_overlay(img, mid_x, mid_y, zoom_level, status_text, status_color)
    
    # Draw HUD information
    if nearest_face is not None and 'angle' in locals():
        draw_hud_info(img, forehead_x, forehead_y, distance, angle, target_status, fps)
    else:
        draw_hud_info(img, 0, 0, 0, 0, target_status, fps)
    
    # Display FPS in corner
    cv2.putText(img, f"FPS: {fps:.1f}", (FRAME_WIDTH - 100, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Show the scope UI
    cv2.imshow("🔫 Advanced Aiming System", img)
    
    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('+') or key == ord('='):  # Zoom in
        zoom_level = min(zoom_level + 0.1, 3.0)
    elif key == ord('-') or key == ord('_'):  # Zoom out
        zoom_level = max(zoom_level - 0.1, 0.5)
    elif key == ord('l'):  # Toggle lock target
        lock_target = not lock_target
        speak_async("Auto lock " + ("enabled" if lock_target else "disabled"))
    elif key == ord('r'):  # Reset focal length
        focal_length = None
        focal_length_history.clear()
        speak_async("Focal length reset")
    elif key == ord(' '):  # Space for manual fire command
        if target_locked:
            speak_async("Fire!")
            # Visual fire effect
            fire_overlay = img.copy()
            cv2.circle(fire_overlay, (mid_x, mid_y), 50, (0, 0, 255), -1)
            cv2.addWeighted(fire_overlay, 0.3, img, 0.7, 0, img)
            cv2.imshow("🔫 Advanced Aiming System", img)
            cv2.waitKey(100)
    elif key == 27:  # ESC to exit
        speak_async("System shutting down")
        break

# Release resources
webcam.release()
cv2.destroyAllWindows()
print("System terminated.")
