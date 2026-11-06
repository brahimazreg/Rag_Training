from embedding import embedding_model
from langchain_chroma import Chroma


# Connect to our existing Chroma database
vector_store = Chroma(
    collection_name="rag_documents",
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)


# Create a LangChain retriever
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