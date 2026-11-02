"""
Generative AI & LLMs Internship — Week 4 Capstone
Streamlit Web Dashboard for Production GenAI Platform
"""

import os
import streamlit as st
import requests

st.set_page_config(page_title="NEXIS GenAI Platform", page_icon="⚡", layout="wide")

st.title("⚡ NEXIS Solutions LLM Platform")
st.write("Production-Ready Domain-Specific AI Assistant with Streaming, RAG, Memory, & Guardrails")

# Sidebar Analytics & Controls
st.sidebar.header("📊 Usage Analytics")
try:
    analytics_resp = requests.get("http://127.0.0.1:8000/analytics").json()
    st.sidebar.metric("Total Queries Processed", analytics_resp.get("total_queries", 0))
    st.sidebar.metric("Estimated Tokens Used", analytics_resp.get("total_tokens_estimated", 0))
    st.sidebar.metric("Multimodal Files Ingested", analytics_resp.get("multimodal_inputs", 0))
except Exception:
    st.sidebar.warning("API Server offline.")

st.sidebar.markdown("---")
st.sidebar.markdown("🔒 **Safety Guardrails:** ACTIVE")
st.sidebar.markdown("🧠 **Conversational Memory:** ACTIVE")

# Main Interface Tabs
tab1, tab2 = st.tabs(["💬 Multimodal Chat Assistant", "📘 Architecture & Documentation"])

with tab1:
    user_input = st.text_area("Enter your prompt / question:", "Explain how streaming LLM responses work in production FastAPI backends.")
    uploaded_file = st.file_uploader("Attach Image / Code Screenshot (Optional):", type=["jpg", "png", "jpeg"])

    if st.button("🚀 Stream Response", type="primary"):
        if not user_input.strip():
            st.warning("Please enter a question or prompt.")
        else:
            files = {}
            if uploaded_file:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

            data = {"prompt": user_input}
            
            with st.spinner("Connecting to FastAPI Streaming Backend..."):
                try:
                    res = requests.post("http://127.0.0.1:8000/chat/stream", data=data, files=files, stream=True)
                    if res.status_code == 200:
                        st.subheader("🤖 Streamed AI Output")
                        output_area = st.empty()
                        full_text = ""
                        for chunk in res.iter_content(chunk_size=None, decode_unicode=True):
                            if chunk:
                                full_text += chunk
                                output_area.markdown(full_text + "▌")
                        output_area.markdown(full_text)
                    else:
                        st.error(f"Error ({res.status_code}): {res.json().get('detail')}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")

with tab2:
    st.markdown("""
    ### 🏛️ System Architecture Overview
    - **Backend API:** FastAPI with async streaming responses (`StreamingResponse`).
    - **LLM Engine:** Google Gemini API (`gemini-2.5-flash`).
    - **Guardrails:** Automated input sanitization and prompt injection checks.
    - **Memory:** Multi-turn conversational context tracking[cite: 25].
    - **Multimodal Support:** Tensor processing for text and visual file uploads[cite: 25].
    """)