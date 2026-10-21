import streamlit as st
import requests

st.set_page_config(page_title="KnowFlow AI", page_icon="🤖", layout="wide")

API_URL = "http://127.0.0.1:8000/api/v1"

st.title("🤖 KnowFlow AI — Enterprise Knowledge & Decision Assistant")
st.markdown("Secure document ingestion, vector RAG search, LLM Q&A, and business analytics.")

# Sidebar for Authentication & Navigation
st.sidebar.header("Authentication & Control")
auth_mode = st.sidebar.radio("Mode", ["Login", "Register"])

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

if "token" not in st.session_state:
    st.session_state["token"] = ""

if auth_mode == "Register":
    full_name = st.sidebar.text_input("Full Name")
    if st.sidebar.button("Register"):
        res = requests.post(f"{API_URL}/auth/register", json={"email": email, "password": password, "full_name": full_name})
        if res.status_code == 201:
            st.sidebar.success("Registered successfully! Please log in.")
        else:
            st.sidebar.error(res.json().get("detail", "Registration failed"))
else:
    if st.sidebar.button("Login"):
        res = requests.post(f"{API_URL}/auth/login", data={"username": email, "password": password})
        if res.status_code == 200:
            st.session_state["token"] = res.json()["access_token"]
            st.sidebar.success("Logged in successfully!")
        else:
            st.sidebar.error("Invalid credentials")

if st.session_state["token"]:
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    
    tab1, tab2, tab3 = st.tabs(["📚 Document Ingestion & RAG", "📊 Business Analytics", "🛡️ ML Anomaly Detection"])
    
    with tab1:
        st.header("Upload & Query Knowledge Base")
        uploaded_file = st.file_uploader("Upload PDF, TXT, or CSV", type=["pdf", "txt", "csv"])
        if uploaded_file and st.button("Upload Document"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            res = requests.post(f"{API_URL}/documents/upload", headers=headers, files=files)
            if res.status_code == 201:
                st.success(f"Successfully uploaded: {uploaded_file.name}")
            else:
                st.error(res.json().get("detail", "Upload failed"))
                
        st.divider()
        question = st.text_input("Ask a question about your documents:")
        if st.button("Ask AI") and question:
            with st.spinner("Analyzing documents..."):
                res = requests.post(f"{API_URL}/chat/ask", headers=headers, json={"question": question})
                if res.status_code == 200:
                    data = res.json()
                    st.subheader("Answer:")
                    st.write(data["answer"])
                    
                    if data["citations"]:
                        st.subheader("Source Citations:")
                        for citation in data["citations"]:
                            st.info(f"**File:** {citation['filename']} (Chunk {citation['chunk_index']})\n\n> {citation['content_snippet']}")
                else:
                    st.error("Failed to generate answer.")
                    
    with tab2:
        st.header("CSV Executive Insights")
        doc_id = st.number_input("Enter CSV Document ID", min_value=1, step=1)
        if st.button("Generate Analytics & Insights"):
            with st.spinner("Computing statistics and generating insights..."):
                res = requests.post(f"{API_URL}/analytics/insights", headers=headers, json={"document_id": doc_id})
                if res.status_code == 200:
                    data = res.json()
                    st.subheader("Executive Insights:")
                    st.write(data["insights"])
                    st.subheader("Summary Statistics:")
                    st.json(data["summary_stats"])
                else:
                    st.error(res.json().get("detail", "Analytics failed"))
                    
    with tab3:
        st.header("Scikit-Learn Isolation Forest Anomaly Detection")
        vals_input = st.text_input("Enter comma-separated numbers (e.g. 10,12,11,105,13,9):", "10, 12, 11, 105, 13, 9")
        if st.button("Detect Anomalies"):
            try:
                values = [float(x.strip()) for x in vals_input.split(",")]
                res = requests.post(f"{API_URL}/analytics/detect-anomalies", headers=headers, json={"values": values})
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"Anomalies detected at indices: {data['anomalies_detected']}")
                    st.write("Anomaly Scores:", data["scores"])
                else:
                    st.error("Anomaly detection failed.")
            except ValueError:
                st.error("Please enter valid comma-separated numbers.")
else:
    st.info("👈 Please log in using the sidebar to access KnowFlow AI features.")