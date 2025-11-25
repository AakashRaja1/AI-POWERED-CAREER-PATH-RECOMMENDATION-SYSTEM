from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

payload_snake = {
    'user_id': 'u123',
    'full_name': 'Test Student',
    'education_level': "Bachelor's",
    'academic_performance': 'Above average',
    'skills': ['Python', 'SQL', 'Machine Learning'],
    'certifications': '',
    'preference_data_people_ideas': 'data',
    'problem_solving_style': 'Break problems into parts and prototype',
    'structured_or_flexible': 'structured',
    'independent_or_team': 'team',
    'learning_style': 'practice',
    'interests': 'AI, data',
    'extra_curricular': 'Coding Club'
}

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


def test_predict_snake_case():
    r = client.post('/api/predict', json=payload_snake)
    assert r.status_code == 200
    j = r.json()
    assert 'Best-Fit Career Domain' in j
    assert 'Confidence Score' in j


def test_predict_alias_keys():
    r = client.post('/api/predict', json=payload_alias)
    assert r.status_code == 200
    j = r.json()
    assert 'Best-Fit Career Domain' in j
    assert 'Confidence Score' in j
