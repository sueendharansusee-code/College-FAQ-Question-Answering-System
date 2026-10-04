"""
NLP Engine for College FAQ System.
Handles text preprocessing (tokenization, stop words removal, lemmatization) using NLTK,
TF-IDF vectorization, and Cosine Similarity scoring using scikit-learn.
"""

import re
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import database

# NLTK Setup with graceful fallback
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK datasets quietly
for resource in ['punkt', 'stopwords', 'wordnet']:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass

# Fallback English stop words set if NLTK download is restricted
DEFAULT_STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",
    "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
    'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself',
    'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
    'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be',
    'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a',
    'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on',
    'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too',
    'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now'
}

try:
    STOP_WORDS = set(stopwords.words('english'))
except Exception:
    STOP_WORDS = DEFAULT_STOP_WORDS

try:
    LEMMATIZER = WordNetLemmatizer()
except Exception:
    LEMMATIZER = None


def preprocess_text(text):
    """
    Preprocesses raw text query or document:
    1. Lowercasing
    2. Punctuation removal
    3. Tokenization
    4. Stop words filtering
    5. Lemmatization
    """
    if not text:
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove punctuation and numbers
    text = re.sub(r'[' + re.escape(string.punctuation) + r']', ' ', text)
    text = re.sub(r'\d+', ' ', text)

    # 3. Tokenize
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()

    # 4. Filter stop words & short tokens
    cleaned_tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]

    # 5. Lemmatize
    if LEMMATIZER:
        try:
            lemmatized_tokens = [LEMMATIZER.lemmatize(t) for t in cleaned_tokens]
        except Exception:
            lemmatized_tokens = cleaned_tokens
    else:
        lemmatized_tokens = cleaned_tokens

    return " ".join(lemmatized_tokens)


class FAQMatcher:
    """
    FAQ Retrival & Cosine Similarity Matching Engine.
    """
    def __init__(self, confidence_threshold=0.20):
        self.confidence_threshold = confidence_threshold
        self.vectorizer = None
        self.tfidf_matrix = None
        self.faq_list = []
        self.is_indexed = False
        self.reindex()

    def reindex(self):
        """
        Loads all FAQs from SQLite, preprocesses questions & keywords,
        and fits/transforms the TF-IDF Vectorizer.
        """
        print("[NLP Engine] Indexing FAQs into TF-IDF Vectorizer...")
        database.init_db()
        self.faq_list = database.get_all_faqs()

        if not self.faq_list:
            print("[NLP Engine] Warning: No FAQs found in database.")
            self.is_indexed = False
            return

        # Prepare corpus: combine Question + Keywords + Category Name
        corpus = []
        for faq in self.faq_list:
            raw_doc = f"{faq['question']} {faq.get('keywords', '')} {faq.get('category_name', '')}"
            processed_doc = preprocess_text(raw_doc)
            corpus.append(processed_doc)

        # Initialize TF-IDF Vectorizer (unigrams + bigrams for contextual matching)
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.is_indexed = True
        print(f"[NLP Engine] Successfully indexed {len(self.faq_list)} FAQs into TF-IDF matrix.")

    def match(self, user_query):
        """
        Processes a user query and returns the best matching FAQ,
        similarity score, confidence rating, and top candidate suggestions.
        """
        if not user_query or not user_query.strip():
            return {
                "success": False,
                "message": "Please enter a valid question.",
                "similarity_score": 0.0,
                "confidence_level": "None",
                "status": "UNANSWERED"
            }

        if not self.is_indexed or self.tfidf_matrix is None or len(self.faq_list) == 0:
            self.reindex()
            if not self.is_indexed:
                return {
                    "success": False,
                    "message": "Sorry, the FAQ database is currently empty.",
                    "similarity_score": 0.0,
                    "confidence_level": "None",
                    "status": "UNANSWERED"
                }

        # Preprocess user query
        processed_query = preprocess_text(user_query)

        if not processed_query.strip():
            # If query contained only stop words like "What is this?"
            processed_query = user_query.lower()

        # Vectorize query
        query_vector = self.vectorizer.transform([processed_query])

        # Compute Cosine Similarity against all stored FAQ vectors
        cosine_sims = cosine_similarity(query_vector, self.tfidf_matrix)[0]

        # Get best match index and top scores
        best_idx = int(np.argmax(cosine_sims))
        best_score = float(cosine_sims[best_idx])

        # Determine confidence level rating
        if best_score >= 0.70:
            confidence_level = "High"
        elif best_score >= 0.40:
            confidence_level = "Medium"
        elif best_score >= self.confidence_threshold:
            confidence_level = "Low"
        else:
            confidence_level = "Unreliable"

        # Get top 3 candidates for suggested alternatives
        sorted_indices = np.argsort(cosine_sims)[::-1]
        suggestions = []
        for idx in sorted_indices[:3]:
            score = float(cosine_sims[idx])
            if score > 0.05 and idx != best_idx:
                faq_item = self.faq_list[idx]
                suggestions.append({
                    "id": faq_item['id'],
                    "question": faq_item['question'],
                    "category": faq_item['category_name'],
                    "score_percentage": round(score * 100, 1)
                })

        best_faq = self.faq_list[best_idx]
        formatted_score = round(best_score * 100, 1)

        # Check against confidence threshold
        if best_score >= self.confidence_threshold:
            status = "ANSWERED"
            response_payload = {
                "success": True,
                "answer": best_faq['answer'],
                "matched_faq_id": best_faq['id'],
                "matched_question": best_faq['question'],
                "category": best_faq['category_name'],
                "category_icon": best_faq.get('category_icon', 'fa-folder'),
                "similarity_score": best_score,
                "score_percentage": f"{formatted_score}%",
                "confidence_level": confidence_level,
                "preprocessed_tokens": processed_query,
                "status": status,
                "suggestions": suggestions
            }
        else:
            # Fallback when confidence is below threshold
            status = "UNANSWERED"
            response_payload = {
                "success": False,
                "answer": "Sorry, I could not find a reliable answer.",
                "matched_faq_id": None,
                "matched_question": best_faq['question'],
                "category": best_faq['category_name'],
                "similarity_score": best_score,
                "score_percentage": f"{formatted_score}%",
                "confidence_level": confidence_level,
                "preprocessed_tokens": processed_query,
                "status": status,
                "suggestions": suggestions
            }

        # Log query resolution to SQLite query history
        try:
            database.log_query(
                user_query=user_query,
                matched_faq_id=best_faq['id'] if best_score >= self.confidence_threshold else None,
                matched_question=best_faq['question'],
                matched_answer=best_faq['answer'] if best_score >= self.confidence_threshold else "Sorry, I could not find a reliable answer.",
                similarity_score=best_score,
                category_name=best_faq['category_name'],
                status=status
            )
        except Exception as e:
            print(f"[NLP Engine] Warning: Failed to log query history: {e}")

        return response_payload


# Global Singleton Instance
nlp_matcher = FAQMatcher(confidence_threshold=0.20)
