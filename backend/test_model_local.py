import joblib
from pathlib import Path

ART = Path('model_artifacts')
print('Artifacts dir exists:', ART.exists())

try:
    vec = joblib.load(ART / 'vectorizer.joblib')
    print('vectorizer OK')
except Exception as e:
    print('vectorizer load error:', e)

try:
    le = joblib.load(ART / 'label_encoder.joblib')
    print('label encoder OK')
except Exception as e:
    print('label encoder load error:', e)

try:
    clf = joblib.load(ART / 'career_clf.joblib')
    print('classifier OK')
except Exception as e:
    print('classifier load error:', e)

try:
    reg = joblib.load(ART / 'conf_reg.joblib')
    print('regressor OK')
except Exception as e:
    print('regressor load error or absent:', e)

# sample
cols_input = [
    'Education Level', 'Academic Performance', 'Skills', 'Certifications',
    'Do you prefer working with data, people, or ideas?', 'How do you approach solving complex problems?',
    'Do you thrive better in a structured or flexible environment?', 'Do you prefer working independently or in a team?',
    'Do you learn best through practice, observation, or theory?', 'Interests', 'Extra-Curricular Activities'
]

sample = {
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
    'Extra-Curricular Activities': 'Coding club'
}

text = ' '.join(sample.get(c, '') for c in cols_input)
try:
    X = vec.transform([text])
    pred = clf.predict(X)[0]
    try:
        label = le.inverse_transform([pred])[0]
    except Exception:
        label = str(pred)
    print('Predicted:', label)
    if 'reg' in globals() and reg is not None:
        print('Conf:', float(reg.predict(X)[0]))
except Exception as e:
    print('Prediction failed:', e)
