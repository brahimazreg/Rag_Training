from configure import EMBEDDING_MODEL_NAME
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing")

embedding_model = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL_NAME,
    google_api_key=gemini_api_key
)


def embed_documents(chunks):
    vectors = embedding_model.embed_documents(
        [chunk.page_content for chunk in chunks]
    )
    return vectors