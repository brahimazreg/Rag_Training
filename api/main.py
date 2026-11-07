
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag_chain import ask_question_with_sources


app = FastAPI(
    title="RAG Training API",
    description="API for asking questions about PDF documents",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask the RAG system"
    )


@app.get("/")
def home():
    return {
        "message": "Welcome to the RAG API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    try:
        result = ask_question_with_sources(
            request.question
        )

        return {
            "success": True,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred: {str(e)}"
        )
