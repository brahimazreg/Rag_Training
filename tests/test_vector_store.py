from documents_loader import load_documents
from spliter import split_documents
from embedding import embed_documents
from vector_store import create_vector_store


def main():
    documents=load_documents()
    chunks=split_documents(documents)


    # Temporary test: only 5 chunks
    test_chunks = chunks[:5]

    vectors = embed_documents(test_chunks)
    
    vector_store= create_vector_store(test_chunks,vectors)

    print(" Check  if number of chunks is equal to number of vectors")
    assert len(test_chunks) == len(vectors)
   

     # Step 6: Check stored data
    collection = vector_store._collection

    print("Number of stored vectors:", collection.count())

    print(" Check  if number of chunks is equal to number of collections")
    assert collection.count() == len(test_chunks)

    print("Vector store test passed!")


if __name__=="__main__":
    main()