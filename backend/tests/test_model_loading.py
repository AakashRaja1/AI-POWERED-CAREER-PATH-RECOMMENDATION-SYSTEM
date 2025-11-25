import os
import pytest
import joblib
import numpy as np
from fastapi.testclient import TestClient
from app.main import app

# Path to model artifacts uses environment variable
MODEL_PATH = os.getenv('MODEL_PATH', 'model_artifacts')


def test_vectorizer_exists():
    """Test that TF-IDF vectorizer exists and can transform input."""
    vec_path = os.path.join(MODEL_PATH, 'tfidf_vectorizer.joblib')
    assert os.path.exists(vec_path), "TF-IDF vectorizer not found"
    
    vectorizer = joblib.load(vec_path)
    # Test basic transform works
    test_text = "python machine learning data science"
    transformed = vectorizer.transform([test_text])
    assert transformed.shape[1] > 0, "Vectorizer produced empty features"


def test_classifier_exists():
    """Test that classifier exists and can predict."""
    clf_path = os.path.join(MODEL_PATH, 'career_classifier.joblib')
    assert os.path.exists(clf_path), "Classifier not found"
    
    classifier = joblib.load(clf_path)
    # Test predict works with dummy features
    n_features = 100  # adjust based on your vectorizer's vocabulary size
    X = np.zeros((1, n_features))
    pred = classifier.predict(X)
    assert len(pred) == 1, "Classifier prediction failed"


def test_regressor_exists():
    """Test that confidence regressor exists and can predict."""
    reg_path = os.path.join(MODEL_PATH, 'confidence_regressor.joblib')
    assert os.path.exists(reg_path), "Regressor not found"
    
    regressor = joblib.load(reg_path)
    # Test predict works with dummy features
    n_features = 100  # adjust based on your vectorizer's vocabulary size
    X = np.zeros((1, n_features))
    conf = regressor.predict(X)
    assert len(conf) == 1, "Regressor prediction failed"
    assert 0 <= conf[0] <= 1, "Confidence score outside [0,1]"


@pytest.mark.parametrize("input_data,expected_status", [
    (
        {
            "User ID": "TEST_001",
            "Full Name": "Test User",
            "Education Level": "BS Computer Science",
            "Academic Performance": "3.5",
            "skills": "Python; Machine Learning; SQL",
            "Certifications": "AWS Solutions Architect",
            "Do you prefer working with data, people, or ideas?": "data",
            "How do you approach solving complex problems?": "Analytical",
            "Do you thrive better in a structured or flexible environment?": "Flexible",
            "Do you prefer working independently or in a team?": "Independently",
            "Do you learn best through practice, observation, or theory?": "Practice",
            "Interests": "AI; Data Science",
            "Extra-Curricular Activities": "Kaggle competitions",
            "Behavioral Insight": "Analytical mindset"
        },
        200
    ),
    (
        {
            # Minimal valid input
            "User ID": "TEST_002",
            "Full Name": "Min Test",
            "Education Level": "High School",
            "skills": "",  # empty skills should work
            "Academic Performance": "3.0"
        },
        200
    ),
    (
        {
            # Invalid: missing required fields
            "User ID": "TEST_003"
        },
        422
    )
])
def test_predict_endpoint_validation(client: TestClient, input_data, expected_status):
    """Test /api/predict endpoint with various inputs."""
    response = client.post("/api/predict", json=input_data)
    assert response.status_code == expected_status

    if expected_status == 200:
        data = response.json()
        # Check required prediction fields exist
        assert "Best-Fit Career Domain" in data
        assert "Confidence Score" in data
        assert 0 <= data["Confidence Score"] <= 1