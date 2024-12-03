from gensim.corpora import Dictionary
from gensim.models import LdaModel, CoherenceModel
from utils.text_processor import TextProcessor
import numpy as np

class TopicService:
    def __init__(self, num_topics=3):
        self.num_topics = num_topics
        self.text_processor = TextProcessor()

    def analyze_topics(self, text):
        """Analyze topics in the given text"""
        processed_text = self.text_processor.preprocess(text)
        tokenized_data = [processed_text.split()]
        
        dictionary = Dictionary(tokenized_data)
        corpus = [dictionary.doc2bow(doc) for doc in tokenized_data]

        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=self.num_topics,
            passes=15,
            alpha='auto',
            random_state=42
        )

        coherence_model = CoherenceModel(
            model=lda_model,
            texts=tokenized_data,
            dictionary=dictionary,
            coherence='c_v'
        )

        # Get topic keywords with probabilities
        topics = []
        for topic_id in range(self.num_topics):
            topic_info = {
                'id': topic_id + 1,
                'keywords': [],
                'summary': ''
            }
            
            # Get top keywords for the topic
            word_probs = lda_model.show_topic(topic_id, topn=10)
            topic_info['keywords'] = [
                {'word': word, 'probability': prob} 
                for word, prob in word_probs
            ]
            
            # Generate topic summary
            top_words = [word['word'] for word in topic_info['keywords'][:5]]
            topic_info['summary'] = self._generate_topic_summary(top_words)
            
            topics.append(topic_info)

        dominant_topic = self._get_dominant_topic(lda_model, corpus)
        if dominant_topic:
            # Add summary to dominant topic
            dominant_words = [word['word'] for word in topics[dominant_topic['topic_id']-1]['keywords'][:5]]
            dominant_topic['summary'] = self._generate_topic_summary(dominant_words)

        return {
            'topics': topics,
            'coherence_score': coherence_model.get_coherence(),
            'dominant_topic': dominant_topic
        }

    def _generate_topic_summary(self, top_words):
        """Generate a human-readable summary based on top words"""
        if len(top_words) > 1:
            return f"{', '.join(top_words[:-1])} and {top_words[-1]}"
        return top_words[0] if top_words else ""

    def _get_dominant_topic(self, lda_model, corpus):
        """Identify the dominant topic in the document"""
        if not corpus:
            return None
            
        topic_dist = lda_model.get_document_topics(corpus[0])
        dominant_topic = max(topic_dist, key=lambda x: x[1])
        return {
            'topic_id': dominant_topic[0] + 1,
            'probability': dominant_topic[1]
        }