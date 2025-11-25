import time
from fastapi.testclient import TestClient
from app.main import app

# Ensure database tables exist for tests (creates tables if missing)
from app.database.init_db import init_db


# initialize DB schema for test run
init_db()


client = TestClient(app)


def test_predict_and_persist():
    payload = {
        "User ID": "TEST_PY_001",
        "Full Name": "Py Test",
        "Education Level": "BS Computer Science",
        "Academic Performance": "3.6",
        "skills": "Python; ML; SQL",
        "Certifications": "None",
        "Do you prefer working with data, people, or ideas?": "data",
        "How do you approach solving complex problems?": "Analytical",
        "Do you thrive better in a structured or flexible environment?": "Flexible",
        "Do you prefer working independently or in a team?": "Independently",
        "Do you learn best through practice, observation, or theory?": "Practice",
        "Interests": "AI; Data",
        "Extra-Curricular Activities": "Kaggle",
        "Behavioral Insight": "Analytical",
    }

    r = client.post('/api/predict', json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    # basic expected keys
    assert 'Best-Fit Career Domain' in data

    # small delay to ensure DB commit before listing
    time.sleep(0.5)

    r2 = client.get('/api/predictions')
    assert r2.status_code == 200
    rows = r2.json()
    # test that at least one row for this user exists
    assert any(r.get('user_id') == 'TEST_PY_001' for r in rows)
