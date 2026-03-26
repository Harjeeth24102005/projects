# Import necessary libraries
import cv2  # OpenCV for image/video processing
import mediapipe as mp  # MediaPipe for hand detection and tracking

# Define a class for hand tracking using MediaPipe
class HandTracker:
    def __init__(self):
        # Initialize MediaPipe Hands module
        self.mp_hands = mp.solutions.hands
        
        # Configure the Hands module (only 10 hand, with detection and tracking confidence)
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,         # Use continuous detection from video stream
            max_num_hands=3,                 # Detect only one hand
            min_detection_confidence=0.7,    # Minimum confidence for detecting a hand
            min_tracking_confidence=0.7      # Minimum confidence for tracking the hand
        )
        
        # Utility for drawing hand landmarks
        self.mp_draw = mp.solutions.drawing_utils

    # Method to detect hands and draw landmarks
    def find_hands(self, img):
        # Convert BGR (OpenCV default) to RGB (MediaPipe requirement)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the RGB image and detect hands
        self.results = self.hands.process(img_rgb)

        # If any hand is detected
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                # Draw hand landmarks and connections on the original image
                self.mp_draw.draw_landmarks(
                    img,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        
        # Return the image with landmarks drawn
        return img

    # Method to get wrist position (landmark 0)
    def get_wrist_position(self):
        # If hand landmarks are detected
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]  # Take the first detected hand
            wrist = hand.landmark[0]  # Landmark 0 is the wrist
            return wrist.x, wrist.y   # Return normalized coordinates (between 0 and 1)
        
        # If no hand detected, return None
        return None

# Main function to run the wave detection logic
def main():
    # Open webcam (0 is usually the default camera)
    cap = cv2.VideoCapture(0)
    
    # Create an instance of the hand tracker
    tracker = HandTracker()

    # Variables for wave detection
    last_x = None               # Previous x-position of the wrist
    movement_buffer = []        # Stores recent horizontal movements
    wave_detected = False       # Flag to indicate if a wave has been detected
    wave_cooldown = 0           # Cooldown counter to prevent repeated detection

    print("Wave detection started. Wave your hand to activate command.")

    # Main loop
    while True:
        # Read frame from the webcam
        success, img = cap.read()
        if not success:
            break  # Exit if frame not read properly

        # Flip image horizontally (mirror effect)
        img = cv2.flip(img, 1)

        # Detect hands and draw landmarks
        img = tracker.find_hands(img)

        # Get wrist position from detected hand
        wrist_pos = tracker.get_wrist_position()

        if wrist_pos:
            current_x, current_y = wrist_pos  # Get current wrist x and y

            # If we have a previous x-position
            if last_x is not None:
                # Calculate movement (difference in x)
                movement = current_x - last_x

                # Add movement to buffer
                movement_buffer.append(movement)

                # Keep only the most recent 8 movements
                if len(movement_buffer) > 8:
                    movement_buffer.pop(0)

                # Detect wave pattern if enough movement data and cooldown expired
                if len(movement_buffer) >= 6 and wave_cooldown <= 0:
                    # Sum of absolute movements (how much total movement occurred)
                    total_movement = sum(abs(m) for m in movement_buffer)

                    # Count how many times the direction of movement changed (sign flip)
                    direction_changes = sum(
                        1 for i in range(1, len(movement_buffer))
                        if movement_buffer[i - 1] * movement_buffer[i] < 0
                    )

                    # Check if it's a "wave" pattern:
                    # Enough total movement + back-and-forth motion
                    if total_movement > 0.3 and direction_changes >= 2:
                        wave_detected = True
                        wave_cooldown = 30  # Set cooldown (30 frames)
                        print("Hi! 👋")  # Trigger command (wave detected)
                        movement_buffer.clear()  # Reset buffer

            # Update last_x for next frame
            last_x = current_x

        # Decrease cooldown every frame
        if wave_cooldown > 0:
            wave_cooldown -= 1

            # Show "Command Activated!" message on screen
            cv2.putText(img, "Command Activated!", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Show the video frame
        cv2.imshow("Wave Detection", img)

        # Break loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup: release webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Run the main function if script is executed
if __name__ == "__main__":
    main()
