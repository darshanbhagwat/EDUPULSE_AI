
# ==========================================
# EDUPULSE AI - STUDENT PERFORMANCE ANALYSIS
# ==========================================

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# STEP 1: CREATE DATASET

np.random.seed(42)

number_of_students = 1000

data = {
    "study_hours": np.random.uniform(1, 10, number_of_students),
    "attendance": np.random.uniform(40, 100, number_of_students),
    "previous_score": np.random.uniform(30, 100, number_of_students),
    "assignments_completed": np.random.randint(0, 11, number_of_students),
    "sleep_hours": np.random.uniform(4, 10, number_of_students)
}

df = pd.DataFrame(data)

score = (
    df["study_hours"] * 3
    + df["attendance"] * 0.2
    + df["previous_score"] * 0.35
    + df["assignments_completed"] * 1.5
    + df["sleep_hours"] * 1.5
    + np.random.normal(0, 5, number_of_students)
)

df["final_score"] = np.clip(score, 0, 100).round(2)

# STEP 2: SAVE DATASET

df.to_csv("data/student_data.csv", index=False)

print("Dataset created successfully!")
print("Dataset shape:", df.shape)

# STEP 3: PREPARE DATA

X = df[
    [
        "study_hours",
        "attendance",
        "previous_score",
        "assignments_completed",
        "sleep_hours"
    ]
]

y = df["final_score"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# STEP 4: TRAIN MODEL

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# STEP 5: PREDICT

predictions = model.predict(X_test)

# STEP 6: EVALUATE

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nMODEL TRAINING COMPLETED!")
print("Mean Absolute Error:", round(mae, 2))
print("R2 Score:", round(r2, 3))

# STEP 7: SAVE MODEL

joblib.dump(model, "models/student_model.pkl")

print("\nModel saved successfully!")

# STEP 8: FEATURE IMPORTANCE

importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFEATURE IMPORTANCE:")
print(importance.to_string(index=False))

print("\nEDUPULSE AI MODEL READY!")
