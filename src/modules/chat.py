from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def create_embeddings(all_text_segments, max_features=5000):
    vectorizer = TfidfVectorizer(max_features=max_features)
    embeddings = vectorizer.fit_transform(all_text_segments)
    return vectorizer, embeddings

def search_with_embeddings(prompt, vectorizer, embeddings, all_text_segments):
    query_vec = vectorizer.transform([prompt])
    similarities = cosine_similarity(query_vec, embeddings).flatten()
    best_match_index = np.argmax(similarities)
    best_match_segment = all_text_segments[best_match_index]
    return best_match_index, best_match_segment