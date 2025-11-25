import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score

# === PATH SETTINGS ===
DATA_PATH = "../../LatestCareerdataset.csv"  # adjust if dataset is elsewhere
ARTIFACT_DIR = "app/model_artifacts"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

# === LOAD DATA ===
df = pd.read_csv(DATA_PATH)

# === COMBINE TEXT COLUMNS ===
input_columns = [
    "Education Level",
    "Academic Performance",
    "Skills",
    "Certifications",
    "Do you prefer working with data, people, or ideas?",
    "How do you approach solving complex problems?",
    "Do you thrive better in a structured or flexible environment?",
    "Do you prefer working independently or in a team?",
    "Do you learn best through practice, observation, or theory?",
    "Interests",
    "Extra-Curricular Activities"
]

df["combined_text"] = df[input_columns].fillna("").agg(" ".join, axis=1)

# === TARGET COLUMN ===
y = df["Best-Fit Career Domain"].fillna("Unknown").astype(str)

# === ENCODE LABELS ===
le = LabelEncoder()
y_enc = le.fit_transform(y)

# === TRAIN TEST SPLIT ===
X_train, X_test, y_train, y_test = train_test_split(
    df["combined_text"], y_enc, test_size=0.2, random_state=42, stratify=y_enc
)

# === TF-IDF VECTORIZE ===
tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1, 2))
Xtr = tfidf.fit_transform(X_train)
Xte = tfidf.transform(X_test)

# === TRAIN CLASSIFIER ===
clf = LogisticRegression(max_iter=1000, class_weight="balanced", solver="liblinear", random_state=42)
clf.fit(Xtr, y_train)

# === EVALUATE ===
y_pred = clf.predict(Xte)
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print(f"✅ Model trained successfully!")
print(f"Accuracy: {acc:.3f} | F1-score: {f1:.3f}")

# === SAVE ARTIFACTS ===
joblib.dump(tfidf, os.path.join(ARTIFACT_DIR, "vectorizer.joblib"))
joblib.dump(clf, os.path.join(ARTIFACT_DIR, "career_classifier.joblib"))
joblib.dump(le, os.path.join(ARTIFACT_DIR, "label_encoder.joblib"))

print(f"✅ Artifacts saved in: {ARTIFACT_DIR}")
print(os.listdir(ARTIFACT_DIR))
