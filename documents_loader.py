
from configure import DATA_FILE_PATH
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader



def load_documents(path=DATA_FILE_PATH):

    if not path :
        path=DATA_FILE_PATH

    documents=[]

    pdf_loader= DirectoryLoader(
            path=path,
            glob="**/*.pdf" ,
            loader_cls=PyPDFLoader,
            show_progress=True
            )
        
    documents.extend(pdf_loader.load())
    return documents