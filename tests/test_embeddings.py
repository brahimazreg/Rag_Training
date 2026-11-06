from spliter import split_documents
from documents_loader import load_documents
from embedding import embed_documents
from configure import DATA_FILE_PATH



def main():

    documents= load_documents(DATA_FILE_PATH)
    print(f"Nomber of documents :{len(documents)}")
    chunks  = split_documents(documents)
    print(f"Nomber of chunks :{len(chunks)}")
    vectors=embed_documents(chunks)

    print(f"Nomber of vectors: {len(vectors)}")
    print(vectors[0])

if __name__=="__main__":
    main()
