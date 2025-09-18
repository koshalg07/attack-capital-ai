import os
from functools import lru_cache
from typing import List, Optional
from dataclasses import dataclass

try:
    # Load .env if python-dotenv is available
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    pass


@dataclass
class Settings:
    livekit_api_key: str
    livekit_api_secret: str
    livekit_ws_url: str
    port: int
    gemini_api_key: Optional[str]
    agent_identity: str
    cors_origins: List[str]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    livekit_api_key = os.environ.get("LIVEKIT_API_KEY", "")
    livekit_api_secret = os.environ.get("LIVEKIT_API_SECRET", "")
    livekit_ws_url = os.environ.get("LIVEKIT_WS_URL") or os.environ.get("LIVEKIT_URL", "")
    port_str = os.environ.get("PORT", "3001")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    agent_identity = os.environ.get("AGENT_IDENTITY", "assistant")

    cors_raw = os.environ.get("CORS_ORIGINS", "http://localhost:5173")
    cors_origins = [o.strip() for o in cors_raw.split(",") if o.strip()]

    try:
        port = int(port_str)
    except ValueError:
        port = 3001

    return Settings(
        livekit_api_key=livekit_api_key,
        livekit_api_secret=livekit_api_secret,
        livekit_ws_url=livekit_ws_url,
        port=port,
        gemini_api_key=gemini_api_key,
        agent_identity=agent_identity,
        cors_origins=cors_origins,
    )


