import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score

# Use dataset in the backend folder
here = os.path.dirname(__file__)
DATA_PATH = os.path.join(here, "LatestCareerdataset.csv")

if not os.path.exists(DATA_PATH):
    raise SystemExit(f"Dataset not found at {DATA_PATH}")

print("Loading dataset from:", DATA_PATH)
df = pd.read_csv(DATA_PATH)

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

y = df["Best-Fit Career Domain"].fillna("Unknown").astype(str)

le = LabelEncoder()
y_enc = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    df["combined_text"], y_enc, test_size=0.2, random_state=42, stratify=y_enc
)

tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1,2))
Xtr = tfidf.fit_transform(X_train)
Xte = tfidf.transform(X_test)

clf = LogisticRegression(max_iter=1000, class_weight="balanced", solver="liblinear", random_state=42)
clf.fit(Xtr, y_train)

y_pred = clf.predict(Xte)
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")

print(f"Model evaluation completed:\n  Accuracy: {acc:.4f}\n  Weighted F1: {f1:.4f}")

# Optionally save small report
report = {
    "accuracy": float(acc),
    "f1_weighted": float(f1),
}
print(report)
