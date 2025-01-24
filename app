import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView


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


class ChatbotApp(App):
    def build(self):
        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Scrollable area for chatbot messages
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        
        # Create a BoxLayout to hold the chat messages
        self.chat_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))  # This makes the box grow as new labels are added
        
        self.scroll_view.add_widget(self.chat_box)
        self.layout.add_widget(self.scroll_view)
        
        # Text input field
        self.text_input = TextInput(
            hint_text="Type your message here...",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        self.text_input.bind(on_text_validate=self.on_send)  # Bind Enter key to on_send
        self.layout.add_widget(self.text_input)
        
        # Ensure the cursor is focused on the typing bar at startup
        self.text_input.focus = True
        
        return self.layout

    def on_send(self, instance):
        user_input = self.text_input.text.strip()
        if not user_input:
            return
        
        # Add user message to chat
        user_message = Label(
            text=f"You: {user_input}",
            size_hint_y=None,
            height=40,
            halign="right",  # Right-align user messages
            valign="middle"
        )
        user_message.text_size = (self.text_input.width * 0.8, None)
        self.chat_box.add_widget(user_message)
        
        # Get chatbot's response
        response = get_response(user_input)
        if "bye" in user_input.lower():
            response = "Goodbye!"
        
        # Add chatbot message to chat
        bot_message = Label(
            text=f"Chatbot: {response}",
            size_hint_y=None,
            height=40,
            halign="left",  # Left-align chatbot messages
            valign="middle"
        )
        bot_message.text_size = (self.text_input.width * 0.8, None)
        self.chat_box.add_widget(bot_message)
        
        # Clear text input and keep focus
        self.text_input.text = ""
        self.text_input.focus = True  # Keep the cursor in the typing bar
        
        # Scroll to the latest message
        self.scroll_view.scroll_to(self.chat_box)

        # If "bye" in user input, close the app
        if "bye" in user_input.lower():
            self.stop()


if __name__ == "__main__":
    ChatbotApp().run()
