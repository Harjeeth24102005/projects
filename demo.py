def get_response(user_input):
    responses = {
        "hi": ["Hello!", "Hi there!", "Hey! How can I help you?"],
        "how are you": ["I'm good, thanks for asking!", "I'm doing well, how about you?", "I'm great! How can I assist you today?"],
        "what's your name": ["I'm a chatbot.", "I don't have a name, but you can call me Chatbot.", "You can call me Chatbot."],
        "bye": ["Goodbye!", "See you later!", "Have a great day!"]
    }
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return "Sorry, I don't understand that."
def main():
    print("Chatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if "bye" in user_input.lower():
            print("Chatbot: Goodbye!")
            break
        response = get_response(user_input)
        print(f"Chatbot: {response}")
if __name__ == "__main__":
    main()
