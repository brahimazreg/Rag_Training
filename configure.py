
# ==============================
# DATA FILE PATH
# ==============================

DATA_FILE_PATH = "data" 

# ==============================
# MODEL CONFIGURATION
# ==============================

EMBEDDING_MODEL_NAME ="gemini-embedding-2"

#LLM_MODEL_NAME= "models/gemini-3.8-flash"  
GROQ_MODEL_NAME = "openai/gpt-oss-120b"

# ==============================
# DOCUMENT CONFIGURATION
# ==============================

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

# ==============================
# RETRIEVAL CONFIGURATION
# ==============================

TOP_K = 3

# ==============================
# VECTOR DATABASE
# ==============================

VECTOR_DB = "chroma"

CHROMA_DIRECTORY = "./chroma_db"

COLLECTION_NAME = "my_documents"

# ==============================
# GENERATION CONFIGURATION
# ==============================

TEMPERATURE = 0.2

MAX_OUTPUT_TOKENS = 2048

# Create our prompt template
PROMPT= """
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