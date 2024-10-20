import cv2

# Load the Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Start capturing video from the webcam
webcam = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    _, img = webcam.read()
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.5, 4)  # Fixed 'dedectMultiScale' to 'detectMultiScale'
    
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
    
    # Display the image with detected faces
    cv2.imshow("Face Detection", img)
    
    # Break the loop if the 'Esc' key is pressed
    key = cv2.waitKey(10)
    if key == 27:
        break

# Release the webcam and close windows
webcam.release()
cv2.destroyAllWindows()
