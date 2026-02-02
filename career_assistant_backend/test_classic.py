try:
    from langchain_classic.retrievers import ContextualCompressionRetriever
    print('SUCCESS: ContextualCompressionRetriever found in langchain_classic.retrievers')
except Exception as e:
    print(f'FAILED: ContextualCompressionRetriever in langchain_classic.retrievers: {e}')

try:
    from langchain_classic.retrievers.document_compressors import LLMChainExtractor
    print('SUCCESS: LLMChainExtractor found in langchain_classic.retrievers.document_compressors')
except Exception as e:
    print(f'FAILED: LLMChainExtractor in langchain_classic.retrievers.document_compressors: {e}')

try:
    from langchain_classic.chains import ConversationalRetrievalChain
    print('SUCCESS: ConversationalRetrievalChain found in langchain_classic.chains')
except Exception as e:
    print(f'FAILED: ConversationalRetrievalChain in langchain_classic.chains: {e}')

try:
    from langchain_classic.memory import ConversationSummaryMemory
    print('SUCCESS: ConversationSummaryMemory found in langchain_classic.memory')
except Exception as e:
    print(f'FAILED: ConversationSummaryMemory in langchain_classic.memory: {e}')

try:
    from langchain_core.prompts import PromptTemplate
    print('SUCCESS: PromptTemplate found in langchain_core.prompts')
except Exception as e:
    print(f'FAILED: PromptTemplate in langchain_core.prompts: {e}')

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print('SUCCESS: ChatGoogleGenerativeAI found in langchain_google_genai')
except Exception as e:
    print(f'FAILED: ChatGoogleGenerativeAI in langchain_google_genai: {e}')
