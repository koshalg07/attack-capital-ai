"""LiveKit chat agent skeleton.

This module sketches how an agent could join a LiveKit room, listen on a
data channel (e.g., topic 'lk.chat'), and respond via LLM + memory.

It is intentionally lightweight and not wired to auto-run. Consult LiveKit
Agents examples to implement real-time behaviors.
"""

from typing import Optional

from app.services.llm_client import generate_reply
from app.services.memory_store import Mem0Memory, SQLiteMemory
from app.utils.config import get_settings


def handle_user_message(user_id: str, text: str, memory: Optional[SQLiteMemory] = None) -> str:
    mem = memory or SQLiteMemory()
    past = mem.search(user_id=user_id, k=5)
    context_texts = [m["text"] for m in past]
    reply = generate_reply(text, context_messages=context_texts)
    mem.save(user_id=user_id, text=text, metadata={"role": "user"})
    mem.save(user_id=user_id, text=reply, metadata={"role": "assistant"})
    return reply


def run_agent(identity: Optional[str] = None, room: str = "default") -> None:  # pragma: no cover
    """Join a LiveKit room as an agent and respond to lk.chat messages."""
    from livekit import agents
    from livekit.agents import JobContext

    settings = get_settings()
    agent_identity = identity or settings.agent_identity

    async def entry(ctx: JobContext):  # type: ignore
        room_info = await ctx.connect(
            url=settings.livekit_ws_url,
            token=agents.token.VideoGrant(
                identity=agent_identity,
                room=room,
                can_publish_data=True,
                room_join=True,
            ).to_jwt(settings.livekit_api_key, settings.livekit_api_secret),
        )

        mem = Mem0Memory()

        async def on_data(pkt: agents.proto.DataPacket):  # type: ignore
            if pkt.topic != "lk.chat":
                return
            user = pkt.participant.identity or "user"
            text = pkt.data.decode("utf-8")
            reply = handle_user_message(user, text, mem)
            await ctx.room.local_participant.publish_data(reply.encode("utf-8"), topic="lk.chat")

        ctx.room.on("data_received", on_data)

    agents.run(entry)



