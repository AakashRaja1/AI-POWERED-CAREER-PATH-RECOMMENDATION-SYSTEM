from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

payload_alias = {
    'User ID': 'u123',
    'Full Name': 'Test Student',
    'Education Level': "Bachelor's",
    'Academic Performance': 'Above average',
    'Skills': 'Python; SQL; Machine Learning',
    'Certifications': '',
    'Do you prefer working with data, people, or ideas?': 'data',
    'How do you approach solving complex problems?': 'Break problems into parts and prototype',
    'Do you thrive better in a structured or flexible environment?': 'structured',
    'Do you prefer working independently or in a team?': 'team',
    'Do you learn best through practice, observation, or theory?': 'practice',
    'Interests': 'AI, data',
    'Extra-Curricular Activities': 'Coding Club'
}

def test_debug_prediction():
    response = client.post('/predict', json=payload_alias)
    assert response.status_code == 200
    print(response.json())