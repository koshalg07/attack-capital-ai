from functools import lru_cache
from typing import List, Optional

try:
    # Pydantic v2
    from pydantic_settings import BaseSettings
    from pydantic import Field
except Exception: 
    
    from pydantic import BaseSettings  
    from pydantic import Field 


class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    Uses sensible defaults for local development.
    """

    livekit_api_key: str = Field(default="", alias="LIVEKIT_API_KEY")
    livekit_api_secret: str = Field(default="", alias="LIVEKIT_API_SECRET")
    livekit_ws_url: str = Field(default="", alias="LIVEKIT_WS_URL")

    port: int = Field(default=3001, alias="PORT")

    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    agent_identity: str = Field(default="assistant", alias="AGENT_IDENTITY")

    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])  # frontend dev URL

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  


