from langchain_chroma import Chroma
from embedding import embedding_model

def create_vector_store(chunks, vectors):

    vector_store = Chroma(
        collection_name="rag_documents",
        embedding_function=embedding_model,
        persist_directory="./chroma_db"
    )

    # Store chunks and their precomputed embeddings
    vector_store._collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=[chunk.page_content for chunk in chunks],
        embeddings=vectors,
        metadatas=[chunk.metadata for chunk in chunks]
    )

    return vector_store