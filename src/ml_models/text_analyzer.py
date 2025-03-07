"""
text_analyzer.py

This module adds machine learning capabilities to our document processor:
- Feature extraction from text
- Document classification
- Basic text analysis using sklearn
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentAnalyzer:
    """
    Analyzes documents using various ML techniques.
    This is where we'll implement different ML models to understand our documents.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features = 1000, # Limit features to most important words
            stop_words = 'english', # Remove common English words
            ngram_range = (1, 2) # Use both single words and pair of words
        )

        # Initialize the model
        self.classifier_rf = RandomForestClassifier(n_estimators=100)
        self.classifier_lr = LogisticRegression(max_iter=1000)
    
    def compare_documents(self, doc1_text: str, doc2_text: str, doc1_name: str, doc2_name: str):
        """
        Compares two documents and visualizes their differences.
        Think of this like having two documents side by side and noting their unique characteristics.
        """

        # Get basic features for both documents
        doc1_features = self.extract_features(doc1_text)
        doc2_features = self.extract_features(doc2_text)

        # Get important words using TF-IDF
        combined_texts = [doc1_text, doc2_text]
        tfidf_matrix = self.vectorizer.fit_transform(combined_texts)
        feature_names = self.vectorizer.get_feature_names_out()

        # Create visualizations
        self._plot_word_importance(tfidf_matrix, feature_names, [doc1_name, doc2_name])
        self._plot_feature_comparison(doc1_features, doc2_features, doc1_name, doc2_name)

        return {
            'document_comparison': {
                doc1_name: {
                    'features': doc1_features,
                    'top_words': self._get_top_words(doc1_text, 10)
                },
                doc2_name: {
                    'features': doc2_features,
                    'top_words': self._get_top_words(doc2_text, 10)
                }
            }
        }
    
    def _plot_word_importance(self, tfidf_matrix, feature_names, doc_names):
        """
        Creates a heatmap showing the most important words in each document.
        """
        plt.figure(figsize=(12,8))

        # Get top 15 words for visualization
        importance_scores = np.array(tfidf_matrix.toarray())
        top_word_indices = importance_scores.sum(axis=0).argsort()[-15:]
        top_words = [feature_names[i] for i in top_word_indices]

        # Create heatmap
        sns.heatmap(
            importance_scores[:, top_word_indices],
            xticklabels=top_words,
            yticklabels=doc_names,
            cmap='YlOrRd'
        )

        plt.title('Most Important Words in Each Document')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('word_importance.png')
        plt.close()
    
    def _plot_feature_comparison(self, features1, features2, name1, name2):
        """
        Creates a bar chart comparing document features.
        """

        plt.figure(figsize=(10, 6))

        # Prepare data for visualization
        features = pd.DataFrame({
            name1: list(features1.values()),
            name2: list(features2.values())
        }, index=list(features1.keys()))

        # Create grouped bar chart
        features.plot(kind='bar')
        plt.title('Document Feature Comparison')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('feature_comparison.png')
        plt.close()

    def _get_top_words(self, text: str, n: int = 10) -> list:
        """
        Gets the most frequent meaningful words in a text.
        """

        words = text.lower().split()
        word_counts = Counter(words)

        # Remove common English words
        stop_words = set(['the', 'and', 'is', 'in', 'to', 'of', 'a', 'for'])
        meaningful_words = [(word, count) for word, count in word_counts.items()
                            if word not in stop_words and len(word) > 2]
        
        return sorted(meaningful_words, key=lambda x: x[1], reverse=True)[:n]

    def extract_features(self, text: str) -> dict:
        """
        Extract basic features from text that might indicate document type.
        """
        features = {
            'word_count': len(text.split()),
            'avg_word_length': np.mean([len(word) for word in text.split()]),
            'number_count': sum(c.isdigit() for c in text) / len(text) if text else 0,
            'uppercase_ratio': sum(c.isupper() for c in text) / len(text) if text else 0
        }

        return features

    def analyze_document(self, text: str) -> dict:
        """
        Perform comprehensive document analysis.
        """

        # Extract basic features from text
        features = self.extract_features(text)

        # Perform keyword extraction using TF-IDF
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text])
            feature_names = self.vectorizer.get_feature_names_out()

            # Take top keywords based on TF-IDF
            tfidf_scores = tfidf_matrix.toarray()[0]
            top_indices = tfidf_scores.argsort()[-10:][::-1]
            top_keywords = [(feature_names[i], tfidf_scores[i]) for i in top_indices]

            analysis_result = {
                'basic_features': features,
                'top_keywords': top_keywords,
                'estimated_reading_time': features['word_count'] / 200,
                'complexity_score': self._calculate_complexity(text)
            }

            return analysis_result
        except Exception as e:
            logger.error(f"Error during document analysis: {str(e)}")
            raise
    
    def _calculate_complexity(self, text: str) -> float:
        """
        Calculate complexity of a document.
        Higher score indicates more complex text.
        """
        sentences = text.split('.')
        avg_sentence_length = np.mean([len(s.split()) for s in sentences if s.strip()])
        unique_words = len(set(text.lower().split()))
        total_words = len(text.split())

        # Combine metrics into a single complexity score
        complexity = (avg_sentence_length * 0.5 +
                     (unique_words / total_words) * 100)
        
        return round(complexity, 2)