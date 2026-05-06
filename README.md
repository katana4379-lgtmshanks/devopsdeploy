# 🎓 Smart Study Planner — ML-Powered Student Performance Predictor

> A machine learning web application that predicts student exam scores, generates personalised study timetables, and exports downloadable PDF reports — deployed live via a CI/CD pipeline on **Render**.

---

## 🚀 Live Demo

[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-RandomForest-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)

---

## 📌 Project Overview

This project demonstrates an **end-to-end MLOps workflow**:

1. **Train** a Random Forest regression model on student study data
2. **Serve** predictions via a Flask REST API
3. **Deploy** automatically to a cloud web server using a **GitHub → Render CI/CD pipeline**

Every push to the `main` branch triggers an automatic redeploy — no manual intervention required.

---

## ✨ Features

- 🤖 **ML Prediction Engine** — Random Forest Regressor trained on 6,600 synthetic student records
- 📊 **Multi-Subject Input** — Enter data for multiple subjects in one go
- 🗓️ **Auto-Generated Timetable** — Study slots ranked by predicted performance
- 🔍 **Explainability** — Highlights risk factors (low sleep, poor attendance, etc.)
- 📄 **PDF Export** — Downloadable study timetable with scores and status via ReportLab
- ⚡ **Real-Time Predictions** — REST API responds with scores, status labels, advice, and colour coding

---

## 🧠 ML Model Details

| Property | Value |
|---|---|
| Algorithm | Random Forest Regressor |
| Training Samples | 6,600 (synthetic) |
| Estimators | 300 (full) / 30 (compressed) |
| Target Variable | Exam Score (0–100) |
| Serialization | `joblib` (`.pkl`) |

### Input Features

| Feature | Type | Description |
|---|---|---|
| `Hours_Studied` | int | Daily study hours (0–12) |
| `Attendance` | int | Class attendance percentage (0–100) |
| `Access_to_Resources` | categorical | Low / Medium / High |
| `Sleep_Hours` | int | Average sleep per night (3–9) |
| `Previous_Scores` | int | Prior exam score (0–100) |
| `Tutoring_Sessions` | int | Weekly tutoring sessions (0–5) |

### Prediction Output

| Score Range | Status | Colour |
|---|---|---|
| < 40 | High Attention ⚠️ | Red |
| 40 – 59 | Moderate 🔶 | Orange |
| 60 – 69 | Good ✅ | Green |
| ≥ 70 | Excellent 🌟 | Dark Green |

---

## 🗂️ Project Structure

```
devopsdeploy/
│
├── app.py               # Flask application & API routes
├── train_model.py       # Model training script
├── model.pkl            # Serialised trained model
├── scaler.pkl           # (Legacy) Feature scaler
├── requirements.txt     # Python dependencies
├── runtime.txt          # Python version for Render (python-3.11.x)
├── install_py312.bat    # Windows local setup helper
│
├── templates/           # Jinja2 HTML templates
│   └── index.html
│
├── static/              # CSS, JS, and frontend assets
│
└── .gitignore
```

---

## ⚙️ Local Setup

### Prerequisites

- Python 3.11+
- `pip`

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/katana4379-lgtmshanks/devopsdeploy.git
cd devopsdeploy

# 2. Create and activate a virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Retrain the model from scratch
python train_model.py

# 5. Run the Flask app
python app.py
```

The app will be available at `http://localhost:5000`.

---

## 🌐 API Reference

### `POST /predict`

Predicts exam scores for one or more subjects.

**Request body:**
```json
{
  "subjects": [
    {
      "name": "Mathematics",
      "hours": 6,
      "attendance": 80,
      "access": "High",
      "sleep": 7,
      "previous": 72,
      "tutoring": 2
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "results": [...],
  "timetable": [...],
  "avg_score": 74.3,
  "total_subjects": 1
}
```

### `POST /download_pdf`

Generates and returns a PDF study timetable from the prediction results.

### `GET /check_model`

Returns `{ "loaded": true/false }` — useful for health checks.

---

## 🔄 CI/CD Pipeline

This project uses a **GitHub → Render** continuous deployment pipeline.

```
Developer pushes to main
        │
        ▼
  GitHub Repository
        │
        │  Webhook trigger
        ▼
  Render Build Process
   ├── Install dependencies (requirements.txt)
   ├── Set Python runtime (runtime.txt → python-3.11.x)
   └── Start server (gunicorn app:app)
        │
        ▼
  Live Web Application
```

Every commit to `main` automatically triggers a fresh build and redeploy on Render — **no manual steps needed**.

### Render Configuration

| Setting | Value |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Python Version | 3.11 (via `runtime.txt`) |
| Service Type | Web Service (Free tier) |

---

## 📦 Dependencies

Key packages used:

```
flask
scikit-learn
pandas
numpy
joblib
reportlab
gunicorn
```

---

## 📝 Notes

- The `model.pkl` included in the repo is a **compressed version** (30 estimators, 2,000 rows) to stay within GitHub's file size limits. The full model (300 estimators, 6,600 rows) can be regenerated locally via `train_model.py`.
- The `venv/` folder is committed in this repo but is typically added to `.gitignore` in production projects.
- `scaler.pkl` is retained for compatibility but is not used in the current prediction pipeline.

---

## 👤 Author

**katana4379-lgtmshanks** · [GitHub Profile](https://github.com/katana4379-lgtmshanks)

---

*Built as a demonstration of MLOps principles — training, serving, and deploying a machine learning model with an automated CI/CD pipeline.*
