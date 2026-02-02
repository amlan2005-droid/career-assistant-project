import os

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF file using PyMuPDF (fitz)."""
    text = ""
    try:
        import fitz
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        # Fallback to simple string extraction if needed, 
        # but for now we just return empty if AI/Library fails
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from a DOCX file using python-docx."""
    text = ""
    try:
        import docx
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error extracting DOCX text: {e}")
    return text

def extract_text(file_path: str) -> str:
    """Detects file type and extracts text."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    return ""
