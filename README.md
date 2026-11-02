
# NEXIS GenAI Production Platform (Generative AI & LLMs — Week 4 Major Project Capstone)

A production-ready domain-specific AI Assistant platform built with Google Gemini API, FastAPI streaming backend, Streamlit dashboard, RAG pipeline, conversational memory, multimodal support (Text + Images), safety guardrails, and real-time usage analytics[cite: 25].

---

## 📌 Core Platform Features

- **FastAPI Streaming Backend:** Low-latency token streaming using `StreamingResponse`[cite: 25].
- **Multimodal RAG & Memory:** Ingests images and documents with conversational history tracking[cite: 25].
- **Safety Guardrails:** Pre-execution prompt injection and malicious keyword filtering[cite: 25].
- **Analytics Dashboard:** Tracks query counts, token estimations, and file upload statistics[cite: 25].
- **Docker & CI/CD:** Fully containerized (`Dockerfile`) with automated GitHub Actions CI/CD workflows (`ci-cd.yml`)[cite: 25].

---

## 🚀 How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
