from flask import Flask, request, jsonify
import pandas as pd
import pickle
import os
import re
from datetime import datetime
import PyPDF2
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST"]}})

# ---- Job Recommendations ---- #

try:
    df = pd.read_pickle('df.pkl')
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    print(f"Error loading files: {e}")
    df = None
    similarity = None

def recommendation(title):
    if df is None or similarity is None:
        print("DataFrame or similarity matrix not loaded.")
        return []

    title = title.strip().lower()
    df.reset_index(drop=True, inplace=True)
    df.columns = df.columns.str.strip()

    if 'Title' not in df.columns:
        print("Error: 'Title' column missing.")
        return []

    try:
        idx = df[df['Title'].str.lower() == title].index[0]
        distances = similarity[idx]
        similar_jobs = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:21]
        jobs = [
            {
                'Title': df.iloc[i].Title,
                'Position': df.iloc[i].Position,
                'Company': df.iloc[i].Company,
                'Status': df.iloc[i].Status,
                'JobDescription': df.iloc[i]['Job.Description']
            }
            for i, _ in similar_jobs if i < len(df) and 'Job.Description' in df.columns
        ]
        return jobs if jobs else "No similar jobs found."

    except IndexError:
        print("Job title not found in DataFrame.")
        return []

@app.route('/recommend', methods=['POST'])
def recommend_jobs():
    data = request.json
    job_title = data.get('title')
    if not job_title:
        return jsonify({'status': 'failure', 'message': 'Job title is required'}), 400

    recommendations = recommendation(job_title)
    return jsonify({'status': 'success', 'recommendations': recommendations}) if recommendations else \
        jsonify({'status': 'failure', 'message': 'Job title not found or no recommendations available'}), 404

# ---- ATS Checker ---- #

def insert_data(name, email, resume_score, timestamp, no_of_pages, reco_field, cand_level, skills, recommended_skills, recommended_courses):
    print("Data inserted into the database:")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Resume Score: {resume_score}")
    print(f"Timestamp: {timestamp}")
    print(f"No. of Pages: {no_of_pages}")
    print(f"Recommended Field: {reco_field}")
    print(f"Candidate Level: {cand_level}")
    print(f"Skills: {skills}")
    print(f"Recommended Skills: {recommended_skills}")
    print(f"Recommended Courses: {recommended_courses}")

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        return "".join(page.extract_text() or "" for page in reader.pages)

def extract_resume_data(text):
    email_pattern = r"[\w\.-]+@[\w\.-]+"
    phone_pattern = r"\+?\d[\d -]{8,12}\d"
    skills_list = [
        "Python", "JavaScript", "Java", "SQL", "React", "Node.js", "C++", "HTML", "CSS", 
        "Machine Learning", "Data Science", "UI/UX Design", "Flutter", "Kotlin", "Swift", 
        "Django", "AWS", "Docker", "Kubernetes", "TensorFlow", "Pandas", "NLP", "Cybersecurity",
        "Business Analysis", "Project Management", "Salesforce", "SAP", "Excel", "Financial Modeling",
        "R", "Blockchain", "IoT", "Azure", "Google Cloud", "Network Security", "Penetration Testing"
    ]

    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    skills = [skill for skill in skills_list if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]

    return {
        'email': email.group(0) if email else 'N/A',
        'mobile_number': phone.group(0) if phone else 'N/A',
        'skills': skills
    }

def recommend_field_and_courses(skills):
    field_map = {
        'Software Development': ['Python', 'JavaScript', 'React', 'Node.js', 'C++', 'Java', 'Ruby', 'Go'],
        'Data Science': ['Python', 'Machine Learning', 'Data Science', 'Pandas', 'NumPy', 'TensorFlow'],
        'UI/UX Design': ['UI/UX Design', 'Figma', 'Adobe XD', 'Photoshop', 'Illustrator', 'Sketch'],
        'Mobile App Development': ['Flutter', 'Kotlin', 'Swift', 'React Native', 'Android', 'iOS'],
        'Web Development': ['HTML', 'CSS', 'JavaScript', 'React', 'Vue', 'Django', 'Flask'],
        'DevOps': ['AWS', 'Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'CI/CD'],
        'Cybersecurity': ['Network Security', 'Ethical Hacking', 'Penetration Testing', 'Cryptography'],
        'Cloud Computing': ['AWS', 'Google Cloud', 'Azure', 'Kubernetes', 'Serverless'],
        'Finance': ['Financial Modeling', 'Excel', 'Data Analysis', 'SQL'],
        'Project Management': ['Agile', 'Scrum', 'Project Planning', 'JIRA']
    }

    course_map = {
        'Python': ['Advanced Python Programming', 'Data Science with Python'],
        'JavaScript': ['JavaScript Mastery', 'React.js Essentials'],
        'Machine Learning': ['Machine Learning A-Z', 'Deep Learning Specialization'],
        'UI/UX Design': ['UI/UX Design Fundamentals', 'Adobe XD for Beginners'],
        'Flutter': ['Complete Flutter Bootcamp', 'Advanced Flutter UI'],
        'Project Management': ['Agile Fundamentals', 'Scrum Master Certification'],
        'Cybersecurity': ['Cybersecurity Basics', 'Network Security']
    }

    reco_field = 'General IT'
    max_matches = 0
    recommended_courses = []
    recommended_skills = skills

    for field, skill_set in field_map.items():
    # Count how many skills from skill_set are in the user's skills list
     matches = sum(1 for skill in skill_set if skill in skills)
     if matches > max_matches:
        max_matches = matches
        reco_field = field 

    for skill in skills:
        if skill in course_map:
            recommended_courses.extend(course_map[skill])

    recommended_courses = list(set(recommended_courses))
    return reco_field, recommended_skills, recommended_courses

@app.route('/analyze_resume', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400

        resume_file = request.files['resume']
        if resume_file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        save_dir = './Uploaded_Resumes'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        save_path = os.path.join(save_dir, resume_file.filename)
        resume_file.save(save_path)

        resume_text = extract_text_from_pdf(save_path)
        resume_data = extract_resume_data(resume_text)

        name = 'N/A'
        email = resume_data.get('email', 'N/A')
        mobile_number = resume_data.get('mobile_number', 'N/A')
        skills = resume_data.get('skills', [])
        no_of_pages = len(PyPDF2.PdfReader(save_path).pages)
        cand_level = "Fresher" if no_of_pages == 1 else "Intermediate" if no_of_pages == 2 else "Experienced"
        
        reco_field, recommended_skills, rec_course = recommend_field_and_courses(skills)
        resume_score = calculate_resume_score(resume_data, no_of_pages, skills, reco_field)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_data(name, email, resume_score, timestamp, no_of_pages, reco_field, cand_level, ','.join(skills), ','.join(recommended_skills), ','.join(rec_course))

        return jsonify({
            'name': name,
            'email': email,
            'mobile_number': mobile_number,
            'no_of_pages': no_of_pages,
            'cand_level': cand_level,
            'resume_score': resume_score,
            'recommended_field': reco_field,
            'recommended_skills': recommended_skills,
            'recommended_courses': rec_course
        })

    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)}), 500

def calculate_resume_score(resume_data, no_of_pages, skills, reco_field):
    score = 10 if resume_data.get('email') and resume_data.get('mobile_number') else 0
    score += min(len(skills) * 2, 20)
    score += min(no_of_pages * 10, 20)
    if reco_field != 'General IT':
        score += 10
    return min(score, 100)

