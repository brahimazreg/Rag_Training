
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
from rag_chain import ask_question_with_sources


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

        # Display sources for assistant messages
        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:

                with st.expander("📄 Sources"):

                    for source in sources:

                        filename = source["source"]
                        page = source["page"]

                        if page is not None:
                            st.markdown(
                                f"- **{filename}** — Page {page}"
                            )
                        else:
                            st.markdown(f"- **{filename}**")


# Chat input
question = st.chat_input(
    "Ask a question about your PDFs..."
)


if question:

    # Save and display user question
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
                result = ask_question_with_sources(question)

                answer = result["answer"]
                sources = result["sources"]

            except Exception as e:

                answer = f"An error occurred: {e}"
                sources = []

        st.markdown(answer)

        # Display sources
        if sources:

            with st.expander("📄 Sources"):

                for source in sources:

                    filename = source["source"]
                    page = source["page"]

                    if page is not None:
                        st.markdown(
                            f"- **{filename}** — Page {page}"
                        )
                    else:
                        st.markdown(f"- **{filename}**")


    # Save assistant response and sources
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
