from documents_loader import load_documents
from configure import DATA_FILE_PATH

def main():
    response = load_documents(DATA_FILE_PATH)
    if isinstance(response.content, list):
        for block in response.content:
            if block.get("type") == "text":
                print(block["text"])
    else:
        print(response.content)

if __name__=="__main__":
    main()
