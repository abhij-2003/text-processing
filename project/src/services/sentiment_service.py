from textblob import TextBlob

class SentimentService:
    def __init__(self):
        self.results = []

    def analyze_sentiment(self, text):
        """Analyze the sentiment of the given text."""
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
        """Categorize the sentiment based on polarity score."""
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