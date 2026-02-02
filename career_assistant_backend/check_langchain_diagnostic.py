import importlib
import sys

def try_import(p, n):
    try:
        mod = importlib.import_module(p)
        item = getattr(mod, n)
        print(f"SUCCESS: {n} found in {p}")
    except Exception as e:
        print(f"FAILED: {n} in {p} -> {e}")

print("Testing retrievers...")
try_import('langchain_community.retrievers', 'ContextualCompressionRetriever')
try_import('langchain.retrievers', 'ContextualCompressionRetriever')

print("\nTesting document_compressors...")
try_import('langchain_community.retrievers.document_compressors', 'LLMChainExtractor')
try_import('langchain_community.document_compressors', 'LLMChainExtractor')

print("\nTesting chains...")
try_import('langchain_community.chains', 'ConversationalRetrievalChain')
try_import('langchain.chains', 'ConversationalRetrievalChain')

print("\nTesting memory...")
try_import('langchain_community.memory', 'ConversationSummaryMemory')
try_import('langchain.memory', 'ConversationSummaryMemory')
