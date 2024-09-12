import random
import pyttsx3
import speech_recognition as sr
engine = pyttsx3.init()
def set_speech_rate(rate=150):
    """Set the speech rate of the TTS engine."""
    engine.setProperty('rate', rate)
def speak(text):
    """Convert the text to speech with the specified rate."""
    set_speech_rate(150)  # Adjust the rate as needed (e.g., 150 words per minute)
    engine.say(text)
    engine.runAndWait()
def get_response(user_input):
    """Generate a response based on user input."""
    responses = {
        "hello": ["Hello!", "Hi there!", "Hey! How can I help you?"],
        "how are you": ["I'm good, thanks for asking!", "I'm doing well, how about you?", "I'm great! How can I assist you today?"],
        "what's the name of this college": ["GOJAN SCHOOL OF BUSINESS AND TECHNOLOGY"],
        "tell me about this college": ["GOJAN SCHOOL OF BUSINESS AND TECHNOLOGY creates a dynamic, optimistic, committed community of educated youth by providing a conducive learning environment at affordable cost and proper training to empower them with leadership potential and employable skills. Providing academic excellence through quality teaching, learning, and research. Fostering and encouraging innovation and creativity by inculcation of entrepreneurial spirit and productive partnership. Creating an environment of intellectual stimulus and scientific inquiry. Creating a hub and a satellite center for learning and research. Recognizing and accepting social responsibility to create a harmonious environment"],
        "what's your name": ["I'm a iri.", "I don't have a name, but you can call me Chatbot.", "You can call me Chatbot."],
        "what are the courses in this college": ["GOJAN SCHOOL OF BUSINESS AND TECHNOLOGY runs Eight Under Graduate Courses (B.E. Aeronautical Engineering, B.E. Computer Science and Engineering, B.E. Electronics and Communication Engineering, B.E – Artificial Intelligence and Machine Learning Engineering, B.E – Cyber Security Engineering, B.E – Medical Electronics Engineering, B.E – Mechanical and Automation Engineering and B.Tech. Information Technology) and Post Graduate Course (M.B.A. Master of Business Administration)."],
        "bye": ["Goodbye. Wishing you a pleasant and productive time ahead.!"]
    }
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return "Sorry, I don't understand that."
def listen():
    """Listen to the user's voice input and return the text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Sorry, there was an error with the speech recognition service.")
            return None
def main():
    """Run the voice assistant."""
    speak("Hello! I am Iris! How can I assist you?")
    while True:
        user_input = listen()
        if user_input:
            if "bye" in user_input.lower():
                speak("Goodbye. Wishing you a pleasant and productive time ahead.!")
                break
            response = get_response(user_input)
            speak(response)
if __name__ == "__main__":
    main()
