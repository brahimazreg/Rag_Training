PDF Question Answering — RAG Application
1. Project Overview

This project is a Retrieval-Augmented Generation (RAG) application built with Python, LangChain, Google Gemini Embeddings, Groq, and ChromaDB.

The objective is to build an application that answers questions using information retrieved exclusively from two PDF documents.

If the answer is not available in the provided documents, the application must respond exactly:

I don't have enough information in the provided documents.
2. Technologies Used
Python: Main programming language.
LangChain: Framework for building the RAG pipeline.
Google Gemini Embeddings: Converts text into numerical vector representations.
Groq: LLM provider used to generate answers.
ChromaDB: Vector database used to store and retrieve document embeddings.
PyPDF: PDF document loading.
RecursiveCharacterTextSplitter: Splits documents into smaller chunks.
3. Project Architecture

The application follows this workflow:

Load PDF documents.
Split documents into smaller text chunks.
Generate embeddings using Google Gemini.
Store document chunks and embeddings in ChromaDB.
Retrieve relevant chunks based on the user's question.
Build a prompt using the retrieved context.
Send the prompt to Groq.
Generate an answer based exclusively on the provided context.
4. Project Structure
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
│
├── requirements.txt
├── progress.md
├── README.md
├── .gitignore
└── .env


Note: .venv/, .env, and chroma_db/ are local resources and should not be committed to GitHub.

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

6. Environment Configuration

Create a .env file in the project root directory.

Add your API keys:

env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key


Never publish your API keys or commit your .env file to GitHub.

7. Running the Application

To test the complete RAG pipeline:

bash
python -m tests.test_rag_chain


Example question:

text
Who can purchase licenses?


Example answer:

text
Billing administrators can purchase licenses.


Example question without an answer in the PDFs:

text
What is the population of Japan?


Expected response:

text
I don't have enough information in the provided documents.

8. Implementation Progress
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
Retrieval relevance checking	Pending
Source document references	Pending
Streamlit interface	Pending
FastAPI integration	Pending
9. Learning Objectives

This project is being developed step by step to understand the fundamental components of Retrieval-Augmented Generation.

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
10. Future Improvements
Implement retrieval relevance checking.
Improve fallback validation.
Display source documents and page references.
Build an interactive Streamlit interface.
Create a REST API using FastAPI.
Add more PDF documents.
Improve error handling and application reliability.
11. Project Status

The first complete RAG pipeline has been successfully implemented and tested.

The application can retrieve information from PDF documents and generate answers using Groq, with Gemini handling document and question embeddings.

This project is part of a practical learning journey focused on understanding and building RAG applications from the ground up.