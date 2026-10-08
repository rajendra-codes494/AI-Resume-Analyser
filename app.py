import streamlit as st
import os
from dotenv import load_dotenv

# Import helper functions from our custom modules
from resume_parser import extract_text_from_pdf
from ats_score import analyze_resume
from gemini_feedback import get_gemini_feedback, generate_job_description
from utils import extract_text_from_file

# Load environment variables
load_dotenv()

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Resume Analyzer | Organic Moody Luxury",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS & JS for Organic Warm Espresso & Botanical Leaf Aesthetics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Space+Grotesk:wght@400;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Base application background: Deep rich black to warm espresso gradient */
.stApp {
    background: radial-gradient(circle at 82% 18%, #2A1A14 0%, #170E0B 45%, #0A0605 100%) !important;
    color: #E3D7CC !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Botanical Leaves Silhouette Overlay on Top Right */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; right: 0;
    width: 680px; height: 680px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 800'%3E%3Cg fill='%23080504' opacity='0.78'%3E%3Cpath d='M800 0 Q680 120 540 320 Q690 220 800 0 Z'/%3E%3Cpath d='M800 120 Q640 260 480 480 Q660 360 800 120 Z'/%3E%3Cpath d='M720 0 Q580 160 460 360 Q600 240 720 0 Z'/%3E%3Cpath d='M800 280 Q660 420 520 620 Q700 500 800 280 Z'/%3E%3Cpath d='M620 0 Q480 180 380 420 Q520 280 620 0 Z'/%3E%3Cpath d='M800 420 Q680 560 600 750 Q740 640 800 420 Z'/%3E%3C/g%3E%3Cg fill='%231b110c' opacity='0.55'%3E%3Cpath d='M760 40 Q620 180 500 380 Q640 260 760 40 Z'/%3E%3Cpath d='M780 200 Q620 360 480 580 Q660 440 780 200 Z'/%3E%3C/g%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
    background-position: top right;
    pointer-events: none;
    z-index: 0;
    opacity: 0.88;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #0E0907 !important;
    border-right: 1px solid rgba(200, 122, 87, 0.2) !important;
}
[data-testid="stSidebar"] * {
    color: #A69B91;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #E3D7CC;
}

/* Headers */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', 'Space Grotesk', sans-serif;
    color: #F2E8DF !important;
    font-weight: 700;
}

/* Section headers for Gemini AI output */
h3 {
    color: #E6A17E !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.15rem !important;
    margin-top: 32px !important;
    margin-bottom: 16px !important;
    border-left: 3px solid #C87A57 !important;
    padding-left: 14px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}

/* Frosted Glassmorphism Containers & Inputs */
.stTextInput input, .stTextArea textarea,
.stTextInput > div > div > input, .stTextArea > div > textarea {
    background-color: rgba(26, 17, 14, 0.65) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    color: #F5EBE1 !important;
    border: 1px solid rgba(200, 122, 87, 0.35) !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
}

/* High-contrast peach/copper placeholder text */
::placeholder,
::-webkit-input-placeholder,
::-moz-placeholder,
:-ms-input-placeholder,
.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: rgba(227, 215, 204, 0.45) !important;
    opacity: 1 !important;
}

.stTextInput input:focus, .stTextArea textarea:focus,
.stTextInput > div > div > input:focus, .stTextArea > div > textarea:focus {
    border-color: #E6A17E !important;
    box-shadow: 0 0 20px rgba(230, 161, 126, 0.3) !important;
}

/* Radio Buttons & Option Labels */
label, .stRadio label, [data-testid="stRadio"] label, div[role="radiogroup"] label, div[role="radiogroup"] p {
    color: #E3D7CC !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.5px;
}

/* Radio active state dot indicator in glowing peach/copper */
div[role="radiogroup"] [data-checked="true"] div {
    background-color: #E6A17E !important;
    border-color: #E6A17E !important;
    box-shadow: 0 0 10px rgba(230, 161, 126, 0.5) !important;
}

/* File Uploader Dropzone - Frosted Glass Dark Espresso */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] section,
[data-testid="stFileUploadDropzone"],
[data-testid="stFileUploadDropzone"] > div,
[data-testid="stFileUploaderDropzone"],
.stFileUploader section {
    background-color: rgba(26, 17, 14, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px dashed rgba(200, 122, 87, 0.4) !important;
    border-radius: 12px !important;
    color: #F5EBE1 !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploadDropzone"]:hover {
    border-color: #E6A17E !important;
    background-color: rgba(36, 23, 19, 0.75) !important;
    box-shadow: 0 0 25px rgba(200, 122, 87, 0.25) !important;
}

[data-testid="stFileUploader"] *,
[data-testid="stFileUploadDropzone"] *,
[data-testid="stFileUploaderDropzone"] *,
.stFileUploader * {
    color: #E3D7CC !important;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploadDropzone"] small,
[data-testid="stFileUploaderDropzone"] small {
    color: #B3A69B !important;
}

/* Upload Button inside File Dropzone - Warm Copper fill with Peach Text */
[data-testid="stFileUploader"] button,
[data-testid="stFileUploadDropzone"] button,
[data-testid="stFileUploaderDropzone"] button {
    background-color: rgba(180, 115, 80, 0.35) !important;
    color: #F2B897 !important;
    border: 1px solid rgba(230, 161, 126, 0.5) !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 7px 18px !important;
    transition: all 0.25s ease !important;
}

[data-testid="stFileUploader"] button *,
[data-testid="stFileUploadDropzone"] button *,
[data-testid="stFileUploaderDropzone"] button * {
    color: #F2B897 !important;
}

[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploadDropzone"] button:hover {
    background-color: #C87A57 !important;
    color: #150D0A !important;
}
[data-testid="stFileUploader"] button:hover *,
[data-testid="stFileUploadDropzone"] button:hover * {
    color: #150D0A !important;
}

/* Radio Buttons Container */
.stRadio > div {
    display: flex;
    flex-direction: row;
    gap: 20px;
}

/* Secondary Buttons */
.stButton > button {
    background-color: rgba(26, 17, 14, 0.65) !important;
    backdrop-filter: blur(12px) !important;
    color: #F2B897 !important;
    border: 1px solid rgba(200, 122, 87, 0.35) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600 !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.stButton > button:hover {
    border-color: #E6A17E !important;
    color: #F5EBE1 !important;
    box-shadow: 0 0 18px rgba(200, 122, 87, 0.3) !important;
    transform: translateY(-1px);
}

/* MAIN ACTION BUTTON: Luminous Warm Metallic Copper Gradient Bar */
.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #7A432F 0%, #B85C38 30%, #F2B897 50%, #B85C38 70%, #7A432F 100%) !important;
    color: #150E0B !important;
    border: 1px solid rgba(242, 184, 151, 0.4) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1.05rem !important;
    padding: 12px 24px !important;
    border-radius: 10px !important;
    height: 56px !important;
    letter-spacing: 2px;
    box-shadow: 0 8px 32px rgba(200, 122, 87, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #B85C38 0%, #E6A17E 30%, #F8E5D8 50%, #E6A17E 70%, #B85C38 100%) !important;
    color: #150E0B !important;
    box-shadow: 0 12px 40px rgba(230, 161, 126, 0.55) !important;
    transform: translateY(-2px);
}

/* Organic Warm Custom Classes */
.brand-area {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 2px;
    color: #F5EBE1;
    margin-bottom: 30px;
    border-bottom: 1px solid rgba(200, 122, 87, 0.25);
    padding-bottom: 15px;
}
.brand-accent {
    background: linear-gradient(135deg, #F2B897, #E6A17E, #C87A57);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.status-card {
    background-color: rgba(26, 17, 14, 0.65);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(200, 122, 87, 0.25);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 20px;
}
.status-connected {
    color: #48C78E;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 1px;
}
.status-disconnected {
    color: #E76F51;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 1px;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background-color: rgba(26, 17, 14, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(200, 122, 87, 0.45);
    color: #F2B897;
    padding: 6px 18px;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 20px;
    box-shadow: 0 0 20px rgba(200, 122, 87, 0.2);
}
.hero-title {
    font-family: 'Outfit', 'Space Grotesk', sans-serif;
    font-size: 3.8rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 12px;
    color: #F5EBE1;
    letter-spacing: -1px;
}
.hero-title-highlight {
    background: linear-gradient(135deg, #F8E5D8, #F2B897, #E6A17E, #C87A57);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 15px rgba(200, 122, 87, 0.35));
}
.hero-subtitle {
    font-size: 1.18rem;
    color: #C8BFB5;
    margin-bottom: 35px;
    font-weight: 400;
}
.panel-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.95rem;
    font-weight: 700;
    color: #E6A17E !important;
    letter-spacing: 1.5px;
    margin-bottom: 15px;
}
.panel-number {
    color: #F2B897 !important;
    margin-right: 8px;
}

/* Frosted Glass Cards for Results Dashboard */
.metric-card-primary, .metric-card-secondary, .skills-card {
    position: relative;
    background-color: rgba(26, 17, 14, 0.65) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(200, 122, 87, 0.3) !important;
    border-radius: 14px !important;
    padding: 26px;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 10px 32px rgba(0, 0, 0, 0.5);
}
.metric-card-primary:hover, .metric-card-secondary:hover, .skills-card:hover {
    border-color: rgba(230, 161, 126, 0.6) !important;
    box-shadow: 0 0 30px rgba(200, 122, 87, 0.25), 0 12px 35px rgba(0,0,0,0.65) !important;
    transform: translateY(-3px);
}

.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #B3A69B;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
    margin-bottom: 14px;
}
.metric-value-large {
    font-family: 'Outfit', sans-serif;
    font-size: 4.2rem;
    font-weight: 800;
    color: #F2B897;
    line-height: 1;
    text-shadow: 0 0 25px rgba(200, 122, 87, 0.4);
}
.metric-value-small {
    font-family: 'Outfit', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #F5EBE1;
    line-height: 1;
}
.custom-progress-container {
    width: 100%;
    background-color: rgba(40, 26, 21, 0.8);
    border: 1px solid rgba(200, 122, 87, 0.2);
    border-radius: 4px;
    height: 8px;
    margin-top: 25px;
    margin-bottom: 10px;
    overflow: hidden;
}
.custom-progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #8C523B, #C87A57, #F2B897);
    border-radius: 4px;
    box-shadow: 0 0 14px rgba(200, 122, 87, 0.5);
    transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
}
.skills-card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 15px;
    letter-spacing: 1px;
    color: #F5EBE1;
}
.skill-tag {
    display: inline-block;
    padding: 5px 14px;
    border-radius: 6px;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 4px;
    border: 1px solid;
    transition: all 0.2s ease;
}
.skill-tag:hover {
    transform: translateY(-1px);
}
.skill-tag-matched { background-color: rgba(72, 199, 142, 0.1); border-color: rgba(72, 199, 142, 0.4); color: #48C78E; }
.skill-tag-missing { background-color: rgba(231, 111, 81, 0.1); border-color: rgba(231, 111, 81, 0.4); color: #E76F51; }
.skill-tag-extra { background-color: rgba(230, 161, 126, 0.1); border-color: rgba(230, 161, 126, 0.4); color: #F2B897; }

/* Hide default streamlit UI headers */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ----------------- SIDEBAR CONFIGURATION -----------------
with st.sidebar:
    st.markdown("""
        <div class="brand-area">
            ◈ AI RESUME<br><span class="brand-accent">ANALYZER</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='panel-title'>AI CONFIGURATION</div>", unsafe_allow_html=True)
    
    env_api_key = os.getenv("GEMINI_API_KEY")
    if not env_api_key:
        st.markdown("""
            <div class="status-card">
                <div class="status-disconnected">○ API KEY REQUIRED</div>
            </div>
        """, unsafe_allow_html=True)
        user_api_key = st.text_input("Enter Gemini API Key:", type="password")
        if user_api_key:
            os.environ["GEMINI_API_KEY"] = user_api_key
            st.success("API Key configured for this session")
    else:
        st.markdown("""
            <div class="status-card">
                <div class="status-connected">✓ API KEY CONNECTED</div>
                <div style="font-size: 0.8rem; color: #B3A69B; margin-top: 5px;">Loaded from environment</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>ABOUT SYSTEM</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="status-card" style="color: #C8BFB5; font-size: 0.88rem; line-height: 1.6;">
            AI Resume Analyzer uses:<br>
            • Executive ATS scoring<br>
            • Keyword matching<br>
            • Semantic vector similarity<br>
            • Gemini AI recommendations
        </div>
    """, unsafe_allow_html=True)


# ----------------- MAIN APP USER INTERFACE -----------------

st.markdown("""
    <div class="hero-badge">+ EXECUTIVE ATS INTELLIGENCE</div>
    <div class="hero-title">AI RESUME <span class="hero-title-highlight">ANALYZER</span></div>
    <div class="hero-subtitle">Optimize your professional profile with AI-driven ATS precision.</div>
    <div style="height: 1px; background: linear-gradient(90deg, rgba(200, 122, 87, 0.4), rgba(200, 122, 87, 0.05)); margin-bottom: 40px;"></div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<div class='panel-title'><span class='panel-number'>01</span> UPLOAD RESUME</div>", unsafe_allow_html=True)
    resume_file = st.file_uploader("Upload your resume for ATS analysis. (PDF only)", type=["pdf"], label_visibility="collapsed")
    if resume_file:
        st.markdown(f"""
            <div style="background-color: rgba(26, 17, 14, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(200, 122, 87, 0.45); padding: 15px; border-radius: 10px; margin-top: -15px; color: #F5EBE1;">
                <span style="color: #F2B897; margin-right: 8px;">✓</span> <b>{resume_file.name}</b> ({(resume_file.size/1024):.1f} KB)
            </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("<div class='panel-title'><span class='panel-number'>02</span> TARGET JOB DESCRIPTION</div>", unsafe_allow_html=True)
    
    if "jd_text" not in st.session_state:
        st.session_state.jd_text = ""
        
    jd_mode = st.radio(
        "Choose Input Method",
        options=["Paste Text", "Upload File", "Auto-Generate with AI"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if jd_mode == "Paste Text":
        jd_text = st.text_area(
            "Paste Job Description",
            value=st.session_state.jd_text,
            height=200,
            label_visibility="collapsed",
            placeholder="Paste requirements, duties, and skills needed for the target role..."
        )
        st.session_state.jd_text = jd_text
        
    elif jd_mode == "Upload File":
        jd_file = st.file_uploader("Upload Job Description (.txt or .pdf)", type=["txt", "pdf"], label_visibility="collapsed")
        if jd_file is not None:
            extracted_text = extract_text_from_file(jd_file)
            if extracted_text:
                st.session_state.jd_text = extracted_text
                st.success("✅ Job Description parsed successfully!")
        jd_text = st.session_state.jd_text
        if jd_text:
            jd_text = st.text_area("Preview (Edit if needed):", value=jd_text, height=150, label_visibility="collapsed")
            st.session_state.jd_text = jd_text
            
    elif jd_mode == "Auto-Generate with AI":
        c_title, c_exp = st.columns(2)
        with c_title:
            job_title = st.text_input("JOB TITLE", placeholder="e.g. Senior Software Engineer")
        with c_exp:
            experience = st.text_input("EXPECTED EXPERIENCE", placeholder="e.g. 5+ years")
            
        if st.button("✦ GENERATE JOB DESCRIPTION"):
            if not job_title or not experience:
                st.warning("Please provide both Job Title and Expected Experience.")
            else:
                with st.spinner("Generating job description..."):
                    generated_jd = generate_job_description(job_title, experience)
                    st.session_state.jd_text = generated_jd
        
        jd_text = st.text_area(
            "Review and Edit Job Description:",
            value=st.session_state.jd_text,
            height=150,
            label_visibility="collapsed"
        )
        st.session_state.jd_text = jd_text

st.markdown("<div style='margin-top: 35px;'></div>", unsafe_allow_html=True)

# Center-aligned Main Action Button (Luminous Warm Metallic Copper Gradient Bar)
analyze_button = st.button("✦ ANALYZE RESUME →", type="primary", use_container_width=True)

# Helper function for rendering skill badges
def render_skill_badges(skills, tag_class):
    if not skills:
        return "<span style='color: #B3A69B; font-style: italic;'>None detected</span>"
    return "".join([f"<span class='skill-tag {tag_class}'>{s}</span>" for s in skills])

if analyze_button:
    if not resume_file:
        st.error("Please upload a resume PDF file first.")
    elif not jd_text or len(jd_text.strip()) == 0:
        st.error("Please provide a job description.")
    else:
        st.markdown("<div style='text-align: center; color: #F2B897; margin: 25px 0; font-weight: 700; letter-spacing: 2px;'>✦ EVALUATING EXECUTIVE ATS MATCH...</div>", unsafe_allow_html=True)
        
        with st.spinner("Processing structural parsing & semantic analysis..."):
            resume_text = extract_text_from_pdf(resume_file)
            
            if not resume_text:
                st.error("Could not extract text from the resume.")
            else:
                analysis_results = analyze_resume(resume_text, jd_text)
                ai_suggestions = get_gemini_feedback(resume_text, jd_text)
                
                # Results UI Dashboard
                st.markdown("""
                    <div style="margin-top: 50px;">
                        <span class="hero-badge" style="border-color: #E6A17E; color: #F2B897; margin-bottom: 10px;">✦ ANALYSIS COMPLETE</span>
                        <div class="panel-title" style="font-size: 1.2rem; color: #F5EBE1;">ATS EVALUATION RESULTS</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Top Metrics
                col_res1, col_res2 = st.columns([1.2, 1], gap="large")
                
                with col_res1:
                    st.markdown(f"""
                        <div class="metric-card-primary">
                            <div class="metric-label">OVERALL ATS SCORE</div>
                            <div class="metric-value-large">{analysis_results['ats_score']}%</div>
                            <div class="custom-progress-container">
                                <div class="custom-progress-bar" style="width: {analysis_results['ats_score']}%;"></div>
                            </div>
                            <div style="color: #B3A69B; font-size: 0.88rem; text-align: right; margin-top: -5px;">ATS COMPATIBILITY RATING</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_res2:
                    st.markdown(f"""
                        <div class="metric-card-secondary" style="margin-bottom: 20px;">
                            <div class="metric-label">KEYWORD DENSITY MATCH</div>
                            <div class="metric-value-small">{int(analysis_results['keyword_score'])}%</div>
                        </div>
                        <div class="metric-card-secondary">
                            <div class="metric-label">SEMANTIC SIMILARITY</div>
                            <div class="metric-value-small">{int(analysis_results['cosine_score'])}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
                st.markdown("<div class='panel-title'>SKILL VECTOR BREAKDOWN</div>", unsafe_allow_html=True)
                
                # Skills matching breakdowns
                scol1, scol2, scol3 = st.columns(3, gap="medium")
                
                with scol1:
                    st.markdown(f"""
                        <div class="skills-card">
                            <div class="skills-card-title"><span style="color: #48C78E; margin-right: 6px;">✓</span> MATCHED SKILLS</div>
                            {render_skill_badges(analysis_results['matched_skills'], 'skill-tag-matched')}
                        </div>
                    """, unsafe_allow_html=True)
                    
                with scol2:
                    st.markdown(f"""
                        <div class="skills-card">
                            <div class="skills-card-title"><span style="color: #E76F51; margin-right: 6px;">✕</span> MISSING SKILLS</div>
                            {render_skill_badges(analysis_results['missing_skills'], 'skill-tag-missing')}
                        </div>
                    """, unsafe_allow_html=True)
                    
                with scol3:
                    st.markdown(f"""
                        <div class="skills-card">
                            <div class="skills-card-title"><span style="color: #F2B897; margin-right: 6px;">+</span> ADDITIONAL SKILLS</div>
                            {render_skill_badges(analysis_results['extra_skills'], 'skill-tag-extra')}
                        </div>
                    """, unsafe_allow_html=True)
                
                # Gemini AI Insights
                st.markdown("""
                    <div style="margin-top: 50px; padding: 40px; background-color: rgba(26, 17, 14, 0.7); backdrop-filter: blur(14px); border: 1px solid rgba(200, 122, 87, 0.35); border-radius: 14px; box-shadow: 0 10px 32px rgba(0,0,0,0.5);">
                        <span class="hero-badge" style="margin-bottom: 12px;">✦ AI STRATEGIC RECOMMENDATIONS</span>
                        <div style="color: #C8BFB5; margin-bottom: 30px; font-size: 1.05rem;">Personalized optimization feedback tailored for executive resume screening.</div>
                """, unsafe_allow_html=True)
                
                st.markdown(ai_suggestions)
                
                st.markdown("</div>", unsafe_allow_html=True)
