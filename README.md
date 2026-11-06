PDF Question Answering — RAG Application
1. Project Overview

This project is a Retrieval-Augmented Generation (RAG) application built with Python, LangChain, Google Gemini Embeddings, Groq, ChromaDB, Streamlit, and FastAPI.

The objective is to build an application that answers questions using information retrieved exclusively from the provided PDF documents.

The application follows a document-based question-answering approach. It retrieves relevant information from PDF documents and uses an LLM to generate answers based on the retrieved context.

If the answer is not available in the provided documents, the application must respond exactly:

text
I don't have enough information in the provided documents.


The project includes:

A RAG pipeline for document retrieval and answer generation.
A ChromaDB vector database for storing document embeddings.
A Streamlit frontend for user interaction.
A FastAPI backend exposing the RAG functionality through REST API endpoints.
Source document references, including PDF filenames and page numbers.
2. Technologies Used
Technology	Purpose
Python	Main programming language
LangChain	Framework for building the RAG pipeline
Google Gemini Embeddings	Converts text into numerical vector representations
Groq	LLM provider used to generate answers
ChromaDB	Vector database used to store and retrieve document embeddings
PyPDF	PDF document loading
RecursiveCharacterTextSplitter	Splits documents into smaller chunks
Streamlit	Interactive frontend application
FastAPI	Backend REST API framework
Uvicorn	ASGI server used to run FastAPI
Pydantic	Request validation and data models
Requests	HTTP communication between Streamlit and FastAPI
3. Project Architecture

The application follows a Retrieval-Augmented Generation workflow.

RAG Pipeline
Load PDF documents.
Split documents into smaller text chunks.
Generate embeddings using Google Gemini.
Store document chunks and embeddings in ChromaDB.
Retrieve relevant chunks based on the user's question.
Build a prompt using the retrieved context.
Send the prompt to Groq.
Generate an answer based exclusively on the provided context.
Extract source document references, including filenames and page numbers.
Return the generated answer and sources.
Application Architecture

The project follows a frontend/backend architecture.

Frontend — Streamlit

Provides the user interface.
Allows users to enter questions.
Sends HTTP POST requests to the FastAPI backend.
Displays generated answers and PDF source references.

Backend — FastAPI

Exposes REST API endpoints.
Receives and validates user questions.
Calls the existing RAG pipeline.
Returns answers and source references in JSON format.

RAG Pipeline

Retrieves relevant documents.
Generates answers using Groq.
Extracts PDF source references.
Application Workflow
text
                 USER
                   |
                   v
          STREAMLIT FRONTEND
              app.py
                   |
                   |
             HTTP POST
             /ask
                   |
                   v
           FASTAPI BACKEND
              main.py
                   |
                   v
              RAG CHAIN
             rag_chain.py
                   |
                   v
              RETRIEVER
             retriever.py
                   |
                   v
              CHROMADB
                   |
             Relevant chunks
                   |
                   v
              GROQ LLM
                   |
             Generated answer
                   |
                   v
          SOURCE EXTRACTION
                   |
                   v
             JSON RESPONSE
                   |
                   v
          STREAMLIT FRONTEND
                   |
                   v
             USER RESPONSE

4. Project Structure
text
Rag_Training/
│
├── frontend/
│   └── app.py
│
├── tests/
│   ├── __init__.py
│   ├── test_documents_loader.py
│   ├── test_embeddings.py
│   ├── test_prompt.py
│   ├── test_rag_chain.py
│   ├── test_retriever.py
│   ├── test_splitter.py
│   └── test_vector_store.py
│
├── data/
│   ├── fabric-admin.pdf
│   └── second-document.pdf
│
├── chroma_db/
│
├── configure.py
├── documents_loader.py
├── embedding.py
├── llm.py
├── main.py
├── rag_chain.py
├── retriever.py
├── splitter.py
├── vector_store.py
│
├── requirements.txt
├── progress.md
├── README.md
├── .gitignore
└── .env


Note: .venv/, .env, and chroma_db/ are local resources and should not be committed to GitHub. PDF documents should only be committed when permitted by their licensing and distribution rights.

5. Installation
Step 1 — Clone the repository
bash
git clone YOUR_REPOSITORY_URL

cd Rag_Training

Step 2 — Create a virtual environment
bash
python -m venv .venv

Step 3 — Activate the virtual environment

Windows PowerShell:

powershell
.venv\Scripts\activate

Step 4 — Install dependencies
bash
pip install -r requirements.txt

Step 5 — Configure environment variables

Create a .env file in the project root directory.

Add your API keys:

env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key


Never publish your API keys or commit your .env file to GitHub.

6. Running the Application

The application consists of two independent components: FastAPI (backend) and Streamlit (frontend).

Both applications must be running simultaneously.

Step 1 — Start the FastAPI backend

Open the first terminal in VS Code.

Make sure the virtual environment is activated and execute:

bash
uvicorn main:app --reload


FastAPI will be available at:

text
http://127.0.0.1:8000

Step 2 — Access the API documentation

FastAPI automatically generates interactive API documentation using Swagger UI.

Open:

text
http://127.0.0.1:8000/docs


The documentation allows users to test API endpoints directly from their browser.

Step 3 — Start the Streamlit frontend

Open a second terminal in VS Code.

Execute:

bash
streamlit run frontend/app.py


Streamlit will be available at:

text
http://localhost:8501

Step 4 — Ask questions

Open the Streamlit application in your browser.

Enter a question about the provided PDF documents.

The frontend sends the question to the FastAPI backend, which executes the RAG pipeline and returns the generated answer and its sources.

7. FastAPI Endpoints

The backend currently exposes the following endpoints:

Method	Endpoint	Description
GET	/	Returns a welcome message
GET	/health	Checks API health
POST	/ask	Processes a question using the RAG pipeline
POST /ask

This endpoint receives a question and returns an answer with its corresponding PDF references.

Request:

json
{
  "question": "What is the main topic of the documents?"
}


Response:

json
{
  "success": true,
  "answer": "The documents primarily cover Microsoft Fabric administration, including admin roles, governance, security, settings, and tools for managing and monitoring the Fabric platform.",
  "sources": [
    {
      "source": "fabric-admin.pdf",
      "page": "3"
    },
    {
      "source": "fabric-admin.pdf",
      "page": "2"
    },
    {
      "source": "fabric-admin.pdf",
      "page": "1"
    }
  ]
}


The response includes:

success: Indicates whether the request was processed successfully.
answer: Generated answer from the RAG pipeline.
sources: List of PDF documents and corresponding page numbers used as references.
8. Testing the RAG Pipeline

To test the complete RAG pipeline independently:

bash
python -m tests.test_rag_chain

Example question
text
Who can purchase licenses?

Example answer
text
Billing administrators can purchase licenses.

Example question without an answer in the PDFs
text
What is the population of Japan?

Expected response
text
I don't have enough information in the provided documents.

9. Implementation Progress
Component	Status
PDF loading	Completed
Text splitting	Completed
Gemini embeddings	Completed
ChromaDB storage	Completed
Similarity search	Completed
LangChain retriever	Completed
Context generation	Completed
Prompt configuration	Completed
Groq LLM integration	Completed
Complete RAG chain	Completed
Answer extraction	Completed
Initial fallback testing	Completed
Source document references	Completed
Streamlit interface	Completed
FastAPI backend	Completed
Streamlit–FastAPI integration	Completed
API endpoint testing	Completed
Retrieval relevance checking	Pending
PDF upload through API	Pending
Conversation history	Pending
Production deployment	Pending
10. Learning Objectives

This project is being developed step by step to understand the fundamental components of Retrieval-Augmented Generation and API-based application development.

The main learning objectives are:

Understand document loading and preprocessing.
Understand text chunking and metadata.
Understand embeddings and vector representations.
Understand vector databases and similarity search.
Understand retrieval and context generation.
Understand prompt engineering.
Understand LangChain Expression Language (LCEL).
Understand LLM integration.
Build a complete RAG application.
Understand REST API development using FastAPI.
Understand communication between frontend and backend.
Understand HTTP requests and JSON responses.
Integrate Streamlit with FastAPI.
11. Future Improvements

Potential improvements include:

Implement retrieval relevance checking.
Improve fallback validation.
Add PDF upload functionality through FastAPI.
Support additional PDF documents.
Implement conversation history and multi-turn question answering.
Improve error handling and application reliability.
Improve the frontend user experience.
Add API authentication.
Deploy the application to a production environment.
12. Project Status

The first complete RAG application has been successfully implemented and tested.

The application can:

Load and process PDF documents.
Generate embeddings using Google Gemini.
Store and retrieve document embeddings using ChromaDB.
Retrieve relevant information based on user questions.
Generate context-based answers using Groq.
Return source document references, including PDF filenames and page numbers.
Expose the RAG pipeline through a FastAPI REST API.
Provide an interactive Streamlit frontend.
Connect the frontend and backend through HTTP requests.

The project currently demonstrates a complete end-to-end RAG application with a separated frontend and backend architecture.

This project is part of a practical learning journey focused on understanding and building RAG applications from the ground up, from document processing and retrieval to API development and frontend integration.