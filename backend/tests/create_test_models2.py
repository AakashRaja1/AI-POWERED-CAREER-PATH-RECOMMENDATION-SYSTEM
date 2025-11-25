import numpy as np
from sklearn.dummy import DummyClassifier, DummyRegressor
import joblib

# Create and save a dummy classifier that always predicts "Data Scientist"
clf = DummyClassifier(strategy='constant', constant='Data Scientist')
X = np.zeros((1, 100))  # Dummy feature matrix
y = ['Data Scientist']
clf.fit(X, y)
joblib.dump(clf, 'model_artifacts/career_classifier.joblib')

# Create and save a dummy regressor that always predicts 0.75
reg = DummyRegressor(strategy='constant', constant=0.75)
reg.fit(X, [0.75])
joblib.dump(reg, 'model_artifacts/confidence_regressor.joblib')