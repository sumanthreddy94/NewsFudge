import streamlit as st
import requests

st.set_page_config(page_title="NewsFudge", layout="centered")

st.title("📰 NewsFudge AI")
st.write("Ask about news articles.")

query = st.text_input("Enter your question:", "")

if st.button("Search") and query:
    with st.spinner("Searching..."):
        try:
            # Call your FastAPI endpoint
            response = requests.get("http://localhost:8000/query", params={"query": query})
            response.raise_for_status()
            result = response.json()

            st.subheader("Answer:")
            st.write(result)

        except requests.exceptions.RequestException as e:
            st.error(f"Error contacting the backend: {e}")
