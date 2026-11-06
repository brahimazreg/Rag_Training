
from configure import PROMPT
from llm import LLM_MODEL
from retriever import get_relevant_documents

from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate


# Step 1: Create prompt template
prompt = ChatPromptTemplate.from_template(PROMPT)


# Step 2: Create a helper to extract Gemini's response
def extract_answer(response):

    if isinstance(response.content, str):
        return response.content

    return "".join(
        block["text"]
        for block in response.content
        if isinstance(block, dict)
        and block.get("type") == "text"
    )


# Step 3: Original function for basic RAG testing
def ask_question(question: str):

    documents = get_relevant_documents(question)

    if not documents:
        return "I don't have enough information in the provided documents."

    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    response = (prompt | LLM_MODEL).invoke({
        "context": context,
        "question": question
    })

    return extract_answer(response)


# Step 4: Generate answer with PDF sources
def ask_question_with_sources(question: str):

    # Retrieve relevant documents ONCE
    documents = get_relevant_documents(question)

    # Check whether relevant documents exist
    if not documents:

        return {
            "answer": "I don't have enough information in the provided documents.",
            "sources": []
        }

    # Build context from retrieved documents
    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    # Generate answer
    response = (prompt | LLM_MODEL).invoke({
        "context": context,
        "question": question
    })

    answer = extract_answer(response)

    # Extract PDF references
    sources = []

    for doc in documents:

        metadata = doc.metadata

        source = metadata.get("source", "Unknown source")

        page = metadata.get("page_label")

        if page is None:
            page = metadata.get("page")

            if page is not None:
                page = int(page) + 1

        reference = {
            "source": Path(source).name,
            "page": str(page) if page is not None else None
        }

        if reference not in sources:
            sources.append(reference)

    return {
        "answer": answer,
        "sources": sources
    }


    
