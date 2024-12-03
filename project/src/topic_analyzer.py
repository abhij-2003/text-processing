import re
import nltk
from nltk.corpus import stopwords
from gensim.corpora import Dictionary
from gensim.models import LdaModel, CoherenceModel
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import PyPDF2
import docx2txt

class TopicAnalyzer:
    def __init__(self, num_topics=3):
        self.num_topics = num_topics
        nltk.download('stopwords', quiet=True)
        self.stop_words = set(stopwords.words('english'))

    def extract_text(self, file_path):
        text = ""
        file_extension = file_path.split('.')[-1].lower()

        try:
            if file_extension == 'pdf':
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text()
            elif file_extension == 'txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
            elif file_extension == 'docx':
                text = docx2txt.process(file_path)
            else:
                raise ValueError("Unsupported file type")
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")

        return text

    def preprocess_text(self, text):
        text = re.sub(r'\W', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\d', '', text)
        text = text.lower()
        return ' '.join(word for word in text.split() if word not in self.stop_words)

    def analyze_topics(self, text):
        processed_text = self.preprocess_text(text)
        tokenized_data = [processed_text.split()]
        
        dictionary = Dictionary(tokenized_data)
        corpus = [dictionary.doc2bow(doc) for doc in tokenized_data]

        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=self.num_topics,
            passes=10,
            random_state=42
        )

        topics = lda_model.print_topics(num_topics=self.num_topics, num_words=10)
        coherence_model = CoherenceModel(
            model=lda_model,
            texts=tokenized_data,
            dictionary=dictionary,
            coherence='c_v'
        )

        return {
            'topics': topics,
            'coherence_score': coherence_model.get_coherence(),
            'lda_model': lda_model,
            'dictionary': dictionary
        }