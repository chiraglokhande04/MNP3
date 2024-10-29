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

# try:
#     df = pd.read_pickle('df.pkl')
#     similarity = pickle.load(open('similarity.pkl', 'rb'))
# except Exception as e:
#     print(f"Error loading files: {e}")
#     df = None
#     similarity = None

# def recommendation(title):
#     if df is None or similarity is None:
#         print("DataFrame or similarity matrix not loaded.")
#         return []

#     title = title.strip().lower()
#     df.reset_index(drop=True, inplace=True)
#     df.columns = df.columns.str.strip()

#     if 'Title' not in df.columns:
#         print("Error: 'Title' column missing.")
#         return []

#     try:
#         idx = df[df['Title'].str.lower() == title].index[0]
#         distances = similarity[idx]
#         similar_jobs = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:21]
#         jobs = [
#             {
#                 'Title': df.iloc[i].Title,
#                 'Position': df.iloc[i].Position,
#                 'Company': df.iloc[i].Company,
#                 'Status': df.iloc[i].Status,
#                 'JobDescription': df.iloc[i]['Job.Description']
#             }
#             for i, _ in similar_jobs if i < len(df) and 'Job.Description' in df.columns
#         ]
#         return jobs if jobs else "No similar jobs found."

#     except IndexError:
#         print("Job title not found in DataFrame.")
#         return []

# @app.route('/recommend', methods=['POST'])
# def recommend_jobs():
#     try:
#         data = request.json
#         job_title = data.get('title')
#         if not job_title:
#             return jsonify({'status': 'failure', 'message': 'Job title is required'}), 400

#         recommendations = recommendation(job_title)
#         if recommendations:
#             return jsonify({'status': 'success', 'recommendations': recommendations})
#         else:
#             return jsonify({'status': 'failure', 'message': 'Job title not found or no recommendations available'}), 404
#     except Exception as e:
#         return jsonify({'status': 'failure', 'message': str(e)}), 500





# Load data from sample_data directly
sample_data = [
    # Software Engineering roles
    {"Title": "Software Engineer", "Company": "TechCorp", "Job.Description": "Develop and maintain software applications.", "Status": "open"},
    {"Title": "Software Engineer", "Company": "Innovatech", "Job.Description": "Work on core product development and code optimization.", "Status": "closed"},
    {"Title": "Backend Developer", "Company": "CodeCrafters", "Job.Description": "Build and maintain scalable backend systems.", "Status": "open"},
    {"Title": "Frontend Developer", "Company": "WebDynamics", "Job.Description": "Create interactive user interfaces with React.", "Status": "open"},
    {"Title": "Full Stack Developer", "Company": "NextGenSoft", "Job.Description": "Develop both client and server software.", "Status": "open"},

    # Web Development roles
    {"Title": "Web Developer", "Company": "WebWizards", "Job.Description": "Create and maintain websites and web applications.", "Status": "open"},
    {"Title": "Front-End Developer", "Company": "NetDesigns", "Job.Description": "Develop UI/UX for web platforms.", "Status": "closed"},
    {"Title": "Back-End Developer", "Company": "StackBuild", "Job.Description": "Manage server-side web logic and databases.", "Status": "open"},
    {"Title": "UI/UX Designer", "Company": "CreatiDesign", "Job.Description": "Design user-friendly interfaces for web and mobile apps.", "Status": "open"},
    {"Title": "Web Developer", "Company": "PixelPerfect", "Job.Description": "Design responsive web pages.", "Status": "closed"},

    # App Development roles
    {"Title": "App Developer", "Company": "Appify", "Job.Description": "Develop and maintain mobile applications.", "Status": "open"},
    {"Title": "iOS Developer", "Company": "AppleSoft", "Job.Description": "Build and optimize apps for iOS devices.", "Status": "closed"},
    {"Title": "Android Developer", "Company": "DroidMakers", "Job.Description": "Create applications for the Android platform.", "Status": "open"},
    {"Title": "Cross-Platform Developer", "Company": "FlexiApps", "Job.Description": "Develop applications that work on multiple platforms.", "Status": "closed"},
    {"Title": "React Native Developer", "Company": "MobileHub", "Job.Description": "Build mobile applications with React Native.", "Status": "open"},

    # Data Science roles
    {"Title": "Data Scientist", "Company": "DataMine", "Job.Description": "Analyze large data sets to derive insights.", "Status": "open"},
    {"Title": "Machine Learning Engineer", "Company": "SmartAnalytics", "Job.Description": "Develop ML algorithms for data analysis.", "Status": "closed"},
    {"Title": "Data Analyst", "Company": "MetricSphere", "Job.Description": "Extract and interpret data trends for business decisions.", "Status": "open"},
    {"Title": "Data Engineer", "Company": "DataFlow", "Job.Description": "Develop and optimize data pipelines.", "Status": "closed"},
    {"Title": "AI Engineer", "Company": "DeepVision", "Job.Description": "Build AI-driven solutions for image processing.", "Status": "open"},

    # Machine Learning and AI roles
    {"Title": "ML Engineer", "Company": "MLLab", "Job.Description": "Develop machine learning models and pipelines.", "Status": "open"},
    {"Title": "AI Researcher", "Company": "DeepMindLab", "Job.Description": "Research and develop deep learning solutions.", "Status": "closed"},
    {"Title": "Deep Learning Engineer", "Company": "VisionAI", "Job.Description": "Develop CNN models for image processing.", "Status": "open"},
    {"Title": "NLP Engineer", "Company": "SpeakTech", "Job.Description": "Build NLP solutions for text data.", "Status": "closed"},
    {"Title": "Robotics Engineer", "Company": "AutoBotics", "Job.Description": "Design and develop algorithms for robotic automation.", "Status": "open"},

    # DevOps and System Administration roles
    {"Title": "DevOps Engineer", "Company": "CloudOps", "Job.Description": "Automate deployment and monitoring processes.", "Status": "open"},
    {"Title": "System Administrator", "Company": "SysManage", "Job.Description": "Maintain servers and IT systems.", "Status": "open"},
    {"Title": "Network Engineer", "Company": "NetSecure", "Job.Description": "Manage and maintain network infrastructure.", "Status": "open"},
    {"Title": "Cloud Architect", "Company": "Cloudify", "Job.Description": "Design and oversee cloud solutions.", "Status": "closed"},
    {"Title": "Cybersecurity Specialist", "Company": "SecureSphere", "Job.Description": "Monitor and secure network and data systems.", "Status": "closed"},

    # Product and Project Management roles
    {"Title": "Product Manager", "Company": "InnoSoft", "Job.Description": "Oversee product development from concept to launch.", "Status": "closed"},
    {"Title": "Project Manager", "Company": "PlanIt", "Job.Description": "Coordinate teams to meet project goals and timelines.", "Status": "open"},
    {"Title": "Technical Program Manager", "Company": "TechLead", "Job.Description": "Manage technical programs across multiple teams.", "Status": "open"},
    {"Title": "Scrum Master", "Company": "AgilePath", "Job.Description": "Facilitate Agile processes for development teams.", "Status": "closed"},
    {"Title": "Business Analyst", "Company": "InsightGen", "Job.Description": "Analyze business requirements and document solutions.", "Status": "open"},
    {"Title": "Software Engineer", "Company": "TechGlobal", "Job.Description": "Design and develop scalable software solutions.", "Status": "open"},
    {"Title": "UI/UX Designer", "Company": "CreativeMinds", "Job.Description": "Enhance user experience with creative design solutions.", "Status": "open"},
    {"Title": "Data Analyst", "Company": "InsightfulData", "Job.Description": "Analyze data trends to support business decisions.", "Status": "closed"},
    {"Title": "Business Intelligence Analyst", "Company": "BIWorks", "Job.Description": "Develop BI dashboards and data reports for strategic insights.", "Status": "open"},
    {"Title": "Network Security Specialist", "Company": "SecureNet", "Job.Description": "Implement security protocols to protect network systems.", "Status": "closed"},
    {"Title": "Blockchain Developer", "Company": "CryptoLab", "Job.Description": "Design and develop blockchain-based applications.", "Status": "open"},
    {"Title": "Full Stack Engineer", "Company": "CodeWorld", "Job.Description": "Develop client and server-side applications.", "Status": "open"},
    {"Title": "Game Developer", "Company": "PlaySmart", "Job.Description": "Create engaging video game experiences for various platforms.", "Status": "closed"},
    {"Title": "Cloud Architect", "Company": "SkyHighTech", "Job.Description": "Design cloud infrastructure for scalable applications.", "Status": "open"},
    {"Title": "IT Project Manager", "Company": "ITWorks", "Job.Description": "Coordinate and manage IT projects to ensure timely delivery.", "Status": "open"},

    # Data Science and Machine Learning Jobs
    {"Title": "Data Scientist", "Company": "DataInnovators", "Job.Description": "Model data to extract actionable insights.", "Status": "open"},
    {"Title": "ML Engineer", "Company": "AI Frontier", "Job.Description": "Develop machine learning models for predictive analytics.", "Status": "closed"},
    {"Title": "NLP Engineer", "Company": "Textify", "Job.Description": "Build natural language processing tools for text data analysis.", "Status": "open"},
    {"Title": "Computer Vision Engineer", "Company": "VisionaryTech", "Job.Description": "Develop vision-based AI solutions.", "Status": "closed"},
    {"Title": "Big Data Engineer", "Company": "DataFlow Solutions", "Job.Description": "Build large-scale data pipelines for analysis.", "Status": "open"},

    # Cybersecurity and IT Infrastructure Jobs
    {"Title": "Cybersecurity Analyst", "Company": "SafeNet", "Job.Description": "Monitor and defend against cybersecurity threats.", "Status": "closed"},
    {"Title": "System Engineer", "Company": "ComputeSys", "Job.Description": "Maintain and optimize IT systems and infrastructure.", "Status": "open"},
    {"Title": "Cloud Security Specialist", "Company": "CloudSecure", "Job.Description": "Ensure data and applications are secure in cloud environments.", "Status": "open"},
    {"Title": "IT Support Technician", "Company": "TechAssist", "Job.Description": "Provide technical support and troubleshooting.", "Status": "closed"},

    # Commerce and Business Jobs
    {"Title": "Financial Analyst", "Company": "FinanceFirst", "Job.Description": "Analyze financial data to guide business decisions.", "Status": "open"},
    {"Title": "Accountant", "Company": "Numbers & Co", "Job.Description": "Manage accounts and financial statements.", "Status": "closed"},
    {"Title": "Sales Executive", "Company": "SalesForce", "Job.Description": "Drive sales and manage client relationships.", "Status": "open"},
    {"Title": "Marketing Specialist", "Company": "MarketPros", "Job.Description": "Develop and execute marketing campaigns.", "Status": "open"},
    {"Title": "Operations Manager", "Company": "BizOps", "Job.Description": "Oversee and optimize daily business operations.", "Status": "closed"},
    {"Title": "Human Resources Manager", "Company": "PeopleFirst", "Job.Description": "Manage recruitment, training, and employee relations.", "Status": "open"},
    {"Title": "Supply Chain Analyst", "Company": "SupplyNet", "Job.Description": "Analyze and optimize supply chain processes.", "Status": "closed"},
    {"Title": "Product Manager", "Company": "Innovate Inc.", "Job.Description": "Oversee product development from concept to launch.", "Status": "open"},
    {"Title": "Customer Support Specialist", "Company": "HelpDesk", "Job.Description": "Assist customers and resolve inquiries.", "Status": "closed"},

    # Other Specialized Roles
    {"Title": "Real Estate Analyst", "Company": "PropertyPros", "Job.Description": "Evaluate market trends for real estate investments.", "Status": "open"},
    {"Title": "Investment Banker", "Company": "FinanceHub", "Job.Description": "Manage investment portfolios and provide financial advice.", "Status": "closed"},
    {"Title": "Supply Chain Manager", "Company": "LogiCorp", "Job.Description": "Oversee logistics and supply chain operations.", "Status": "open"},
    {"Title": "Data Privacy Consultant", "Company": "PrivacyGuard", "Job.Description": "Advise on data protection and privacy compliance.", "Status": "open"},
    {"Title": "Quality Assurance Specialist", "Company": "TechQuality", "Job.Description": "Ensure products meet quality standards.", "Status": "closed"}
]



# Convert sample_data to a DataFrame
df = pd.DataFrame(sample_data)

# Dummy similarity matrix for recommendation (to avoid loading from 'similarity.pkl')
similarity = [[1 for _ in range(len(df))] for _ in range(len(df))]  # Placeholder, assuming all jobs are equally similar

# Recommendation function
def recommendation(title):
    title = title.strip().lower()
    df.reset_index(drop=True, inplace=True)
    df.columns = df.columns.str.strip()

    # Ensure required column exists
    if 'Title' not in df.columns:
        print("Error: 'Title' column missing.")
        return []

    # Filter DataFrame for exact matches on title
    exact_matches = df[df['Title'].str.lower() == title]
    if not exact_matches.empty:
        idx = exact_matches.index[0]
        distances = similarity[idx] if idx < len(similarity) else [1] * len(df)
        similar_jobs = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:21]

        # Only recommend jobs with the exact title
        jobs = [
            {
                'Title': df.iloc[i].Title,
                'Company': df.iloc[i].Company,
                'Status': df.iloc[i].Status,
                'JobDescription': df.iloc[i]['Job.Description']
            }
            for i, _ in similar_jobs if i < len(df) and df.iloc[i].Title.lower() == title
        ]
        return jobs if jobs else "No similar jobs found."
    
    # If no exact match, look for partial matches
    matches = df[df['Title'].str.lower().str.contains(title)]
    if not matches.empty:
        jobs = matches[['Title', 'Company', 'Status', 'Job.Description']].to_dict(orient='records')
        return jobs
    else:
        return "Job title not found in dataset."


# API endpoint
@app.route('/recommend', methods=['POST'])
def recommend_jobs():
    try:
        data = request.json
        job_title = data.get('title')
        
        if not job_title:
            return jsonify({'status': 'failure', 'message': 'Job title is required'}), 400

        # Call the recommendation function
        recommendations = recommendation(job_title)

        # Check if recommendations were found
        if isinstance(recommendations, list) and recommendations:
            return jsonify({'status': 'success', 'recommendations': recommendations}), 200
        else:
            return jsonify({'status': 'failure', 'message': recommendations}), 404

    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)}), 500


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

        save_dir = '/tmp'
        save_path = os.path.join(save_dir, resume_file.filename)

        # Save the resume file
        try:
            resume_file.save(save_path)
            print(f"Resume saved successfully at: {save_path}")
        except Exception as e:
            print(f"Error saving resume file: {e}")
            return jsonify({"error": "Could not save the resume file"}), 500

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

