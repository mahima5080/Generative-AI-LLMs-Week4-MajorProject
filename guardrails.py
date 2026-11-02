"""
Generative AI & LLMs Internship — Week 4 Capstone
Guardrails & Safety Moderation Module
"""

BLOCKED_KEYWORDS = ["ignore previous instructions", "system prompt", "drop database", "sudo rm -rf"]

def validate_user_input(text: str) -> dict:
    """Validates user text for prompt injections and malicious content."""
    text_lower = text.lower()
    for keyword in BLOCKED_KEYWORDS:
        if keyword in text_lower:
            return {
                "is_safe": False,
                "reason": f"Input flagged by safety guardrails (Forbidden pattern detected: '{keyword}')"
            }
    
    if len(text.strip()) == 0:
        return {"is_safe": False, "reason": "Empty input submission."}

    return {"is_safe": True, "reason": "Sanitized and validated."}