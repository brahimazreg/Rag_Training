from embedding import embedding_model
from langchain_chroma import Chroma

from configure import COLLECTION_NAME
# Relevance threshold
RELEVANCE_THRESHOLD = 0.40


# Connect to existing Chroma database
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embedding_model,
    persist_directory="./chroma_db"
)


# Create LangChain retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


def question_retriever(question):

    results = retriever.invoke(question)

    return results


def get_relevant_documents(question):

    results = vector_store.similarity_search_with_relevance_scores(
        question,
        k=3
    )

    relevant_documents = []

    for doc, score in results:

        print(f"Relevance score: {score:.3f}")

        if score >= RELEVANCE_THRESHOLD:

            relevant_documents.append(doc)

    return relevant_documents


def get_context(question):

    results = get_relevant_documents(question)

    context = "\n\n".join(
        doc.page_content for doc in results
    )

    return context