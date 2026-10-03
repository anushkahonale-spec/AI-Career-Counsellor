from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/predict", methods=["POST"])
def predict():

    skills = request.form.getlist("skills")
    skills = [s.lower() for s in skills]

    # SAFE CGPA HANDLING (NO CRASH)
    cgpa_input = request.form.get("cgpa")

    try:
        cgpa = float(cgpa_input)
    except (TypeError, ValueError):
        cgpa = 0

    scores = {
        "AI Engineer 🤖": 0,
        "ML Engineer 🧠": 0,
        "Data Scientist 📊": 0,
        "Frontend Developer ⚛️": 0,
        "Backend Developer 🌐": 0
    }

    # Skill scoring logic
    if "ai" in skills:
        scores["AI Engineer 🤖"] += 40

    if "machine learning" in skills:
        scores["ML Engineer 🧠"] += 40

    if "data" in skills:
        scores["Data Scientist 📊"] += 30

    if "python" in skills:
        scores["AI Engineer 🤖"] += 20
        scores["ML Engineer 🧠"] += 20
        scores["Backend Developer 🌐"] += 30

    if "html" in skills or "css" in skills or "javascript" in skills:
        scores["Frontend Developer ⚛️"] += 50

    # CGPA influence
    if cgpa >= 8:
        scores["AI Engineer 🤖"] += 20
        scores["ML Engineer 🧠"] += 20
    elif cgpa >= 6:
        scores["Backend Developer 🌐"] += 10

    # Convert to percentage output
    max_score = max(scores.values()) if max(scores.values()) > 0 else 1

    result = []
    for career, score in scores.items():
        if score > 0:
            percent = int((score / max_score) * 100)
            result.append((career, percent))

    result.sort(key=lambda x: x[1], reverse=True)

    if not result:
        result = [("Explore Software Development 👨‍💻", 100)]

    return render_template("result.html", careers=result)


if __name__ == "__main__":
    app.run(debug=True)