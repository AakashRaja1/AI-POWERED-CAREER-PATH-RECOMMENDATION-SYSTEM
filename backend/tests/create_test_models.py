import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Create a simple vectorizer for testing
vectorizer = TfidfVectorizer()
vectorizer.fit_transform(['python machine learning data science'])

# Save it
joblib.dump(vectorizer, 'model_artifacts/tfidf_vectorizer.joblib')