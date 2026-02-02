import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

print("Attempting to import app.main...")
try:
    from app import main
    print("Success! app.main imported correctly.")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
