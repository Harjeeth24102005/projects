import cv2  # Import the OpenCV library for computer vision tasks

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Initialize video capture from the default webcam (device 0)
webcam = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not webcam.isOpened():
    print("Error: Could not open webcam.")  # Print error message if webcam fails to open
    exit()  # Exit the program

# Start an infinite loop for capturing frames from the webcam
while True:
    # Capture a frame from the webcam
    ret, img = webcam.read()
    
    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read frame.")  # Print error message if frame capture fails
        break  # Break the loop if there is an error

    # Convert the captured image to grayscale for face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image using the Haar Cascade classifier
    faces = face_cascade.detectMultiScale(gray, 1.5, 4)

    # Draw circles around detected faces in the original image
    for (x, y, w, h) in faces:
        # Calculate the center and radius for the circle
        center = (x + w // 2, y + h // 2)  # Center of the face
        radius = int((w + h) // 4)  # Approximate radius (average of width and height)
        cv2.circle(img, center, radius, (0, 255, 0), 3)  # Draw the circle

    # Display the image with circles in a window titled "Face Detection"
    cv2.imshow("Face Detection", img)
    
    # Wait for 10 milliseconds for a key event
    key = cv2.waitKey(10)
    
    # Check if the Escape key (ASCII 27) was pressed
    if key == 27:  # Escape key
        break  # Exit the loop

# Release the webcam resource
webcam.release()
# Close all OpenCV windows
cv2.destroyAllWindows()
