import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.title("RAG Application")

question = st.text_input("Ask a question")

if st.button("Submit"):

    if question.strip():

        try:
            response = requests.post(
                API_URL,
                json={"question": question},
                timeout=120
            )

            response.raise_for_status()

            result = response.json()

            st.subheader("Answer")
            st.markdown(result["answer"])

            st.subheader("Sources")

            for source in result["sources"]:

                st.write(
                    f"📄 {source['source']} "
                    f"- Page {source['page']}"
                )

        except requests.exceptions.RequestException as e:

            st.error(f"API connection error: {e}")

    else:
        st.warning("Please enter a question.")