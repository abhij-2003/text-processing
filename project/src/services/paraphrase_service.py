import google.generativeai as gen_ai

class ParaphraseService:
    def __init__(self, api_key):
        gen_ai.configure(api_key=api_key)
        self.model = gen_ai.GenerativeModel('gemini-pro')
        self.chat_session = None

    def start_session(self):
        """Initialize or reset paraphrase session"""
        self.chat_session = self.model.start_chat(history=[])
        return self.chat_session

    def paraphrase(self, text):
        """Generate paraphrased version of input text"""
        if not self.chat_session:
            self.start_session()
        
        prompt = (
            "Please paraphrase the following text while maintaining its original meaning. "
            "Make it clear and natural, avoiding awkward phrasing:\n\n"
            f"{text}"
        )
        
        response = self.chat_session.send_message(prompt)
        return response.text