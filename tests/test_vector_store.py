
from documents_loader import load_documents
from spliter import split_documents
from embedding import embed_documents
from vector_store import create_vector_store


def main():

    documents = load_documents()
    chunks = split_documents(documents)

    print("Total documents:", len(documents))
    print("Total chunks:", len(chunks))

    # Choose testing mode
    test_all = False

    if test_all:
        test_chunks = chunks
        print("Testing with ALL chunks")
    else:
        test_chunks = chunks[:5]
        print("Testing with first 5 chunks")

    # Generate embeddings
    vectors = embed_documents(test_chunks)

    assert len(test_chunks) == len(vectors)

    # Store in ChromaDB
    vector_store = create_vector_store(test_chunks, vectors)

    collection = vector_store._collection

    print("Number of stored vectors:", collection.count())

    assert collection.count() >= len(test_chunks)

    print("Vector store test passed!")


if __name__ == "__main__":
    main()
