import requests
import time
from sqlmodel import select
from app.database.session import engine
from app.database.models import Prediction

url = 'http://127.0.0.1:8000/api/predict'
payload = {
    "User ID": "TEST_PERSIST_001",
    "Full Name": "Persist Test",
    "Education Level": "BS Computer Science",
    "Academic Performance": "3.7",
    "skills": "Python; Machine Learning; SQL",
    "Certifications": "None",
    "Do you prefer working with data, people, or ideas?": "data",
    "How do you approach solving complex problems?": "Analytical and logical",
    "Do you thrive better in a structured or flexible environment?": "Flexible",
    "Do you prefer working independently or in a team?": "Independently",
    "Do you learn best through practice, observation, or theory?": "Practice",
    "Interests": "AI; Data Science",
    "Extra-Curricular Activities": "Kaggle",
    "Behavioral Insight": "Analytical"
}

print('Posting payload...')
r = requests.post(url, json=payload)
print('Status code:', r.status_code)
print('Response JSON:', r.json())

# give a short delay to ensure DB commit
time.sleep(1)

print('\nQuerying DB for the inserted row...')
from sqlmodel import Session

with Session(engine) as session:
    statement = select(Prediction).where(Prediction.user_id == 'TEST_PERSIST_001')
    results = session.exec(statement).all()
    print('Found rows:', len(results))
    for row in results:
        print(row)
