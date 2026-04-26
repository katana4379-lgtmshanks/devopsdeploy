from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import joblib
import os
import io
from datetime import datetime

# ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

model = None

# ---------------- LOAD MODEL ----------------
def load_model():
    global model
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
        return True
    return False

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- CHECK MODEL ----------------
@app.route("/check_model")
def check_model():
    return jsonify({"loaded": load_model()})

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
def predict():
    global model

    if model is None:
        return jsonify({"success": False, "message": "Model not loaded"}), 400

    data = request.get_json()
    subjects = data.get("subjects", [])

    if not subjects:
        return jsonify({"success": False, "message": "No data"}), 400

    names = []
    rows = []
    reasons = []

    access_map = {"Low": 0, "Medium": 1, "High": 2}

    for s in subjects:
        name = s["name"]
        hours = float(s["hours"])
        attendance = float(s["attendance"])
        access = access_map.get(s["access"], 1)
        sleep = float(s["sleep"])
        previous = float(s["previous"])
        tutoring = int(s["tutoring"])

        names.append(name)
        rows.append([hours, attendance, access, sleep, previous, tutoring])

        # Explainability
        r = []
        if sleep < 5:
            r.append("Low sleep")
        if attendance < 50:
            r.append("Low attendance")
        if access == 0:
            r.append("Poor study material")
        if hours < 4:
            r.append("Low study hours")

        reasons.append(", ".join(r) if r else "Good balance")

    # DataFrame
    df = pd.DataFrame(rows, columns=[
        "Hours_Studied",
        "Attendance",
        "Access_to_Resources",
        "Sleep_Hours",
        "Previous_Scores",
        "Tutoring_Sessions"
    ])

    # 🔥 CORRECT PREDICTION (NO SCALER)
    preds = model.predict(df)

    results = []

    for i, name in enumerate(names):
        score = round(float(preds[i]), 1)

        if score < 40:
            status, color, advice = "High Attention", "#ff4d4d", "Study daily"
        elif score < 60:
            status, color, advice = "Moderate", "#ffa500", "Practice more"
        elif score < 70:
            status, color, advice = "Good", "#2ecc71", "Stay consistent"
        else:
            status, color, advice = "Excellent", "#27ae60", "Keep it up"

        results.append({
            "name": name,
            "score": score,
            "status": status,
            "color": color,
            "advice": advice,
            "reason": reasons[i],
            "previous": rows[i][4]
        })

    # ---------------- TIMETABLE ----------------
    slots = ["9-10 AM", "10-11 AM", "11-12 PM", "2-3 PM", "3-4 PM"]

    timetable = []
    for i in range(min(len(results), len(slots))):
        timetable.append({
            "slot": slots[i],
            "subject": results[i]["name"],
            "score": results[i]["score"]
        })

    avg = round(np.mean([r["score"] for r in results]), 1)

    return jsonify({
        "success": True,
        "results": results,
        "timetable": timetable,
        "avg_score": avg,
        "total_subjects": len(results)
    })

# ---------------- PDF DOWNLOAD ----------------
@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    data = request.get_json()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("Smart Study Timetable", styles["Title"])
    elements.append(title)

    date = Paragraph(datetime.now().strftime("%d %B %Y"), styles["Normal"])
    elements.append(date)

    elements.append(Spacer(1, 15))

    status_map = {}
    prev_map = {}

    for r in data.get("results", []):
        status_map[r["name"]] = r["status"]
        prev_map[r["name"]] = r.get("previous", "")

    table_data = [["Time", "Subject", "Previous Score", "Predicted Score", "Status"]]

    for t in data.get("timetable", []):
        subject = t.get("subject", "")

        table_data.append([
            t.get("slot", ""),
            subject,
            str(prev_map.get(subject, "")),
            str(t.get("score", "")),
            status_map.get(subject, "")
        ])

    table = Table(table_data, colWidths=[90, 150, 110, 110, 100])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="timetable.pdf",
        mimetype="application/pdf"
    )

# ---------------- RUN ----------------
if __name__ == "__main__":
    if not load_model():
        print("⚠️ Model not found! Train first.")
    app.run(host="0.0.0.0", port=5000)