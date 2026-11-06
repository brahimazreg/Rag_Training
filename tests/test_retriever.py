from retriever import vector_store


def main():   


    questions = [
        "Who can purchase licenses?",
        "What is the population of Japan?"
    ]

    for question in questions:

        print("\nQUESTION:", question)

        results = vector_store.similarity_search_with_relevance_scores(
            question,
            k=3
        )

        for doc, score in results:

            print("\nSCORE:", score)
            print("SOURCE:", doc.metadata.get("source"))
            print("PAGE:", doc.metadata.get("page_label"))
            print("CONTENT:", doc.page_content[:200])

            print("-" * 50)


if __name__ == "__main__":
    main()
