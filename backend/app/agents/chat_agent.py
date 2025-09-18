"""LiveKit chat agent skeleton.

This module sketches how an agent could join a LiveKit room, listen on a
data channel (e.g., topic 'lk.chat'), and respond via LLM + memory.

It is intentionally lightweight and not wired to auto-run. Consult LiveKit
Agents examples to implement real-time behaviors.
"""

from typing import Optional

from app.services.llm_client import generate_reply
from app.services.memory_store import SQLiteMemory
from app.utils.config import get_settings


def handle_user_message(user_id: str, text: str, memory: Optional[SQLiteMemory] = None) -> str:
    """Core logic to handle a user message using memory + LLM.

    This function is framework-agnostic so it can be tested and reused.
    """
    mem = memory or SQLiteMemory()
    # Retrieve recent context
    past = mem.search(user_id=user_id, k=5)
    context_texts = [m["text"] for m in past]

    # Generate reply
    reply = generate_reply(text, context_messages=context_texts)

    # Save both user message and AI reply
    mem.save(user_id=user_id, text=text, metadata={"role": "user"})
    mem.save(user_id=user_id, text=reply, metadata={"role": "assistant"})
    return reply


def run_agent_listener() -> None:  # pragma: no cover - skeleton only
    """Placeholder for integrating with LiveKit Agents or client SDK.

    Steps (to be implemented with livekit-agents or WebRTC client):
    - Connect to room using a token minted by backend.
    - Subscribe to data topic 'lk.chat'.
    - On message, call handle_user_message(identity, text) and publish reply back.
    """
    _ = get_settings()  # access settings if needed later
    # Implementation intentionally omitted.
    pass


