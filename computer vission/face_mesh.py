import cv2  # Import OpenCV library for video capture and image processing
import mediapipe as mp  # Import MediaPipe for face mesh detection

cap = cv2.VideoCapture(0)  # Open the default webcam (device 0)
mesh = mp.solutions.face_mesh.FaceMesh()  # Initialize MediaPipe Face Mesh detector
draw = mp.solutions.drawing_utils  # Get drawing utilities for landmarks and connections
spec = draw.DrawingSpec(thickness=1, circle_radius=0)  # Set drawing style: thin lines, no points
conn = mp.solutions.face_mesh.FACEMESH_TESSELATION  # Use predefined face mesh connections (lines)

while True:  # Start an infinite loop to process webcam frames
    ret, img = cap.read()  # Capture a frame from webcam
    if not ret: break  # Exit loop if frame is not captured successfully

    img = cv2.flip(img, 1)  # Flip the frame horizontally for mirror effect
    res = mesh.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB and process frame

    if res.multi_face_landmarks:  # If one or more faces with landmarks detected
        for f in res.multi_face_landmarks:  # Iterate over each detected face
            draw.draw_landmarks(img, f, conn, None, spec)  # Draw mesh lines (no points) on image

    cv2.imshow("Face Mesh", img)  # Display the image with face mesh overlay
    if cv2.waitKey(1) & 0xFF == ord('h'): break  # Exit loop if 'q' key is pressed

cap.release()  # Release webcam resource
cv2.destroyAllWindows()  # Close all OpenCV windows