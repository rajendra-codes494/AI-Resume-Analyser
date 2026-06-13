import pdfplumber

def extract_text_from_pdf(pdf_file):
    """
    Extracts all text from a PDF file.
    
    Parameters:
    - pdf_file: This can be a string representing the file path, or a file-like object 
                (which is what Streamlit's file uploader returns).
                
    Returns:
    - A single string containing all the text extracted from the PDF.
    """
    extracted_text = ""
    
    try:
        # Open the PDF file using pdfplumber
        with pdfplumber.open(pdf_file) as pdf:
            # Loop through every page in the PDF document
            for page_num, page in enumerate(pdf.pages, start=1):
                # Extract text from the individual page
                page_text = page.extract_text()
                
                # If page contains text, append it to our main text accumulator
                if page_text:
                    extracted_text += page_text + "\n"
                else:
                    print(f"Warning: Page {page_num} did not contain readable text.")
                    
    except Exception as e:
        # If something goes wrong (e.g. file is corrupt), print the error and return empty text
        print(f"Error parsing PDF: {e}")
        return ""
        
    # Return the clean, stripped text (removes leading/trailing extra spaces)
    return extracted_text.strip()
