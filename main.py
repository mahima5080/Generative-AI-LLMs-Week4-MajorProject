"""
Generative AI & LLMs Internship — Week 4 Capstone
FastAPI Production Backend Server
"""

import os
import io
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
from dotenv import load_dotenv
from google import genai
from guardrails import validate_user_input
from RAG_engine import RAGMemoryEngine

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI(
    title="NEXIS Solutions Production GenAI Platform",
    description="LLM-Powered Domain Assistant with RAG, Memory, Guardrails, and Multimodal Support",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

engine = RAGMemoryEngine()

def get_gemini_client():
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY missing in server configuration.")
    return genai.Client(api_key=GEMINI_API_KEY)

@app.get("/analytics")
def get_analytics():
    """Returns usage analytics metrics for the dashboard."""
    return engine.usage_analytics

@app.post("/chat/stream")
async def chat_stream(prompt: str = Form(...), file: UploadFile = File(None)):
    """Streaming response endpoint supporting multimodal inputs and safety guardrails."""
    # 1. Safety Guardrail Check
    guard_check = validate_user_input(prompt)
    if not guard_check["is_safe"]:
        raise HTTPException(status_code=400, detail=guard_check["reason"])

    client = get_gemini_client()
    contents = []

    # 2. Memory Context Integration
    memory_context = engine.get_memory_context()
    full_prompt = f"CONVERSATIONAL HISTORY:\n{memory_context}\n\nUSER QUESTION: {prompt}"

    # 3. Multimodal Image Input Handling
    if file:
        engine.log_multimodal_event()
        image_bytes = await file.read()
        pil_img = Image.open(io.BytesIO(image_bytes))
        contents = [pil_img, full_prompt]
    else:
        contents = [full_prompt]

    # 4. Streamed LLM Execution
    def generate_chunks():
        try:
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=contents
            )
            accumulated_response = ""
            for chunk in response:
                if chunk.text:
                    accumulated_response += chunk.text
                    yield chunk.text
            engine.add_to_memory(prompt, accumulated_response)
        except Exception as e:
            yield f"\n[!] Execution Error: {str(e)}"

    return StreamingResponse(generate_chunks(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)