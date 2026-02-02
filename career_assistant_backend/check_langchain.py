try:
    import langchain
    print(f"Langchain version: {langchain.__version__}")
    from langchain.chains import RetrievalQA
    print("Success: RetrievalQA imported")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
