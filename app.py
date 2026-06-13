import streamlit as st
import os
from dotenv import load_dotenv

# Import helper functions from our custom modules
from resume_parser import extract_text_from_pdf
from ats_score import analyze_resume
from gemini_feedback import get_gemini_feedback
from utils import extract_text_from_file

# Load environment variables (such as GEMINI_API_KEY) from .env file
load_dotenv()

# Set Streamlit page configuration (title, icon, layout)
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS to give the app a premium, sleek look
st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');

    /* Apply custom font globally */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Main Title Styling with red/coral gradient */
    .main-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF8F8F 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        margin-bottom: 2px;
        text-align: center;
    }
    
    /* Subtitle Styling */
    .main-subtitle {
        color: #7f8c8d;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 35px;
    }

    /* Section Header Styling */
    .section-header {
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        border-bottom: 2px solid #FF4B4B30;
        padding-bottom: 8px;
        margin-top: 15px;
        margin-bottom: 15px;
        color: #2c3e50;
    }

    /* Beautiful Score Cards */
    .score-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    }
    .score-number {
        font-family: 'Outfit', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: #38bdf8;
        margin: 5px 0;
    }
    .score-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR CONFIGURATION -----------------
st.sidebar.markdown("### ⚙️ API Configuration")
st.sidebar.markdown(
    "This application uses **Google Gemini API** for personalized AI suggestions. "
    "Please provide your API key below."
)

# Check if Gemini API key exists in environment variables (loaded from .env)
env_api_key = os.getenv("GEMINI_API_KEY")

if not env_api_key:
    st.sidebar.warning("⚠️ GEMINI_API_KEY not found in `.env` file.")
    # Provide a text input for user to type/paste their API key directly
    user_api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
    if user_api_key:
        os.environ["GEMINI_API_KEY"] = user_api_key
        st.sidebar.success("✅ API Key configured successfully for this session!")
else:
    st.sidebar.success("✅ Gemini API Key loaded from `.env` file!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 About the Project")
st.sidebar.markdown(
    "**AI Resume Analyzer** is a beginner-friendly ATS scoring and AI feedback application. "
    "It uses keyword matching and semantic analysis to score resumes, and Gemini AI for resume recommendations."
)


# ----------------- MAIN APP USER INTERFACE -----------------

# Render the application title and subtitle
st.markdown("<div class='main-title'>AI Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Optimize your resume for Applicant Tracking Systems (ATS) with AI-powered feedback</div>", unsafe_allow_html=True)

# Create two columns for uploading inputs (Resume & Job Description)
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='section-header'>📄 1. Upload Resume</div>", unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload your resume (PDF format only):", type=["pdf"])

with col2:
    st.markdown("<div class='section-header'>💼 2. Job Description</div>", unsafe_allow_html=True)
    
    # Option to Paste Text or Upload File
    jd_mode = st.radio(
        "Choose how to input the Job Description:",
        options=["Paste Text", "Upload File (.txt or .pdf)"]
    )
    
    jd_text = ""
    if jd_mode == "Paste Text":
        jd_text = st.text_area(
            "Paste the job description here:",
            height=200,
            placeholder="Paste requirements, duties, and skills needed for the job..."
        )
    else:
        jd_file = st.file_uploader("Upload Job Description file:", type=["txt", "pdf"])
        if jd_file is not None:
            # Extract text from the uploaded txt/pdf file
            jd_text = extract_text_from_file(jd_file)
            if jd_text:
                st.success("✅ Job Description parsed successfully!")

st.markdown("<br>", unsafe_allow_html=True)

# Center-aligned Analyze button
analyze_button = st.button("🚀 Analyze Resume", use_container_width=True)

# Helper function to generate colored HTML tags for skills
def render_skills_tags(skills, color_hex):
    if not skills:
        return "<p style='color: #7f8c8d; font-style: italic;'>None found.</p>"
    
    tags = ""
    for skill in skills:
        tags += f"""
        <span style="
            display: inline-block;
            background-color: {color_hex}15;
            color: {color_hex};
            border: 1px solid {color_hex}50;
            border-radius: 20px;
            padding: 4px 12px;
            margin: 4px;
            font-size: 0.85rem;
            font-weight: 600;
        ">{skill}</span>
        """
    return tags

# Check if analyze button is pressed
if analyze_button:
    # 1. Validation: Ensure both inputs are provided
    if not resume_file:
        st.error("❌ Please upload a resume PDF file first.")
    elif not jd_text or len(jd_text.strip()) == 0:
        st.error("❌ Please provide a job description (either paste it or upload a file).")
    else:
        # Show a processing spinner
        with st.spinner("Analyzing resume and fetching AI suggestions..."):
            # 2. Extract text from resume
            resume_text = extract_text_from_pdf(resume_file)
            
            if not resume_text:
                st.error("❌ Could not extract text from the resume. Please ensure it is not a scanned image PDF.")
            else:
                # 3. Perform Match Analysis
                analysis_results = analyze_resume(resume_text, jd_text)
                
                # 4. Fetch Gemini AI suggestions
                ai_suggestions = get_gemini_feedback(resume_text, jd_text)
                
                # 5. Display Results
                st.markdown("<div class='section-header'>📊 Analysis Results</div>", unsafe_allow_html=True)
                
                # Create 3 columns for metrics / scores
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                # Column 1: Overall ATS Score (weighted)
                with metric_col1:
                    st.markdown(
                        f"""
                        <div class='score-card'>
                            <div class='score-label'>Overall ATS Score</div>
                            <div class='score-number'>{analysis_results['ats_score']}%</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                # Column 2: Keyword matching percentage
                with metric_col2:
                    st.markdown(
                        f"""
                        <div class='score-card'>
                            <div class='score-label'>Keyword Match</div>
                            <div class='score-number'>{int(analysis_results['keyword_score'])}%</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                # Column 3: Cosine Similarity (TF-IDF semantic matching)
                with metric_col3:
                    st.markdown(
                        f"""
                        <div class='score-card'>
                            <div class='score-label'>Semantic Similarity</div>
                            <div class='score-number'>{int(analysis_results['cosine_score'])}%</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                
                # Show an interactive progress bar for the overall score
                st.markdown("**Overall Fit Progress:**")
                st.progress(analysis_results['ats_score'] / 100)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Skills matching breakdowns
                skills_col1, skills_col2, skills_col3 = st.columns(3)
                
                with skills_col1:
                    st.markdown("### 🟢 Matched Skills")
                    st.markdown(
                        render_skills_tags(analysis_results['matched_skills'], "#2ecc71"),
                        unsafe_allow_html=True
                    )
                    
                with skills_col2:
                    st.markdown("### 🔴 Missing Skills")
                    st.markdown(
                        render_skills_tags(analysis_results['missing_skills'], "#e74c3c"),
                        unsafe_allow_html=True
                    )
                    
                with skills_col3:
                    st.markdown("### 🔵 Extra Skills in Resume")
                    st.markdown(
                        render_skills_tags(analysis_results['extra_skills'], "#3498db"),
                        unsafe_allow_html=True
                    )
                
                st.markdown("<br><hr>", unsafe_allow_html=True)
                
                # Display Gemini feedback
                st.markdown("<div class='section-header'>🤖 AI Analysis & Recommendations (Gemini API)</div>", unsafe_allow_html=True)
                st.markdown(ai_suggestions)
