from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda
)

from retriever import get_context









def main():

    question = "How can administrators manage licenses?"


    # Test 1: RunnablePassthrough

    passthrough = RunnablePassthrough()

    result = passthrough.invoke(question)

    print("Passthrough result:")
    print(result)


    # Test 2: RunnableLambda

    context_retriever = RunnableLambda(get_context)

    context = context_retriever.invoke(question)

    print("\nContext result:")
    print(context)

    print("\nContext data type:")
    print(type(context))





if __name__ == "__main__":
    main()
