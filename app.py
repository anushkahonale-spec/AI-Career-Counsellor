from flask import Flask, render_template, request, send_file, redirect

from gemini_helper import get_career_recommendation

from database import (
    init_db,
    save_report,
    get_all_reports,
    get_report,
    get_dashboard_stats,
    delete_report
)

from pdf_generator import generate_pdf


app = Flask(__name__)


# =====================================================
# INITIALIZE DATABASE
# =====================================================

init_db()


# =====================================================
# STORE LATEST REPORT
# =====================================================

latest_report = {}


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template("home.html")


# =====================================================
# CAREER ASSESSMENT FORM
# =====================================================

@app.route("/form")
def form():

    return render_template("form.html")


# =====================================================
# AI CAREER PREDICTION
# =====================================================

@app.route("/predict", methods=["POST"])
def predict():

    global latest_report

    name = request.form.get(
        "name",
        "Student"
    )

    try:

        cgpa = float(
            request.form.get(
                "cgpa",
                0
            )
        )

    except:

        cgpa = 0.0


    skills = request.form.getlist(
        "skills"
    )

    interest = request.form.get(
        "interest",
        ""
    )


    try:

        result = get_career_recommendation(

            name=name,

            cgpa=cgpa,

            skills=skills,

            interests=interest

        )


        # =================================================
        # SAVE REPORT
        # =================================================

        save_report(

            name=name,

            cgpa=cgpa,

            skills=skills,

            interests=interest,

            result=result

        )


        # =================================================
        # STORE LATEST REPORT FOR PDF
        # =================================================

        latest_report = {

            "name": name,

            "career": result.get(
                "career",
                "Not Available"
            ),

            "score": result.get(
                "match",
                0
            ),

            "salary": result.get(
                "salary",
                "Not Available"
            ),

            "companies": result.get(
                "companies",
                []
            ),

            "skills": result.get(
                "skills_to_learn",
                []
            ),

            "roadmap": result.get(
                "roadmap",
                []
            ),

            "why": result.get(
                "why",
                ""
            )

        }


        return render_template(

            "result.html",

            name=name,

            career=result.get(
                "career",
                "Not Available"
            ),

            score=result.get(
                "match",
                0
            ),

            salary=result.get(
                "salary",
                "Not Available"
            ),

            companies=result.get(
                "companies",
                []
            ),

            skills=result.get(
                "skills_to_learn",
                []
            ),

            roadmap=result.get(
                "roadmap",
                []
            ),

            why=result.get(
                "why",
                ""
            )

        )


    except Exception as e:

        print(
            "Prediction Error:",
            e
        )


        return render_template(

            "result.html",

            name=name,

            career="Error",

            score=0,

            salary="Not Available",

            companies=[
                "No Data"
            ],

            skills=[
                "No Data"
            ],

            roadmap=[
                "Try Again"
            ],

            why=(
                "Gemini AI could not generate "
                "a recommendation. Please try again."
            )

        )


# =====================================================
# DOWNLOAD PDF
# =====================================================

@app.route("/download")
def download():

    if not latest_report:

        return "No report available."


    filename = generate_pdf(
        latest_report
    )


    return send_file(

        filename,

        as_attachment=True

    )


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    reports = get_all_reports()

    stats = get_dashboard_stats()


    return render_template(

        "dashboard.html",

        reports=reports,

        stats=stats

    )


# =====================================================
# VIEW FULL REPORT
# =====================================================

@app.route("/report/<int:report_id>")
def view_report(report_id):

    report = get_report(
        report_id
    )


    if report is None:

        return "Report not found"


    return render_template(

        "view_report.html",

        report=report

    )


# =====================================================
# DELETE REPORT
# =====================================================

@app.route("/delete/<int:report_id>")
def delete(report_id):

    delete_report(
        report_id
    )


    return redirect(
        "/dashboard"
    )


# =====================================================
# RUN APPLICATION
# =====================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )