from configure import PROMPT
from llm import LLM_MODEL
from retriever import get_context

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.runnables import RunnableParallel

# Step 1: Create prompt template
prompt = ChatPromptTemplate.from_template(PROMPT)


# Step 2: Wrap context function
context_retriever = RunnableLambda(get_context)


# Step 3: Create mapping
mapping = RunnableParallel({
    "context": context_retriever,
    "question": RunnablePassthrough()
})

# Step 4: Connect the complete RAG pipeline
rag_chain = mapping | prompt | LLM_MODEL


# Step 5: Execute the RAG pipeline
def ask_question(question: str):

    response = rag_chain.invoke(question)

    if isinstance(response.content, str):
        return response.content

    return "".join(
        block["text"]
        for block in response.content
        if isinstance(block, dict)
        and block.get("type") == "text"
    )