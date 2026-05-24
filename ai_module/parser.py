import os
from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts all text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

def extract_text_from_docx(file_path: str) -> str:
    """Extracts all text from a DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = [paragraph.text for paragraph in doc.paragraphs if paragraph.text]
        return "\n".join(text).strip()
    except Exception as e:
        return f"Error reading DOCX file: {str(e)}"

def parse_cv(file_path: str) -> str:
    """
    Main function. Takes a file path, detects the extension,
    and returns the raw text.
    """
    if not os.path.exists(file_path):
        return "Error: File could not be found."

    _, extension = os.path.splitext(file_path.lower())

    if extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif extension in ['.docx', '.doc']:
        return extract_text_from_docx(file_path)
    else:
        return f"Error: Unsupported extension {extension}. Please use PDF or DOCX."