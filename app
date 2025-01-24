import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
def get_response(user_input):
    responses = {
        "hi": ["Hello!", "Hi there!", "Hey! How can I help you?"],
        "how are you": ["I'm good, thanks for asking!", "I'm doing well, how about you?", "I'm great! How can I assist you today?"],
        "what's your name": ["I'm a chatbot.", "I don't have a name, but you can call me Chatbot.", "You can call me Chatbot."],
        "bye": ["Have a great day!"]
    }
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return "Sorry, I don't understand that."
class ChatbotApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.layout.add_widget(Label(text="Chatbot Application", size_hint_y=None, height=70, font_size=30, bold=True, halign="center", valign="middle"))
        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.chat_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_box.bind(minimum_height=self.chat_box.setter('height'))
        self.scroll_view.add_widget(self.chat_box)
        self.layout.add_widget(self.scroll_view)
        self.text_input = TextInput(hint_text="Type your message here...", multiline=False, size_hint_y=None, height=50)
        self.text_input.bind(on_text_validate=self.on_send)
        self.layout.add_widget(self.text_input)
        self.text_input.focus = True
        return self.layout
    def on_send(self, instance):
        user_input = self.text_input.text.strip()
        if not user_input:
            return
        self.chat_box.add_widget(Label(text=f"You: {user_input}", size_hint_y=None, height=60, halign="right", valign="middle", font_size=20, text_size=(self.text_input.width * 0.8, None)))
        response = get_response(user_input)
        self.chat_box.add_widget(Label(text=f"Chatbot: {response}", size_hint_y=None, height=60, halign="left", valign="middle", font_size=20, text_size=(self.text_input.width * 0.8, None)))
        if "bye" in user_input.lower():
            Clock.schedule_once(self.stop, 2)
        self.text_input.text = ""
        self.text_input.focus = True
        self.scroll_view.scroll_to(self.chat_box)
if __name__ == "__main__":
    ChatbotApp().run() 
