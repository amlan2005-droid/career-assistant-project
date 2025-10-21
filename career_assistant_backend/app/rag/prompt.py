from langchain.prompts import PromptTemplate

# Chat prompt template for career assistant
chat_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful career assistant. Use the following context to answer the user's question about careers, jobs, resumes, or professional development.

Context:
{context}

Question: {question}

Answer: Provide a helpful, accurate, and professional response based on the context provided. If the context doesn't contain enough information to answer the question, say so and provide general guidance where possible."""
)
