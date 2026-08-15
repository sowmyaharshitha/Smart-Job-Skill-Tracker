from flask import Flask, render_template, request
from pypdf import PdfReader
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

job_roles = {

    "ServiceNow Developer": [
        "Python",
        "JavaScript",
        "HTML",
        "CSS",
        "ServiceNow Admin",
        "CSA Certification"
    ],

    "Python Developer": [
        "Python",
        "SQL",
        "Git",
        "OOP",
        "Flask"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "SQL"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Statistics"
    ],

    "Cybersecurity Analyst": [
        "Networking",
        "Linux",
        "Python",
        "Cybersecurity",
        "SQL"
    ],

    "Java Developer": [
        "Java",
        "SQL",
        "OOP",
        "Git",
        "Spring Boot"
    ],

    "Cloud Engineer": [
        "AWS",
        "Linux",
        "Networking",
        "Python",
        "Docker"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Machine Learning",
        "Pandas"
    ]
}

def detect_skills(resume_text):
    all_skills = set()

    for skills in job_roles.values():
        all_skills.update(skills)

    detected = []

    resume_text = resume_text.lower()

    for skill in all_skills:
        if skill.lower() in resume_text:
            detected.append(skill)

    return detected 

@app.route('/')
def home():
    return render_template(
        'index.html',
        roles=job_roles.keys(),
        job_roles=job_roles
    )

@app.route('/result', methods=['POST'])
def result():

    name = request.form['name']
    role = request.form['role']

    # Get uploaded resume
    resume = request.files.get('resume')

    resume_text = ""

    if resume and resume.filename:
        reader = PdfReader(resume)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text

    # Get required skills for selected role
    required = job_roles[role]

    # Detect skills from resume
    detected = detect_skills(resume_text)

    # Keep only skills required for the selected role
    completed = [
        skill for skill in required
        if skill in detected
    ]

    # Calculate progress
    progress = int(
        len(completed) /
        len(required) * 100
    )

    # Find missing skills
    missing = []

    for skill in required:
        if skill not in completed:
            missing.append(skill)

    return render_template(
        'result.html',
        name=name,
        role=role,
        progress=progress,
        completed=completed,
        missing=missing
    )

if __name__ == '__main__':
    app.run(debug=True)