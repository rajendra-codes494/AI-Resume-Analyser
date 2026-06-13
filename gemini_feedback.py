import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from the .env file (if it exists)
load_dotenv()

def get_gemini_feedback(resume_text, jd_text):
    """
    Sends the resume text and the job description to the Google Gemini API.
    
    Parameters:
    - resume_text: The full text extracted from the user's PDF resume.
    - jd_text: The job description text.
    
    Returns:
    - A markdown-formatted string containing Gemini's critique and advice.
    """
    # 1. Retrieve the Gemini API key from the environment
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Check if the API key is missing
    if not api_key:
        return (
            "### API Key Missing\n"
            "Please create a `.env` file in the project directory and add your API key:\n"
            "```text\n"
            "GEMINI_API_KEY=your_actual_api_key_here\n"
            "```\n"
            "Or configure it in your system's environment variables."
        )
        
    try:
        # 2. Configure the Generative AI library with the API key
        genai.configure(api_key=api_key)
        
        # 3. Initialize the Gemini 1.5 Flash model
        # gemini-1.5-flash is optimized for fast responses and high quality.
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # 4. Construct a clear, structured prompt for the AI
        prompt = f"""
        You are an expert technical recruiter and career mentor. 
        I want you to analyze the Resume text below against the Job Description. 
        
        Please provide detailed, constructive, and action-oriented feedback structured exactly under these headings:
        
        ### 1. Suggested Missing Skills
        Identify specific skills, tools, or domain knowledge mentioned in the Job Description that are missing or not prominently featured in the Resume. Explain why they are important.
        
        ### 2. Weak Resume Points & Improvements
        Find 2 to 3 points in the Resume that are weak, passive, or lack measurable outcomes (metrics, percentages, etc.). Show "Before" (from resume) and "After" (suggested rewrite) examples.
        
        ### 3. Action Verbs Recommendations
        List 5 to 7 powerful action verbs that would strengthen the Resume based on the job description requirements.
        
        ### 4. Overall Feedback
        Give an honest, encouraging, and clear final assessment of how well the resume aligns with the job description.
        
        ---
        **RESUME TEXT:**
        {resume_text}
        
        ---
        **JOB DESCRIPTION:**
        {jd_text}
        """
        
        # 5. Generate content using the model
        response = model.generate_content(prompt)
        
        # Return the generated text
        return response.text
        
    except Exception as e:
        # Return a helpful error message if the API call fails
        return f"### Error getting feedback\nAn error occurred while connecting to the Gemini API: {str(e)}"
