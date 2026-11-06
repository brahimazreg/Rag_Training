riting


RAG Training Project — Progress Report
Last updated: November 4, 2026

1. Project Overview
I am building a Retrieval-Augmented Generation (RAG) application using:

Python
LangChain
Google Gemini LLM
Google Gemini Embeddings
ChromaDB
Project objective
Build an application that answers questions using information retrieved exclusively from two PDF documents.

If the answer is not available in the documents, the application must respond exactly:

"I don't have enough information in the provided documents."

I am learning RAG step by step. I want to understand every component before implementing it.

2. Project Structure

text
Rag_Training/
│
├── data/
│   ├── fabric-admin.pdf
│   └── second-document.pdf
│
├── chroma_db/
│
├── tests/
│   ├── test_embeddings.py
│   ├── test_vector_store.py
│   ├── test_retriever.py
│   ├── test_prompt.py
│   ├── test_llm.py
│   └── test_rag_chain.py
│
├── configure.py
├── documents_loader.py
├── spliter.py
├── embedding.py
├── llm.py
├── vector_store.py
├── retriever.py
├── rag_chain.py
├── progress.md
├── .env
└── .venv/
3. Completed Implementation
Stage 1 — PDF Loading
File: documents_loader.py

Used DirectoryLoader and PyPDFLoader.
Successfully loaded two PDF documents.
Total: 672 pages.
Documents are represented as LangChain Document objects.
Status: COMPLETED

Stage 2 — Text Splitting
File: spliter.py

Implemented RecursiveCharacterTextSplitter.
Converted documents into smaller chunks.
Each chunk contains page_content and metadata.
Status: COMPLETED

Stage 3 — Gemini Configuration
File: configure.py

Configured:

Embedding model name.
LLM model name.
Chunk size and overlap.
Retrieval top_k.
Chroma configuration.
Temperature and maximum output tokens.
Prompt template.
Status: COMPLETED

Stage 4 — Embeddings
File: embedding.py

Implemented GoogleGenerativeAIEmbeddings.

Learned:

Embeddings are numerical representations of text.
embed_documents() converts document text into vectors.
embed_query() converts questions into vectors.
Query and document embeddings must use compatible models and dimensions.
Embeddings are not a vector database.
Encountered HTTP 429 RESOURCE_EXHAUSTED because of Gemini embedding rate limits.

Status: TESTED

Stage 5 — Chroma Vector Database
File: vector_store.py

Installed ChromaDB and LangChain Chroma integration.
Created persistent database.
Implemented document and embedding storage.
Successfully tested vector storage.
Learned:

Chroma is a vector database.
Collections store document chunks, embeddings, IDs and metadata.
Chroma supports similarity searches.
Status: COMPLETED AND TESTED

Stage 6 — Retrieval
File: retriever.py

Implemented:


python
vector_store = Chroma(
    collection_name="rag_documents",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

def question_retriever(question):
    results = retriever.invoke(question)
    return results

def get_context(question):
    results = question_retriever(question)

    context = "\n\n".join(
        doc.page_content for doc in results
    )

    return context
Learned:

similarity_search() accepts text.
similarity_search_by_vector() accepts an embedding.
as_retriever() creates a LangChain retriever.
invoke(question) performs retrieval.
k=3 returns three nearest chunks.
Retrieved results are Document objects.
doc.page_content contains text.
doc.metadata contains source and page information.
get_context() converts retrieved documents into one context string.
Important bug solved: Chroma expected 3072-dimensional Gemini embeddings but received 384-dimensional MiniLM embeddings. Fixed by configuring the correct embedding_function.

Status: COMPLETED AND TESTED

Stage 7 — Prompt Configuration
File: configure.py

Prompt:


python
PROMPT = """
You are a helpful assistant specialized in answering
questions using the provided PDF documents.

Instructions:
- Answer using ONLY the provided context.
- Do not use outside knowledge.
- Do not invent information.
- If the context does not contain the answer,
  respond exactly:
  "I don't have enough information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
Learned:

ChatPromptTemplate.from_template()
prompt.invoke()
Python string formatting.
Difference between prompt formatting and LLM invocation.
LCEL and the pipe operator.
Status: COMPLETED AND TESTED

Stage 8 — Gemini LLM Initialization
Created a separate file: llm.py

Architectural decision:

configure.py stores configuration values.
llm.py initializes the actual Gemini model instance.
In configure.py:


python
LLM_MODEL_NAME = "gemini-3.8-flash"
In llm.py:


python
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from configure import LLM_MODEL_NAME, MAX_OUTPUT_TOKENS

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

LLM_MODEL = ChatGoogleGenerativeAI(
    model=LLM_MODEL_NAME,
    google_api_key=gemini_api_key,
    max_output_tokens=MAX_OUTPUT_TOKENS
)
Important:

LLM_MODEL_NAME is a string.
LLM_MODEL is an initialized model instance.
rag_chain.py must import LLM_MODEL from llm.py, not configure.py.
Encountered:

HTTP 503 temporary service unavailability.
HTTP 404 model availability error when testing gemini-2.5-flash.
Changed to gemini-3.8-flash based on the API error recommendation.
Status: WORKING

4. Stage 9 — Complete RAG Chain
File: rag_chain.py

Current implementation:


python
from configure import PROMPT
from llm import LLM_MODEL

from retriever import get_context

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel
)


# Step 1: Create prompt template
prompt = ChatPromptTemplate.from_template(PROMPT)


# Step 2: Wrap context function
context_retriever = RunnableLambda(get_context)


# Step 3: Create parallel mapping
mapping = RunnableParallel({
    "context": context_retriever,
    "question": RunnablePassthrough()
})


# Step 4: Connect the complete RAG pipeline
rag_chain = mapping | prompt | LLM_MODEL


# Step 5: Execute the RAG pipeline
def ask_question(question: str):

    response = rag_chain.invoke(question)

    if isinstance(response.content, str):
        return response.content

    return "".join(
        block["text"]
        for block in response.content
        if isinstance(block, dict)
        and block.get("type") == "text"
    )
Learned:

RunnableLambda converts a Python function into a Runnable.
RunnablePassthrough passes the original question through.
RunnableParallel executes multiple Runnable branches.
A normal Python dictionary does not have invoke().
RunnableParallel produces a Runnable dictionary.
The pipe operator connects components.
One invoke() executes the complete pipeline.
Status: IMPLEMENTED AND SUCCESSFULLY EXECUTED

5. Complete RAG Pipeline — First Successful Test
File: tests/test_rag_chain.py


python
from rag_chain import ask_question

question = "Who can purchase licenses?"

answer = ask_question(question)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)
Executed successfully:


powershell
python -m tests.test_rag_chain
Actual answer received:


text
To purchase licenses, you must be a Billing administrator.
This confirms that:

The retriever successfully retrieves document chunks.
Context is generated.
The prompt is formatted.
Gemini receives the prompt.
Gemini generates an answer.
The complete LCEL pipeline executes.
Important output-format issue:

Gemini returned response.content as a list of structured text blocks instead of a plain string.

Fixed by extracting text blocks inside ask_question().

Status: FIRST COMPLETE RAG PIPELINE WORKING

6. Current Progress

Component	Status
PDF loading	Completed
Text splitting	Completed
Gemini embeddings	Tested
Chroma storage	Tested
Similarity search	Tested
LangChain retriever	Working
Context conversion	Completed
Prompt template	Tested
Gemini LLM initialization	Working
LCEL mapping	Working
Complete RAG chain	Working
Answer extraction	Working
Exact fallback validation	Not implemented
Retrieval relevance checking	Not implemented
Source document references	Not implemented
Streamlit interface	Not implemented
7. Next Session — Where to Continue
IMPORTANT: Do not repeat the completed lessons.

Start from the fact that the complete RAG pipeline has already generated its first successful answer.

Lesson 1 — Test questions with answers in PDFs
Test:


python
question = "Who can purchase licenses?"
Verify that the answer is based on the PDF content.

Lesson 2 — Test questions without answers in PDFs
Test:


python
question = "What is the population of Japan?"
Expected exact answer:


text
I don't have enough information in the provided documents.