from dotenv import load_dotenv

from langchain_groq import ChatGroq

from configure import GROQ_MODEL_NAME, MAX_OUTPUT_TOKENS


load_dotenv()


LLM_MODEL = ChatGroq(
    model=GROQ_MODEL_NAME,
    temperature=0.0,
    max_tokens=MAX_OUTPUT_TOKENS
)