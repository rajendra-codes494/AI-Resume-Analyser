import os
# Import our PDF extractor from resume_parser
from resume_parser import extract_text_from_pdf

def extract_text_from_file(uploaded_file):
    """
    Helper function to extract text from a Streamlit file upload.
    Supports both PDF and TXT file formats.
    
    Parameters:
    - uploaded_file: Streamlit UploadedFile object.
    
    Returns:
    - A string containing the text of the file, or an error message if unsupported.
    """
    if uploaded_file is None:
        return ""
        
    # Get the file name in lowercase to check its extension
    file_name = uploaded_file.name.lower()
    
    # 1. Handle PDF files
    if file_name.endswith('.pdf'):
        return extract_text_from_pdf(uploaded_file)
        
    # 2. Handle Text (.txt) files
    elif file_name.endswith('.txt'):
        try:
            # Reset file pointer to the beginning to ensure we read from start
            uploaded_file.seek(0)
            # Read bytes and decode them using standard UTF-8 encoding
            text = uploaded_file.read().decode("utf-8")
            # Reset file pointer back to start as a best practice
            uploaded_file.seek(0)
            return text
            
        except UnicodeDecodeError:
            # Sometimes text files are saved with different encoding (e.g. windows-1252 or latin-1)
            # If UTF-8 fails, we try latin-1 as a fallback
            try:
                uploaded_file.seek(0)
                text = uploaded_file.read().decode("latin-1")
                uploaded_file.seek(0)
                return text
            except Exception as e:
                return f"Error decoding text file: {e}"
                
        except Exception as e:
            return f"Error reading text file: {e}"
            
    # 3. Handle unsupported files
    else:
        return "Error: Unsupported file format. Please upload a .pdf or .txt file."
