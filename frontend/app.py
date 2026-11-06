import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from rag_chain import ask_question


# Page configuration
st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📚"
)

st.title("📚 PDF RAG Assistant")
st.caption("Ask questions about your PDF documents.")


# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
question = st.chat_input("Ask a question about your PDFs...")


if question:

    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)


    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("Searching your documents..."):

            try:
                answer = ask_question(question)

            except Exception as e:
                answer = f"An error occurred: {e}"

            st.markdown(answer)


    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })