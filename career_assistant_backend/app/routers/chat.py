from fastapi import APIRouter
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from ..rag.vectorstore import get_vectorstore
from ..rag.prompt import chat_prompt

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/")
async def chat_endpoint(req: QueryRequest):
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": chat_prompt}
    )

    response = qa_chain.run(req.question)
    return {"answer": response}
