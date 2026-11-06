from spliter import split_documents
from documents_loader import load_documents
from configure import DATA_FILE_PATH



def main():

    documents= load_documents(DATA_FILE_PATH)
    chunks  = split_documents(documents)
    print(len(chunks))
    print(chunks[0])

if __name__=="__main__":
    main()
