import langchain
import os
print(f"Langchain file: {langchain.__file__}")
print(f"Langchain dir: {os.path.dirname(langchain.__file__)}")
try:
    import langchain.chains
    print("langchain.chains imported")
    # print(dir(langchain.chains)) 
except ImportError as e:
    print(f"ImportError: {e}")
