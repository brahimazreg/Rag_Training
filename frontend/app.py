
import os
import requests
import streamlit as st

# Configuration
API_URL = os.getenv(
    "RAG_API_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📚"
)

st.title("📚 PDF RAG Assistant")
st.caption("Ask questions about your PDF documents.")

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Function to communicate with FastAPI
def ask_api(question):

    response = requests.post(
        f"{API_URL}/ask",
        json={"question": question},
        timeout=120
    )

    response.raise_for_status()

    return response.json()


# Display conversation history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:
                with st.expander("📄 Sources"):

                    for source in sources:

                        filename = source["source"]
                        page = source.get("page")

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

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching your documents..."):

            try:
                result = ask_api(question)

                answer = result["answer"]
                sources = result.get("sources", [])

            except requests.exceptions.ConnectionError:
                answer = (
                    "Cannot connect to the FastAPI backend. "
                    "Please check whether the API is running."
                )
                sources = []

            except requests.exceptions.Timeout:
                answer = "The API request timed out. Please try again."
                sources = []

            except requests.exceptions.RequestException as e:
                answer = f"API request failed: {e}"
                sources = []

            except Exception as e:
                answer = f"An unexpected error occurred: {e}"
                sources = []

        st.markdown(answer)

        if sources:

            with st.expander("📄 Sources"):

                for source in sources:

                    filename = source["source"]
                    page = source.get("page")

                    if page is not None:
                        st.markdown(
                            f"- **{filename}** — Page {page}"
                        )
                    else:
                        st.markdown(f"- **{filename}**")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
