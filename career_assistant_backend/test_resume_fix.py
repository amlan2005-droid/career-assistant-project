from app.utils.resume_text_extractor import extract_text_from_resume

def test_extraction():
    # Mock some basic bytes
    mock_bytes = b"This is a test resume content."
    filename = "test_resume.pdf"
    
    print(f"Testing extraction for {filename}...")
    try:
        text, is_scanned = extract_text_from_resume(mock_bytes, filename)
        print("Success: Extraction executed without crashing.")
        print(f"Extracted text length: {len(text)}")
        print(f"Is scanned: {is_scanned}")
    except UnboundLocalError as e:
        print(f"FAILED: UnboundLocalError detected! {e}")
    except Exception as e:
        print(f"Other error (expected for dummy bytes): {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_extraction()
