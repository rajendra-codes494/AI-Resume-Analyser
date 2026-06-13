# AI Resume Analyzer 💼

## Brief One Line Summary
An AI-powered resume evaluation tool that scores resumes against job descriptions using ATS-style keyword matching, semantic similarity, and Google Gemini feedback.

---

## Overview
This project analyzes an uploaded PDF resume and a job description to estimate how well the resume matches the role. It computes a combined ATS score, identifies matched/missing skills, and offers AI-powered suggestions to improve the resume.

The app is implemented in Python with a Streamlit interface, making it easy to run locally and customize for your own resume review workflow.

---

## Problem Statement
Job seekers often struggle to tailor their resumes for Applicant Tracking Systems (ATS) and hiring managers. This project addresses that gap by:

- Extracting text from PDF resumes.
- Comparing resume content with job descriptions.
- Measuring keyword and semantic alignment.
- Generating actionable improvement suggestions.

---

## Dataset
This project does not rely on an external dataset. Instead, it uses:

- An uploaded PDF resume.
- A pasted or uploaded job description.

The app examines the text content of both inputs and computes similarity and skill overlap.

---

## Tools and Technologies
- Python
- Streamlit
- pdfplumber
- pandas
- scikit-learn
- google-generativeai (Google Gemini API)
- python-dotenv

---

## Methods
- **PDF parsing:** `resume_parser.py` extracts text from PDF resumes using `pdfplumber`.
- **Skill matching:** `ats_score.py` compares resume and job description text against a predefined common skill list.
- **Semantic scoring:** TF-IDF vectorization and cosine similarity measure how similar the resume and job description are in overall language and context.
- **AI feedback:** `gemini_feedback.py` sends a structured prompt to Google Gemini to generate suggested missing skills, action verb recommendations, and rewrite suggestions.

---

## Key Insights
- Keyword overlap alone is not enough; semantic similarity improves relevance scoring.
- AI-generated resume feedback can point out weak bullet points and suggest stronger action verbs.
- Resumes that mention job-specific skills and domain terminology score higher with this tool.

---

## Dashboard / Model / Output
The Streamlit app provides:

- Resume upload input (PDF)
- Job description input (paste text or upload `.txt/.pdf`)
- ATS match score
- Matched, missing, and extra skills
- Cosine similarity percentage
- Gemini-generated resume feedback and improvement suggestions

---

## How to Run this Project
1. Clone the repository or copy the project files.
2. Create and activate a Python virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your Gemini API key to a `.env` file:
   ```text
   GEMINI_API_KEY=your_actual_api_key_here
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```
6. Open the provided local URL in your browser.

---

## Results & Conclusion
This project gives job applicants a straightforward way to evaluate resume fit for a role. It combines:

- exact skill and keyword matching,
- semantic similarity scoring,
- and AI-driven feedback.

The result is a practical tool for improving resume relevance and tailoring content to specific job descriptions.

---

## Future Work
Potential improvements include:

- adding OCR support for scanned resume PDFs,
- expanding the skill extraction list,
- supporting multiple resume and job description formats,
- integrating resume section parsing,
- storing historical analyses for tracking progress over time.
