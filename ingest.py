
import argparse
import hashlib
import shutil
import time
from pathlib import Path

from langchain_chroma import Chroma

from configure import (
    DATA_FILE_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    CHROMA_DIRECTORY,
    COLLECTION_NAME
)

from documents_loader import load_documents
from embedding import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter


BATCH_SIZE = 25
MAX_RETRIES = 5


def generate_id(chunk):

    content = (
        str(chunk.metadata.get("source", "")) +
        str(chunk.metadata.get("page", "")) +
        chunk.page_content
    )

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def ingest_documents(rebuild=False):

    db_path = Path(CHROMA_DIRECTORY)

    if rebuild and db_path.exists():
        print("Removing existing ChromaDB...")
        shutil.rmtree(db_path)

    db_path.mkdir(parents=True, exist_ok=True)

    # Step 1: Load PDFs
    print("Loading PDF documents...")

    documents = load_documents(DATA_FILE_PATH)

    if not documents:
        raise ValueError("No PDF documents found.")

    print(f"Loaded {len(documents)} PDF pages.")

    # Step 2: Split documents
    print("Splitting documents...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # Step 3: Connect to ChromaDB
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_model,
        persist_directory=str(db_path)
    )

    # Step 4: Process batches
    total = len(chunks)

    for start in range(0, total, BATCH_SIZE):

        batch = chunks[start:start + BATCH_SIZE]

        batch_number = start // BATCH_SIZE + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

        ids = [generate_id(chunk) for chunk in batch]

        print(
            f"\nProcessing batch {batch_number}/{total_batches}"
        )

        for attempt in range(MAX_RETRIES):

            try:

                vector_store.add_documents(
                    documents=batch,
                    ids=ids
                )

                print(
                    f"Successfully stored {len(batch)} chunks."
                )

                break

            except Exception as error:

                error_message = str(error)

                if "429" not in error_message:
                    raise

                if attempt == MAX_RETRIES - 1:
                    raise

                wait_time = 35 * (attempt + 1)

                print(
                    f"Gemini quota reached. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

    print("\nIngestion completed!")

    print(
        "Total stored chunks:",
        vector_store._collection.count()
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--rebuild",
        action="store_true"
    )

    args = parser.parse_args()

    ingest_documents(rebuild=args.rebuild)
