from typing import List, Optional

from app.utils.config import get_settings


def _try_gemini(user_text: str, context_messages: Optional[List[str]], api_key: Optional[str]) -> Optional[str]:
    if not api_key:
        return None
    try:
        import google.generativeai as genai  # type: ignore

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt_parts: List[str] = ["You are a helpful assistant."]
        if context_messages:
            for c in context_messages[-5:]:
                prompt_parts.append(f"Context: {c}")
        prompt_parts.append(user_text)
        resp = model.generate_content("\n".join(prompt_parts))
        return getattr(resp, "text", None) or (resp.candidates[0].content.parts[0].text if getattr(resp, "candidates", None) else None)
    except Exception:
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


