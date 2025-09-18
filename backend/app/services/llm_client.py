from typing import List, Optional

from app.utils.config import get_settings


def _try_gemini(user_text: str, context_messages: Optional[List[str]], api_key: Optional[str]) -> Optional[str]:
    if not api_key:
        return None
    try:
        import google.generativeai as genai  # type: ignore

        settings = get_settings()
        genai.configure(api_key=api_key)
        model_name = settings.gemini_model or "gemini-1.5-flash"
        model = genai.GenerativeModel(model_name)
        # Build a clean prompt that doesn't echo context back
        recent = context_messages[-5:] if context_messages else []
        context_block = "\n".join(f"- {c}" for c in recent)
        prompt = (
            "You are a concise, helpful assistant. "
            "Use the provided context only if relevant. "
            "Do NOT repeat the context back. Answer naturally.\n\n"
            f"Context:\n{context_block}\n\n"
            f"User: {user_text}"
        )
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", None) or (
            resp.candidates[0].content.parts[0].text if getattr(resp, "candidates", None) else None
        )
        return text.strip() if isinstance(text, str) else text
    except Exception as e:
        # Debug log to surface why Gemini call failed
        print("Gemini error:", repr(e))
        return None


def generate_reply(user_text: str, context_messages: Optional[List[str]] = None) -> str:
    """Generate a reply using Gemini if configured; otherwise return a stub echo."""
    settings = get_settings()

    # Prefer Gemini if available
    gemini = _try_gemini(user_text, context_messages, settings.gemini_api_key)
    if gemini:
        return gemini

    # Final stub
    return f"(stub) You said: {user_text}"


