import pdfplumber
import pypdfium2 as pdfium
import sys
import os

def test_extraction(file_path):
    print(f"File: {file_path}")
    
    # 1. pdfplumber
    try:
        print("\n--- pdfplumber ---")
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    words = page.extract_words()
                    if words:
                        text += " ".join(w['text'] for w in words) + "\n"
            print(f"Length: {len(text.strip())}")
            print(f"Snippet: {text.strip()[:100]}")
    except Exception as e:
        print(f"pdfplumber Error: {e}")

    # 2. pypdfium2
    try:
        print("\n--- pypdfium2 ---")
        pdf = pdfium.PdfDocument(file_path)
        text = ""
        for page in pdf:
            textpage = page.get_textpage()
            text += textpage.get_text_range()
            text += "\n"
            textpage.close()
            page.close()
        pdf.close()
        print(f"Length: {len(text.strip())}")
        print(f"Snippet: {text.strip()[:100]}")
    except Exception as e:
        print(f"pypdfium2 Error: {e}")

if __name__ == "__main__":
    target = r"c:\Users\DELL\career_assistant_project\career_assistant_backend\uploads\resume aiml engineer.pdf"
    if os.path.exists(target):
        test_extraction(target)
    else:
        print(f"File not found: {target}")
