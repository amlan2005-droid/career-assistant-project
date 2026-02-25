import pytesseract
from pdf2image import convert_from_bytes
import pdfplumber
import io
from docx import Document

# Path to tesseract exe on Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_resume(file_bytes: bytes, filename: str):
    """
    Extract text from resume (PDF or DOCX).
    For PDFs: First tries direct text extraction, falls back to OCR if needed.
    Returns: (extracted_text, is_scanned_flag)
    """
    text = ""
    is_scanned = False
    
    # Handle TXT (for debugging)
    if filename.lower().endswith(".txt"):
         text = file_bytes.decode("utf-8", errors="ignore")
    # Handle PDF
    elif filename.lower().endswith(".pdf"):
        # STEP 1: Try direct text extraction using pdfplumber
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            print(f"[DEBUG] Direct extraction got {len(text.strip())} characters")
            
            # If we got enough text, we're done!
            if len(text.strip()) >= 50:
                print("[DEBUG] Successfully extracted text directly from PDF")
                return text, False
            
            # Otherwise, fall back to OCR
            print("[DEBUG] Direct extraction insufficient, trying OCR...")
            
        except Exception as e:
            print(f"[DEBUG] Direct extraction failed: {e}, trying OCR...")
        
        # STEP 2: Fallback to OCR for scanned PDFs
        try:
            text = ""  # Reset text
            poppler_path = r"C:\poppler-25.12.0\Library\bin"
            print(f"[DEBUG] Converting PDF to images using Poppler at: {poppler_path}")
            
            # Verify Poppler exists
            import os
            if not os.path.exists(poppler_path):
                print(f"[ERROR] Poppler path does not exist: {poppler_path}")
                raise FileNotFoundError(f"Poppler not found at {poppler_path}")

            images = convert_from_bytes(file_bytes, poppler_path=poppler_path)
            print(f"[DEBUG] Successfully converted PDF to {len(images)} image(s)")
            
            for i, image in enumerate(images):
                print(f"[DEBUG] Running OCR on page {i+1}...")
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n"
                print(f"[DEBUG] OCR on page {i+1} got {len(page_text.strip())} characters")
            
            is_scanned = True
            print(f"[DEBUG] OCR extraction got {len(text.strip())} total characters")
            
        except Exception as e:
            import traceback
            print(f"[ERROR] OCR extraction failed: {e}")
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            is_scanned = True
            # If both failed, we might want to propagate the error if text is still empty
            if not text.strip():
                print("[WARN] Both direct and OCR extraction failed or yielded no text.")

    # Handle DOCX
    elif filename.lower().endswith(".docx"):
        try:
            doc = Document(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                text += para.text + "\n"
            print(f"[DEBUG] DOCX extraction got {len(text.strip())} characters")
        except Exception as e:
            print(f"[DEBUG] DOCX extraction failed: {e}")

    return text, is_scanned
