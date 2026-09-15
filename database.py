import sqlite3


def init_db():

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_reports(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            cgpa REAL,

            skills TEXT,

            interests TEXT,

            career TEXT,

            match INTEGER,

            salary TEXT

        )
    """)

    conn.commit()
    conn.close()


def save_report(name, cgpa, skills, interests, result):

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO career_reports
        (
            name,
            cgpa,
            skills,
            interests,
            career,
            match,
            salary
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        name,
        cgpa,
        ",".join(skills),
        interests,
        result.get("career", "Not Available"),
        result.get("match", 0),
        result.get("salary", "Not Available")

    ))

    conn.commit()
    conn.close()


def get_all_reports():

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            cgpa,
            career,
            match,
            salary

        FROM career_reports

        ORDER BY id DESC
    """)

    reports = cursor.fetchall()

    conn.close()

    return reports


def get_report(report_id):

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM career_reports
        WHERE id = ?
    """, (report_id,))

    report = cursor.fetchone()

    conn.close()

    return report


def delete_report(report_id):

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM career_reports
        WHERE id = ?
    """, (report_id,))

    conn.commit()
    conn.close()


def get_dashboard_stats():

    conn = sqlite3.connect("career.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM career_reports
    """)

    total = cursor.fetchone()[0]


    cursor.execute("""
        SELECT AVG(cgpa)
        FROM career_reports
    """)

    avg_cgpa = cursor.fetchone()[0]

    if avg_cgpa is None:
        avg_cgpa = 0


    cursor.execute("""
        SELECT AVG(match)
        FROM career_reports
    """)

    avg_match = cursor.fetchone()[0]

    if avg_match is None:
        avg_match = 0


    cursor.execute("""
        SELECT career, COUNT(*) as count

        FROM career_reports

        GROUP BY career

        ORDER BY count DESC

        LIMIT 1
    """)

    top_career = cursor.fetchone()

    if top_career:
        career = top_career[0]
    else:
        career = "N/A"


    conn.close()


    return {

        "total": total,

        "cgpa": round(avg_cgpa, 2),

        "match": round(avg_match, 2),

        "career": career

    }