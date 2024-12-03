from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

class SentimentAnalyzer:
    def __init__(self):
        self.results = []

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        sentiment = blob.sentiment
        polarity = sentiment.polarity
        subjectivity = sentiment.subjectivity

        sentiment_category = self._get_sentiment_category(polarity)
        
        result = {
            "Text": text,
            "Polarity": polarity,
            "Subjectivity": subjectivity,
            "Sentiment": sentiment_category
        }
        self.results.append(result)
        return result

    def _get_sentiment_category(self, polarity):
        if polarity > 0.7:
            return "Very Positive"
        elif polarity > 0.3:
            return "Positive"
        elif polarity > -0.3:
            return "Neutral"
        elif polarity > -0.7:
            return "Negative"
        else:
            return "Very Negative"

    def get_visualization_data(self):
        return pd.DataFrame(self.results)

    def generate_wordcloud(self):
        df = self.get_visualization_data()
        if df.empty:
            return None
        text = ' '.join(df['Text'])
        return WordCloud(width=800, height=400, background_color='white').generate(text)