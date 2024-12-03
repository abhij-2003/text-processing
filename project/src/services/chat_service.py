import google.generativeai as gen_ai

class ChatService:
    def __init__(self, api_key):
        gen_ai.configure(api_key=api_key)
        self.model = gen_ai.GenerativeModel('gemini-pro')
        self.chat_session = None

    def start_chat(self):
        """Initialize or reset chat session"""
        self.chat_session = self.model.start_chat(history=[])
        return self.chat_session

    def send_message(self, message):
        """Send message and get response"""
        if not self.chat_session:
            self.start_chat()
        return self.chat_session.send_message(message)

    def get_history(self):
        """Get chat history"""
        return self.chat_session.history if self.chat_session else []