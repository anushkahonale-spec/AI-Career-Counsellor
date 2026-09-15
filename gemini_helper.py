import os
import json
import re

from dotenv import load_dotenv
from google import genai


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =====================================================
# CLEAN TEXT
# =====================================================

def clean_text(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return text.strip()


# =====================================================
# CLEAN ROADMAP
# =====================================================

def clean_roadmap(roadmap):

    cleaned = []

    if not isinstance(roadmap, list):
        return cleaned

    for step in roadmap:

        step = str(step).strip()

        step = re.sub(
            r"^\d+\s+Step\s*\d*\s*:?\s*",
            "",
            step,
            flags=re.IGNORECASE
        )

        step = re.sub(
            r"^Step\s*\d*\s*:?\s*",
            "",
            step,
            flags=re.IGNORECASE
        )

        if step:
            cleaned.append(step)

    return [
        f"Step {i}: {step}"
        for i, step in enumerate(cleaned[:5], start=1)
    ]


# =====================================================
# CALCULATE MATCH SCORE
# =====================================================

def calculate_match(cgpa, skills, interest):

    score = 0

    # -------------------------------------------------
    # NORMALIZE SKILLS
    # -------------------------------------------------

    skills_lower = [
        str(skill).lower().strip()
        for skill in skills
    ]

    interest_lower = str(
        interest
    ).lower().strip()


    # -------------------------------------------------
    # CGPA - 20 POINTS
    # -------------------------------------------------

    if cgpa >= 9:

        score += 20

    elif cgpa >= 8.5:

        score += 18

    elif cgpa >= 8:

        score += 16

    elif cgpa >= 7:

        score += 13

    elif cgpa >= 6:

        score += 10

    else:

        score += 5


    # -------------------------------------------------
    # CAREER REQUIREMENTS
    #
    # These values MUST match form.html
    # -------------------------------------------------

    career_requirements = {

        "ai": [
            "python",
            "machine learning",
            "ai"
        ],

        "web": [
            "html",
            "css",
            "javascript"
        ],

        "data": [
            "python",
            "machine learning",
            "data"
        ],

        "backend": [
            "python",
            "java",
            "sql"
        ]

    }


    # -------------------------------------------------
    # FIND SELECTED CAREER
    # -------------------------------------------------

    selected_career = None

    for career in career_requirements:

        if career in interest_lower:

            selected_career = career

            break


    # -------------------------------------------------
    # INTEREST + SKILL MATCH
    # 40 POINTS
    # -------------------------------------------------

    if selected_career:

        required_skills = career_requirements[
            selected_career
        ]

        matched_skills = sum(
            1
            for skill in required_skills
            if skill in skills_lower
        )

        skill_ratio = (
            matched_skills /
            len(required_skills)
        )

        score += round(
            skill_ratio * 40
        )

    else:

        score += 20


    # -------------------------------------------------
    # TECHNICAL SKILLS
    # 30 POINTS
    # -------------------------------------------------

    important_skills = [

        "python",

        "java",

        "machine learning",

        "ai",

        "html",

        "css",

        "javascript",

        "data",

        "sql"

    ]


    matched_technical = sum(
        1
        for skill in important_skills
        if skill in skills_lower
    )


    score += min(
        30,
        matched_technical * 4
    )


    # -------------------------------------------------
    # CAREER INTEREST BONUS
    # 10 POINTS
    # -------------------------------------------------

    if selected_career:

        score += 10


    # -------------------------------------------------
    # FINAL SCORE
    # -------------------------------------------------

    return max(
        0,
        min(
            100,
            score
        )
    )


# =====================================================
# GET CAREER RECOMMENDATION
# =====================================================

def get_career_recommendation(
    name,
    cgpa,
    skills,
    interests
):

    # -------------------------------------------------
    # CALCULATE SCORE IN PYTHON
    # -------------------------------------------------

    match_score = calculate_match(
        cgpa,
        skills,
        interests
    )


    print(
        "\n===== PYTHON MATCH SCORE ====="
    )

    print(
        match_score
    )


    # -------------------------------------------------
    # GEMINI PROMPT
    # -------------------------------------------------

    prompt = f"""
You are an AI Career Counsellor for Indian engineering students.

Student profile:

Name: {name}
CGPA: {cgpa}
Skills: {", ".join(skills)}
Career Interest: {interests}

Recommend ONE suitable technology career.

The recommendation must be based ONLY on the student's
provided skills and career interest.

Do not invent skills that the student does not have.

The application has already calculated the match score:

{match_score}%

You MUST use exactly {match_score} as the match score.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "career": "",
    "match": {match_score},
    "salary": "",
    "companies": [],
    "skills_to_learn": [],
    "roadmap": [],
    "why": ""
}}

Rules:

1. Match must remain exactly {match_score}.
2. Salary must use Indian Rupees and LPA.
3. Give 4 to 6 realistic companies.
4. Give 4 to 6 useful skills to learn.
5. Give exactly 5 roadmap steps.
6. Do not write Step 1, Step 2, etc.
7. Do not use markdown.
8. Do not use code fences.
9. Return ONLY JSON.
"""


    try:

        # -------------------------------------------------
        # GEMINI API
        # -------------------------------------------------

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )


        print(
            "\n===== GEMINI RAW RESPONSE ====="
        )

        print(
            response.text
        )


        # -------------------------------------------------
        # CLEAN RESPONSE
        # -------------------------------------------------

        text = clean_text(
            response.text
        )


        # -------------------------------------------------
        # PARSE JSON
        # -------------------------------------------------

        result = json.loads(
            text
        )


        # -------------------------------------------------
        # FORCE PYTHON SCORE
        # -------------------------------------------------

        result["match"] = match_score


        # -------------------------------------------------
        # CLEAN CAREER
        # -------------------------------------------------

        result["career"] = str(
            result.get(
                "career",
                "Not Available"
            )
        ).strip()


        # -------------------------------------------------
        # CLEAN SALARY
        # -------------------------------------------------

        result["salary"] = str(
            result.get(
                "salary",
                "Not Available"
            )
        ).strip()


        # -------------------------------------------------
        # CLEAN COMPANIES
        # -------------------------------------------------

        if not isinstance(
            result.get("companies"),
            list
        ):

            result["companies"] = []


        result["companies"] = [

            str(company).strip()

            for company in result["companies"]

            if str(company).strip()

        ]


        # -------------------------------------------------
        # CLEAN SKILLS
        # -------------------------------------------------

        if not isinstance(
            result.get("skills_to_learn"),
            list
        ):

            result["skills_to_learn"] = []


        result["skills_to_learn"] = [

            str(skill).strip()

            for skill in result["skills_to_learn"]

            if str(skill).strip()

        ]


        # -------------------------------------------------
        # CLEAN ROADMAP
        # -------------------------------------------------

        result["roadmap"] = clean_roadmap(
            result.get(
                "roadmap",
                []
            )
        )


        # -------------------------------------------------
        # CLEAN WHY
        # -------------------------------------------------

        result["why"] = str(
            result.get(
                "why",
                "The recommendation is based on the student's skills, CGPA and career interest."
            )
        ).strip()


        return result


    except Exception as e:

        print(
            "\nGemini Error:",
            e
        )


        # -------------------------------------------------
        # FALLBACK
        # -------------------------------------------------

        return {

            "career": "Technology Professional",

            "match": match_score,

            "salary": "₹5 - ₹10 LPA (Fresher)",

            "companies": [
                "TCS",
                "Infosys",
                "Accenture",
                "Wipro"
            ],

            "skills_to_learn": [
                "Advanced Programming",
                "DSA",
                "SQL",
                "Git & GitHub",
                "Cloud Computing"
            ],

            "roadmap": [
                "Step 1: Strengthen programming fundamentals",
                "Step 2: Practice data structures and algorithms",
                "Step 3: Build practical projects",
                "Step 4: Improve SQL and database skills",
                "Step 5: Prepare for technical interviews"
            ],

            "why": (
                "The recommendation is based on the student's "
                "CGPA, selected skills and career interest."
            )

        }