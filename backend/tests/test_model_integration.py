import os
import pytest
import joblib
import numpy as np
from typing import Dict, Any
from fastapi.testclient import TestClient
from app.main import app

# Path to model artifacts uses environment variable
MODEL_PATH = os.getenv('MODEL_PATH', 'model_artifacts')


def test_model_artifacts_loaded():
    """Test that all model artifacts can be loaded and have expected interfaces."""
    artifacts = {
        'vectorizer': ('tfidf_vectorizer.joblib', 'transform'),
        'classifier': ('career_classifier.joblib', 'predict'),
        'regressor': ('confidence_regressor.joblib', 'predict'),
    }
    
    for name, (filename, method) in artifacts.items():
        path = os.path.join(MODEL_PATH, filename)
        assert os.path.exists(path), f"{name} not found at {path}"
        
        model = joblib.load(path)
        assert hasattr(model, method), f"{name} missing required method {method}"


def test_vectorizer_output_shape():
    """Test TF-IDF vectorizer produces consistent feature dimensionality."""
    vec_path = os.path.join(MODEL_PATH, 'tfidf_vectorizer.joblib')
    vectorizer = joblib.load(vec_path)
    
    # Test various input texts
    texts = [
        "python machine learning data science",
        "",  # empty text should work
        "Python; ML; SQL",  # semicolon separated
        "Python,ML,SQL",  # comma separated
        "PYTHON ML SQL",  # uppercase
    ]
    
    # All transforms should produce same number of features
    shapes = []
    for text in texts:
        X = vectorizer.transform([text])
        shapes.append(X.shape[1])
    
    assert len(set(shapes)) == 1, "Vectorizer produced inconsistent feature dimensions"
    assert shapes[0] > 0, "Vectorizer produced empty feature set"


def test_classifier_prediction_types():
    """Test classifier produces valid career predictions for various inputs."""
    clf_path = os.path.join(MODEL_PATH, 'career_classifier.joblib')
    classifier = joblib.load(clf_path)
    
    # Test with zero and random feature vectors
    n_features = 100
    test_inputs = [
        np.zeros((1, n_features)),
        np.ones((1, n_features)),
        np.random.rand(1, n_features),
        np.random.rand(5, n_features),  # batch prediction
    ]
    
    for X in test_inputs:
        pred = classifier.predict(X)
        assert pred.shape[0] == X.shape[0], "Prediction length mismatch"
        assert all(isinstance(p, str) for p in pred), "Non-string prediction"


def test_regressor_confidence_bounds():
    """Test regressor produces valid confidence scores in [0,1]."""
    reg_path = os.path.join(MODEL_PATH, 'confidence_regressor.joblib')
    regressor = joblib.load(reg_path)
    
    # Test with zero, ones, and random features
    n_features = 100
    test_inputs = [
        np.zeros((1, n_features)),
        np.ones((1, n_features)),
        np.random.rand(1, n_features),
        np.random.rand(5, n_features),  # batch prediction
    ]
    
    for X in test_inputs:
        conf = regressor.predict(X)
        assert conf.shape[0] == X.shape[0], "Confidence score length mismatch"
        assert np.all((conf >= 0) & (conf <= 1)), "Confidence scores outside [0,1]"


@pytest.mark.parametrize("input_data,expected_fields", [
    (
        {
            # Full valid input
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
        {
            "Best-Fit Career Domain": str,
            "Confidence Score": float,
            "Career Rationale": str,
            "5-Year Career Growth Roadmap": str,
            "Skill Gap Analysis": str,
            "Recommended Tools, Courses, and Certifications": str,
            "Alternative/Backup Career Option": str,
            "Behavioral Insight": str
        }
    ),
    (
        {
            # Minimal valid input
            "Education Level": "High School",
            "Academic Performance": "3.0",
            "skills": ""
        },
        {
            "Best-Fit Career Domain": str,
            "Confidence Score": float
        }
    )
])
def test_predict_endpoint_output_types(client: TestClient, input_data: Dict[str, Any], expected_fields: Dict[str, type]):
    """Test /api/predict endpoint produces correctly typed outputs."""
    response = client.post("/api/predict", json=input_data)
    assert response.status_code == 200
    
    data = response.json()
    for field, expected_type in expected_fields.items():
        assert field in data, f"Missing field {field}"
        assert isinstance(data[field], (expected_type, type(None))), \
            f"Field {field} has wrong type: expected {expected_type}, got {type(data[field])}"


@pytest.mark.parametrize("field", [
    "Education Level",
    "Academic Performance"
])
def test_required_fields(client: TestClient, field: str):
    """Test that required fields cannot be omitted."""
    # Start with valid data, remove one required field
    valid_data = {
        "Education Level": "BS Computer Science",
        "Academic Performance": "3.5",
        "skills": "Python"
    }
    
    test_data = valid_data.copy()
    del test_data[field]
    
    response = client.post("/api/predict", json=test_data)
    assert response.status_code == 422, f"Missing {field} should cause validation error"