
import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# ==========================================
# EDUPULSE AI
# ==========================================

st.set_page_config(
    page_title="EduPulse AI",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# LOAD MODEL AND DATA
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("models/student_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("data/student_data.csv")

model = load_model()
df = load_data()

FEATURES = [
    "study_hours",
    "attendance",
    "previous_score",
    "assignments_completed",
    "sleep_hours"
]

# ==========================================
# HEADER
# ==========================================

st.title("🎓 EduPulse AI")
st.subheader("Student Performance & Learning Analytics")

st.info(
    "EduPulse AI is an educational Data Science prototype. "
    "It currently uses simulated training data. "
    "Predictions are estimates, not guaranteed results."
)

# ==========================================
# SIDEBAR INPUTS
# ==========================================

st.sidebar.title("👨‍🎓 Student Information")
st.sidebar.write("Enter academic information:")

study_hours = st.sidebar.slider(
    "Daily study hours", 1.0, 10.0, 5.0, 0.5
)

attendance = st.sidebar.slider(
    "Attendance (%)", 40, 100, 75
)

previous_score = st.sidebar.slider(
    "Previous exam score", 30, 100, 65
)

assignments = st.sidebar.slider(
    "Assignments completed", 0, 10, 7
)

sleep_hours = st.sidebar.slider(
    "Sleep hours", 4.0, 10.0, 7.0, 0.5
)

# ==========================================
# INDIVIDUAL PREDICTION
# ==========================================

st.header("📊 Student Performance Dashboard")

student_data = pd.DataFrame([{
    "study_hours": study_hours,
    "attendance": attendance,
    "previous_score": previous_score,
    "assignments_completed": assignments,
    "sleep_hours": sleep_hours
}])

prediction = float(model.predict(student_data)[0])
prediction = max(0, min(100, prediction))

col1, col2, col3 = st.columns(3)

col1.metric("Estimated Final Score", f"{prediction:.1f}/100")
col2.metric("Attendance", f"{attendance}%")
col3.metric("Study Hours", f"{study_hours} hrs/day")

st.caption(
    "This estimate is based on a model trained using simulated data."
)

# ==========================================
# PERSONALIZED RECOMMENDATIONS
# ==========================================

st.divider()
st.header("💡 Learning Recommendations")

recommendations = []

if study_hours < 3:
    recommendations.append(
        "Consider building a consistent daily study routine."
    )

if attendance < 75:
    recommendations.append(
        "Try attending classes regularly and reviewing missed topics."
    )

if previous_score < 50:
    recommendations.append(
        "Revise foundational concepts and practise sample questions."
    )

if assignments < 5:
    recommendations.append(
        "Complete pending assignments and review your mistakes."
    )

if sleep_hours < 6:
    recommendations.append(
        "Consider maintaining a regular and sufficient sleep schedule."
    )

if not recommendations:
    recommendations.append(
        "Keep reviewing your progress and maintaining consistent learning habits."
    )

for item in recommendations:
    st.write("✅", item)

# ==========================================
# CSV UPLOAD
# ==========================================

st.divider()
st.header("📁 Upload Student Dataset")

st.write(
    "Upload a CSV file containing student academic information "
    "to generate predictions for multiple students."
)

st.caption(
    "Required columns: study_hours, attendance, previous_score, "
    "assignments_completed, sleep_hours"
)

uploaded_file = st.file_uploader(
    "Choose student CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    try:
        uploaded_df = pd.read_csv(uploaded_file)

        missing_columns = [
            column for column in FEATURES
            if column not in uploaded_df.columns
        ]

        if missing_columns:
            st.error(
                "Missing required columns: "
                + ", ".join(missing_columns)
            )

        elif uploaded_df.empty:
            st.error("Your uploaded CSV file is empty.")

        else:
            # Convert feature columns to numeric
            batch_df = uploaded_df[FEATURES].copy()

            for column in FEATURES:
                batch_df[column] = pd.to_numeric(
                    batch_df[column], errors="coerce"
                )

            # Validate data
            if batch_df.isnull().any().any():
                st.error(
                    "Some required columns contain missing or "
                    "non-numeric values. Please correct your CSV."
                )

            elif not batch_df.apply(
                lambda column: column.between(
                    1, 10
                ).all() if column.name in
                ["study_hours", "sleep_hours"]
                else column.between(
                    0, 10
                ).all() if column.name ==
                "assignments_completed"
                else column.between(
                    0, 100
                ).all()
            ).all():
                st.error(
                    "Some values are outside the allowed ranges. "
                    "Check the data requirements."
                )

            else:
                # Generate predictions
                batch_predictions = model.predict(batch_df)

                result_df = uploaded_df.copy()

                result_df["predicted_final_score"] = [
                    round(float(value), 2)
                    for value in batch_predictions
                ]

                st.success(
                    f"Successfully analysed {len(result_df)} student records!"
                )

                st.subheader("📋 Prediction Results")

                st.dataframe(
                    result_df,
                    use_container_width=True
                )

                # Download report
                csv_data = result_df.to_csv(
                    index=False
                ).encode("utf-8")

                st.download_button(
                    label="⬇️ Download Prediction Report",
                    data=csv_data,
                    file_name="edupulse_prediction_report.csv",
                    mime="text/csv"
                )

                # Batch analytics
                st.subheader("📈 Batch Prediction Analytics")

                average_score = result_df[
                    "predicted_final_score"
                ].mean()

                col1, col2 = st.columns(2)

                col1.metric(
                    "Students Analysed",
                    len(result_df)
                )

                col2.metric(
                    "Average Predicted Score",
                    f"{average_score:.2f}"
                )

                fig = px.histogram(
                    result_df,
                    x="predicted_final_score",
                    nbins=20,
                    title="Distribution of Predicted Scores"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

    except Exception as error:
        st.error(f"Unable to process CSV: {error}")

# ==========================================
# DATASET ANALYTICS
# ==========================================

st.divider()
st.header("📈 Academic Analytics")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.histogram(
        df,
        x="final_score",
        nbins=20,
        title="Distribution of Simulated Exam Scores"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:
    fig2 = px.scatter(
        df,
        x="study_hours",
        y="final_score",
        title="Study Hours vs Simulated Exam Scores"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================
# FEATURE IMPORTANCE
# ==========================================

st.divider()
st.header("🔍 Machine Learning Insights")

importance = pd.DataFrame({
    "Feature": FEATURES,
    "Importance": model.feature_importances_
})

importance["Feature"] = importance["Feature"].str.replace(
    "_", " "
).str.title()

fig3 = px.bar(
    importance.sort_values(
        "Importance", ascending=True
    ),
    x="Importance",
    y="Feature",
    orientation="h",
    title="Model Feature Importance"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# SAMPLE DATASET
# ==========================================

with st.expander("View Sample Student Dataset"):

    st.dataframe(
        df.head(20),
       width="stretch"
    )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "EduPulse AI | Student Performance & Learning Analytics | "
    "Built using Python, Pandas, Scikit-learn and Streamlit. "
    "Predictions are based on simulated training data."
)
