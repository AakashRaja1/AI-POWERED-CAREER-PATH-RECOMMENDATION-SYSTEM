import urllib.request, json
url='http://127.0.0.1:8000/api/predict'
payload={
  "User ID": "TEST_SAVE_001",
  "Full Name": "Integration Tester",
  "Education Level": "BS Computer Science",
  "Academic Performance": "3.7",
  "skills": "Python;SQL;Data Analysis",
  "Certifications": "",
  "Do you prefer working with data, people, or ideas?": "data",
  "How do you approach solving complex problems?": "Analytical",
  "Do you thrive better in a structured or flexible environment?": "Flexible",
  "Do you prefer working independently or in a team?": "Independently",
  "Do you learn best through practice, observation, or theory?": "Practice",
  "Interests": "Data Science;AI",
  "Extra-Curricular Activities": "Kaggle",
}
req=urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req, timeout=20) as r:
    print('STATUS', r.status)
    print(r.read().decode())
