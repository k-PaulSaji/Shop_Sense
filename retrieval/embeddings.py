

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SemanticEncoder:
    def __init__(self, texts):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english"
        )
        self.matrix = self.vectorizer.fit_transform(texts)
        self.backend = "TF-IDF"

    def search(self, query, k=5):
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        indices = np.argsort(scores)[::-1][:k]
        return [(int(i), float(scores[i]))
                for i in indices if scores[i] > 0]