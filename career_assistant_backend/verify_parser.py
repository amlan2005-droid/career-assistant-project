import os
import sys

# Add the project root to sys.path so we can import app
sys.path.append(os.getcwd())

from app.services.resume_parser import parse_resume

def test_parser():
    # Use the existing PDF in the uploads folder
    test_pdf = "uploads/backend-developer2 - Template 18.pdf"
    
    if not os.path.exists(test_pdf):
        print(f"Error: {test_pdf} not found.")
        return

    print(f"Testing parser with: {test_pdf}")
    result = parse_resume(test_pdf)
    
    print("\n" + "="*30)
    print("PARSER TEST RESULTS")
    print("="*30)
    print(f"File: {test_pdf}")
    print(f"Text Extracted: {len(result['text'])} chars")
    print(f"Skills Detected: {', '.join(result['skills']) if result['skills'] else 'None'}")
    print("="*30)
    
    import json
    with open("parser_result.json", "w") as f:
        json.dump(result, f, indent=4)
    print("Result saved to parser_result.json")

if __name__ == "__main__":
    test_parser()
