
import sys
import os

print(f"Current Python Executable: {sys.executable}")
print(f"Current Environment Path: {sys.prefix}")
try:
    import google.generativeai
    print("google.generativeai is importable here.")
    print(f"Package location: {os.path.dirname(google.generativeai.__file__)}")
except ImportError:
    print("google.generativeai is NOT importable here.")
