from fastapi import APIRouter
from pydantic import BaseModel

from app.services.memory_store import Mem0Memory, SQLiteMemory
from app.services.llm_client import generate_reply
from app.utils.config import get_settings


router = APIRouter(prefix="/agent", tags=["agent"])


class ReplyRequest(BaseModel):
    userId: str
    text: str


@router.post("/reply")
def agent_reply(payload: ReplyRequest):
    # Use mem0 if configured, else fallback to SQLite transparently
    memory = Mem0Memory()
    context = [m["text"] for m in memory.search(user_id=payload.userId, k=5)]
    reply = generate_reply(payload.text, context_messages=context)
    memory.save(payload.userId, payload.text, {"role": "user"})
    memory.save(payload.userId, reply, {"role": "assistant"})
    return {"reply": reply}


@router.get("/status")
def agent_status():
    settings = get_settings()
    # probe mem0 availability by checking env presence
    has_mem0 = bool(settings.mem0_base_url and settings.mem0_api_key)
    return {"geminiConfigured": bool(settings.gemini_api_key), "mem0Configured": has_mem0}


