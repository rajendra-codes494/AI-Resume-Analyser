import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# A predefined list of common industry skills (tech and soft skills)
# This list is used to find matching and missing skills between the resume and the job description.
COMMON_SKILLS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "C++", "C#", "C", "Go", "Rust", "Swift", "Kotlin", "Ruby", "PHP", "TypeScript", "HTML", "CSS", "SQL", "R",
    # Frameworks & Libraries
    "React", "Angular", "Vue", "Django", "Flask", "FastAPI", "Spring Boot", "Node.js", "Express", "jQuery", "Bootstrap", "Tailwind", "Next.js",
    # AI/ML/Data Science
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "Natural Language Processing", "Computer Vision", "TensorFlow", "PyTorch", "Keras", "Scikit-Learn", "Pandas", "NumPy", "Data Science", "Data Analysis", "Matplotlib", "Seaborn",
    # Cloud & DevOps
    "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "CI/CD", "Terraform", "Jenkins",
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis", "Oracle", "Firebase",
    # Tools & Methods
    "Agile", "Scrum", "Jira", "Linux", "Unix",
    # Soft Skills / Business
    "Project Management", "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking", "Time Management", "Creativity", "Negotiation"
]

def clean_text(text):
    """
    Cleans text by converting to lowercase and replacing extra whitespaces.
    This helps make text comparison more accurate.
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Replaces multiple spaces/newlines/tabs with a single space
    return text.strip()

def extract_skills(text, skills_list=COMMON_SKILLS):
    """
    Checks the text for skills from a predefined list.
    Uses regex word boundaries to avoid partial matching (e.g., matching "Java" in "JavaScript").
    """
    found_skills = set()
    cleaned_text = clean_text(text)
    
    for skill in skills_list:
        skill_lower = skill.lower()
        
        # We use word boundaries \b to match exact words.
        # We escape the skill name (like C++) in case it contains special regex characters.
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        
        # C++ and C# end with symbols that don't match standard word boundaries.
        # We handle them as a special case by not enforcing a boundary at the end.
        if skill_lower.endswith('++') or skill_lower.endswith('#'):
            pattern = r'\b' + re.escape(skill_lower)
            
        if re.search(pattern, cleaned_text):
            found_skills.add(skill)
            
    return found_skills

def calculate_cosine_similarity(text1, text2):
    """
    Calculates how similar two texts are using TF-IDF and Cosine Similarity from scikit-learn.
    This gives a score reflecting the overall context and word choice similarity.
    """
    try:
        # Preprocess both texts
        cleaned_text1 = clean_text(text1)
        cleaned_text2 = clean_text(text2)
        
        # If either text is empty, similarity is 0
        if not cleaned_text1 or not cleaned_text2:
            return 0.0
            
        # Create the TF-IDF Vectorizer
        vectorizer = TfidfVectorizer()
        # Convert texts to TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform([cleaned_text1, cleaned_text2])
        
        # Calculate Cosine Similarity between vector 0 (resume) and vector 1 (job description)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(round(similarity * 100, 2))
    except Exception as e:
        print(f"Error calculating cosine similarity: {e}")
        return 0.0

def analyze_resume(resume_text, jd_text):
    """
    Main function to compare resume text with job description text.
    Extracts matched, missing, and extra skills, and computes the final ATS Score.
    """
    # 1. Extract skills from both texts
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    # 2. Compare the extracted skills
    # Matched: Skills in BOTH resume and job description
    matched_skills = resume_skills.intersection(jd_skills)
    
    # Missing: Skills in job description but NOT in resume
    missing_skills = jd_skills.difference(resume_skills)
    
    # Extra: Skills in resume but NOT in job description
    extra_skills = resume_skills.difference(jd_skills)
    
    # 3. Calculate Scores
    # Keyword overlap score
    if len(jd_skills) > 0:
        keyword_score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        keyword_score = 0.0
        
    # Semantic similarity score
    cosine_score = calculate_cosine_similarity(resume_text, jd_text)
    
    # 4. Calculate Final ATS Score
    # We combine both scores: 60% weight to keyword matching and 40% to overall semantic similarity.
    # If the Job Description mentions no skills from our list, we rely 100% on overall semantic similarity.
    if len(jd_skills) > 0:
        final_ats_score = (keyword_score * 0.6) + (cosine_score * 0.4)
    else:
        final_ats_score = cosine_score
        
    # Round to nearest integer for clean display
    final_ats_score = int(round(final_ats_score))
    # Cap score between 0 and 100
    final_ats_score = max(0, min(final_ats_score, 100))
    
    return {
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),
        "extra_skills": list(extra_skills),
        "ats_score": final_ats_score,
        "keyword_score": round(keyword_score, 2),
        "cosine_score": cosine_score
    }
