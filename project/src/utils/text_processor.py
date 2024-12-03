import re
import nltk
from nltk.corpus import stopwords

class TextProcessor:
    def __init__(self):
        nltk.download('stopwords', quiet=True)
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        """Remove special characters, numbers, and convert to lowercase"""
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\d', '', text)
        return text.lower().strip()

    def remove_stopwords(self, text):
        """Remove common stopwords from text"""
        return ' '.join(word for word in text.split() if word not in self.stop_words)

    def preprocess(self, text):
        """Complete text preprocessing pipeline"""
        text = self.clean_text(text)
        return self.remove_stopwords(text)