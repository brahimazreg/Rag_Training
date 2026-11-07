# PDF Question Answering — RAG Application

## 1. Project Overview

This project is a Retrieval-Augmented Generation (RAG) application built with Python, LangChain, Google Gemini Embeddings, Groq, ChromaDB, Streamlit, and FastAPI.

The objective is to build an application that answers questions using information retrieved exclusively from the provided PDF documents.

The application follows a document-based question-answering approach. It retrieves relevant information from PDF documents and uses an LLM to generate answers based on the retrieved context.

If the answer is not available in the provided documents, the application must respond exactly:

```text
I don't have enough information in the provided documents.
```

The project includes:

- A RAG pipeline for document retrieval and answer generation.
- A ChromaDB vector database for storing document embeddings.
- A Streamlit frontend for user interaction.
- A FastAPI backend exposing the RAG functionality through REST API endpoints.
- Source document references, including PDF filenames and page numbers.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| LangChain | Framework for building the RAG pipeline |
| Google Gemini Embeddings | Converts text into numerical vector representations |
| Groq | LLM provider used to generate answers |
| ChromaDB | Vector database used to store and retrieve document embeddings |
| PyPDF | PDF document loading |
| RecursiveCharacterTextSplitter | Splits documents into smaller chunks |
| Streamlit | Interactive frontend application |
| FastAPI | Backend REST API framework |
| Uvicorn | ASGI server used to run FastAPI |
| Pydantic | Request validation and data models |
| Requests | HTTP communication between Streamlit and FastAPI |

## 3. Project Architecture

The application follows a Retrieval-Augmented Generation workflow.

### RAG Pipeline

1. Load PDF documents.
2. Split documents into smaller text chunks.
3. Generate embeddings using Google Gemini.
4. Store document chunks and embeddings in ChromaDB.
5. Retrieve relevant chunks based on the user's question.
6. Build a prompt using the retrieved context.
7. Send the prompt to Groq.
8. Generate an answer based exclusively on the provided context.
9. Extract source document references, including filenames and page numbers.

### Application Architecture

The project follows a frontend/backend architecture.

**Frontend — Streamlit**

- Provides the user interface.
- Allows users to enter questions.
- Sends HTTP POST requests to the FastAPI backend.
- Displays generated answers and PDF source references.
- Maintains conversation history during the session.

**Backend — FastAPI**

- Exposes REST API endpoints.
- Receives and validates user questions.
- Calls the existing RAG pipeline.
- Returns answers and source references in JSON format.

**RAG Pipeline**

- Retrieves relevant documents.
- Generates answers using Groq.
- Extracts PDF source references.

### Application Workflow

```text
                 USER
                   |
                   v
          STREAMLIT FRONTEND
               app.py
                   |
                   v
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
                USER
```

## 4. Project Structure

```text
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
```

**Note:** `.venv/`, `.env`, and `chroma_db/` are local resources and should not be committed to GitHub. PDF documents should only be committed when permitted by their licensing and distribution rights.

## 5. Installation

### Step 1 — Clone the repository

```bash
git clone YOUR_REPOSITORY_URL

cd Rag_Training
```

### Step 2 — Create a virtual environment

```bash
python -m venv .venv
```

### Step 3 — Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Configure environment variables

Create a `.env` file in the project root directory.

Add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```


## 6. Running the Application Locally

The application consists of two independent components: FastAPI (backend) and Streamlit (frontend).

Both applications must be running simultaneously.

### Step 1 — Start the FastAPI backend

Open the first terminal in VS Code.

Make sure the virtual environment is activated and execute:

```bash
uvicorn main:app --reload
```

FastAPI will be available at:

```text
http://127.0.0.1:8000
```

If your FastAPI entry point is inside an `api/` package, use the corresponding module path:

```bash
uvicorn api.main:app --reload
```

### Step 2 — Access the API documentation

Open:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically generates interactive API documentation using Swagger UI.

### Step 3 — Start the Streamlit frontend

Open a second terminal in VS Code.

Execute:

```bash
streamlit run frontend/app.py
```

Streamlit will be available at:

```text
http://localhost:8501
```

### Step 4 — Ask questions

Open the Streamlit application in your browser.

Enter a question about the provided PDF documents.

The frontend sends the question to the FastAPI backend, which executes the RAG pipeline and returns the generated answer and its sources.

## 7. FastAPI Endpoints

The backend currently exposes the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns a welcome message |
| GET | `/health` | Checks API health |
| POST | `/ask` | Processes a question using the RAG pipeline |

### POST /ask

This endpoint receives a question and returns an answer with its corresponding PDF references.

**Request:**

```json
{
  "question": "What is the main topic of the documents?"
}
```

**Response:**

```json
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
```

The response includes:

- `success`: Indicates whether the request was processed successfully.
- `answer`: Generated answer from the RAG pipeline.
- `sources`: List of PDF documents and corresponding page numbers.

## 8. Testing the RAG Pipeline

To test the complete RAG pipeline independently:

```bash
python -m tests.test_rag_chain
```

### Example question

```text
Who can purchase licenses?
```

### Example answer

```text
Billing administrators can purchase licenses.
```

### Example question without an answer in the PDFs

```text
What is the population of Japan?
```

**Expected response:**

```text
I don't have enough information in the provided documents.
```

## 9. Deployment on Render

The application is deployed on Render using two independent web services:

1. FastAPI — Backend service.
2. Streamlit — Frontend service.

Both services communicate through HTTP requests.

### 9.1 FastAPI Backend Deployment

The FastAPI backend is deployed at:

**Backend URL:**

https://rag-training-1.onrender.com

**API documentation:**

https://rag-training-1.onrender.com/docs

**Question-answering endpoint:**

https://rag-training-1.onrender.com/ask


#### Backend environment variables

Configure the following environment variables in Render:

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Google Gemini API key |
| `GROQ_API_KEY` | Groq API key |

These variables are configured through the Render dashboard and must not be committed to GitHub.


**Important:** Render Persistent Disks require an eligible paid service. Without persistent storage, local database files may be lost when the service restarts or is redeployed. The database should be initialized or restored from the original documents when necessary.



### 9.4 Deployment Verification

After deploying both services, verify that:

**Backend:**

- The FastAPI service is available.
- The `/docs` endpoint opens successfully.
- The `/ask` endpoint accepts questions.
- OpenAI-independent LLM operations work with Gemini and Groq.
- ChromaDB successfully retrieves relevant document chunks.
- Source references are returned correctly.

**Frontend:**

- The Streamlit application opens successfully.
- The frontend connects to the deployed FastAPI backend.
- Questions are submitted successfully.
- Generated answers are displayed.
- PDF filenames and page references are displayed.
- Conversation history is maintained during the session.

### 9.5 Production URLs

**FastAPI backend:**

https://rag-training-1.onrender.com

**FastAPI Swagger documentation:**

https://rag-training-1.onrender.com/docs

**Streamlit frontend:**


Author : AZREG BRAHIM


