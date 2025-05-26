import datetime

import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(page_title="NewsFudge", layout="wide")

# Initialize session state
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "conversations_list" not in st.session_state:
    st.session_state.conversations_list = []
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

# Fetch conversations
def load_conversations():
    try:
        res = requests.get(f"{API_URL}/conversations")
        res.raise_for_status()
        st.session_state.conversations_list = res.json()
    except Exception as e:
        st.error(f"Failed to load conversations: {e}")

# Create new conversation
def create_conversation():
    convo_id = str(uuid.uuid4())
    data = {
        "id": convo_id,
        "title": f"Conversation {len(st.session_state.conversations_list) + 1}",
        "qa_list": [],
        "created_at": datetime.datetime.now().isoformat()
    }
    try:
        res = requests.post(f"{API_URL}/conversations", json=data)
        res.raise_for_status()
        load_conversations()
        st.session_state.conversation_id = convo_id
    except Exception as e:
        st.error(f"Failed to create conversation: {e}")

# Load on first run
if not st.session_state.conversations_list:
    load_conversations()

st.title("🗞️ NewsFudge AI")

# 🔼 Top Row: Dropdown + Button
col1, col2 = st.columns([6, 2])
with col1:
    if st.session_state.conversations_list:
        titles = [c["title"] for c in st.session_state.conversations_list]
        selected_title = st.selectbox("Select Conversation", titles)
        selected_convo = next(c for c in st.session_state.conversations_list if c["title"] == selected_title)
        st.session_state.conversation_id = selected_convo["id"]
    else:
        st.warning("No conversations available.")

with col2:
    if st.button("➕ New Conversation"):
        create_conversation()

# 📜 Show Q/A for selected conversation
if st.session_state.conversation_id:
    try:
        res = requests.get(f"{API_URL}/conversations/{st.session_state.conversation_id}")
        res.raise_for_status()
        conversation = res.json()
        st.session_state.qa_history = conversation["qa_list"]
        st.subheader(conversation["title"])
    except Exception as e:
        st.error(f"Failed to load conversation: {e}")

    for qa in st.session_state.qa_history:
        st.markdown(f"**Q:** {qa['question']}")
        st.markdown(f"**A:** {qa['answer']}")
        st.markdown("---")
        if "urls" in qa and qa["urls"]:
            st.markdown("**Sources:**")
            for url in qa["urls"]:
                st.markdown(f"- [{url}]({url})")


# 🔽 Bottom: Ask new question
st.markdown("## Ask a question")
query = st.text_input("Type your question:", "")
if st.button("🔍 Search"):
    if query.strip():
        try:
            res = requests.get(f"{API_URL}/query", params={"query": query})
            res.raise_for_status()
            answer_full = res.json()
            urls = []
            answer = answer_full["answer"]
            context_list = answer_full["context"]
            for context in context_list:
                metadata = context["metadata"]
                url = metadata["url"]
                urls.append(url)
            qa_payload = {
                "question": query,
                "answer": answer,
                "urls": urls,
                "created_at": datetime.datetime.now().isoformat()
            }
            post_res = requests.post(f"{API_URL}/question/{st.session_state.conversation_id}", json=qa_payload)
            post_res.raise_for_status()

            st.rerun()
        except Exception as e:
            st.error(f"Failed to fetch or store answer: {e}")
