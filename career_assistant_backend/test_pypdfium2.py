import pypdfium2 as pdfium
import sys

def test_pypdfium2(file_path):
    try:
        pdf = pdfium.PdfDocument(file_path)
        text = ""
        for page in pdf:
            textpage = page.get_textpage()
            text += textpage.get_text_range()
            text += "\n"
        print(f"Extracted length: {len(text)}")
        print(f"Snippet: {text[:100]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # We don't have a real PDF here but we can at least check if the imports and basic calls work
    print("Testing pypdfium2 import and basic API...")
    try:
        import pypdfium2
        print(f"Version: {pypdfium2.V_PYPDFIUM2}")
    except Exception as e:
        print(f"Import error: {e}")
