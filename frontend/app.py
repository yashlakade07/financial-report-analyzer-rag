import streamlit as st
import requests

st.set_page_config(page_title="Financial Report RAG", page_icon="📊", layout="centered")

st.title("📊 AI Financial Analyst")
st.markdown("Upload a financial report (PDF) and ask questions about its contents.")

API_URL = "http://fastapi-app:8000/api/v1"

# Sidebar for file upload
with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF Report", type=["pdf"])
    
    if st.button("Process Document", type="primary"):
        if uploaded_file is not None:
            with st.spinner("Analyzing document and generating embeddings..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{API_URL}/upload", files=files)
                    response.raise_for_status()
                    st.success(response.json()["message"])
                    st.session_state["doc_processed"] = True
                except requests.exceptions.RequestException as e:
                    st.error(f"Error processing file: {e}")
        else:
            st.warning("Please upload a file first.")

# Main chat interface
st.header("2. Ask Questions")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("e.g., What was the total revenue for Q3?"):
    if not st.session_state.get("doc_processed", False):
        st.error("Please process a document in the sidebar first!")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                try:
                    res = requests.post(f"{API_URL}/chat", json={"question": prompt})
                    res.raise_for_status()
                    data = res.json()
                    
                    answer = data["answer"]
                    sources = ", ".join(data["sources"])
                    full_response = f"{answer}\n\n*Sources: {sources}*"
                    
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to backend: {e}")