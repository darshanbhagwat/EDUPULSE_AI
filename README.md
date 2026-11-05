
# 🎓 EduPulse AI

### AI-Powered Student Performance & Learning Analytics

EduPulse AI is a Python-based Data Science application that analyses student academic information and generates estimated performance predictions using Machine Learning.

## 🚀 Features

- Student performance prediction
- Random Forest Regression model
- CSV dataset upload
- Batch student predictions
- Interactive analytics dashboard
- Personalized learning recommendations
- Downloadable prediction reports
- Feature importance visualization

## 🧠 Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Plotly
- Matplotlib
- Joblib

## 🤖 Machine Learning

Algorithm: Random Forest Regressor

Dataset: 1,000 simulated student records.

Model evaluation:
- Mean Absolute Error: 4.63
- R² Score: 0.818

These metrics are based on a simulated dataset and do not establish real-world predictive performance.

## 📂 Project Structure

```text
EDUPULSE_AI/
├── app.py
├── train_model.py
├── requirements.txt
├── data/
├── models/
├── screenshots/
├── README.md
└── .gitignore
```

## ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Open the project:

```bash
cd EduPulse-AI
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python train_model.py
```

Run the application:

```bash
streamlit run app.py
```

## 📊 Dataset

This project uses simulated student data for demonstration and experimentation.

The model should not be used for real academic decisions without validation on representative real-world data.

## 🎯 Project Objective

To demonstrate how Data Science and Machine Learning can be used to explore educational data and support student learning insights.

## 👨‍💻 Author

Darshan Yogesh Bhagwat

First-Year B.Sc. Data Science Student

Savitribai Phule Pune University
Department of Technology

## 📌 Project Status

Hackathon Project Prototype
