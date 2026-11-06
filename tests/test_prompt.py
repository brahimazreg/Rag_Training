from configure import PROMPT,LLM_MODEL
from langchain_core.prompts import ChatPromptTemplate

def main():

    context = """
    Microsoft Fabric is a SaaS platform.
    It allows users to get, create, share,
    and visualize data.
    """

    question = "What is Microsoft Fabric?"
    
    prompt = ChatPromptTemplate.from_template(PROMPT)

    formatted_prompt = prompt.invoke({
        "context": context,
        "question": question
    })

    response = LLM_MODEL.invoke(formatted_prompt)

    print(response.content)

    #print(formatted_prompt.to_string())


if __name__ == "__main__":
    main()