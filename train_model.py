import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
import joblib

np.random.seed(42)

print("🔄 Generating dataset...")

rows = 6600

# Generate features
hours = np.random.randint(0, 13, rows)
attendance = np.random.randint(0, 101, rows)
access = np.random.choice([0, 1, 2], rows)
sleep = np.random.randint(3, 10, rows)
previous = np.random.randint(0, 101, rows)
tutoring = np.random.randint(0, 6, rows)

# Create realistic score formula
score = (
    hours * 2 +
    attendance * 0.3 +
    access * 5 +
    sleep * 1.5 +
    previous * 0.4 +
    tutoring * 2
)

# Add randomness
score += np.random.normal(0, 5, rows)

# Clamp between 0–100
score = np.clip(score, 0, 100)

# DataFrame
df = pd.DataFrame({
    "Hours_Studied": hours,
    "Attendance": attendance,
    "Access_to_Resources": access,
    "Sleep_Hours": sleep,
    "Previous_Scores": previous,
    "Tutoring_Sessions": tutoring,
    "Exam_Score": score.round(1)
})

# Train model
X = df.drop("Exam_Score", axis=1)
y = df["Exam_Score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("🚀 Training model...")

model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("\n📊 Evaluation")
print("R2:", round(r2_score(y_test, y_pred), 3))
print("MAE:", round(mean_absolute_error(y_test, y_pred), 2))

print("\n📈 Distribution")
print(df["Exam_Score"].describe())

# Save model
joblib.dump(model, "model.pkl")

print("\n✅ model.pkl ready!")