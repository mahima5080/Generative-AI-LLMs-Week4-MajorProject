"""
Generative AI & LLMs Internship — Week 4 Capstone
Multimodal RAG & Conversational Memory Pipeline
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CHROMA_PATH = "./chroma_capstone_db"

class RAGMemoryEngine:
    def __init__(self):
        self.conversation_memory = []
        self.usage_analytics = {
            "total_queries": 0,
            "total_tokens_estimated": 0,
            "multimodal_inputs": 0
        }

    def add_to_memory(self, user_msg: str, ai_response: str):
        """Appends user query and assistant answer to conversational history."""
        self.conversation_memory.append({"role": "user", "content": user_msg})
        self.conversation_memory.append({"role": "assistant", "content": ai_response})
        self.usage_analytics["total_queries"] += 1
        self.usage_analytics["total_tokens_estimated"] += (len(user_msg) + len(ai_response)) // 4

    def get_memory_context(self) -> str:
        """Formats historical conversation memory into LLM context."""
        formatted = []
        for msg in self.conversation_memory[-6:]:  # Last 3 turns
            formatted.append(f"{msg['role'].capitalize()}: {msg['content']}")
        return "\n".join(formatted)

    def log_multimodal_event(self):
        self.usage_analytics["multimodal_inputs"] += 1