from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Column, DateTime, Integer, String, create_engine, func, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
import requests


class Base(DeclarativeBase):
    pass


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    meta: Mapped[Optional[Dict[str, Any]]] = mapped_column("metadata", JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class SQLiteMemory:
    """Simple SQLite-backed memory store for chat messages.

    This design keeps the API small and pluggable.
    """

    def __init__(self, url: str = "sqlite:///memory.db") -> None:
        # check_same_thread=False so it works in dev with uvicorn reload
        self.engine = create_engine(url, connect_args={"check_same_thread": False} if url.startswith("sqlite") else {})
        Base.metadata.create_all(self.engine)

    def save(self, user_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        with Session(self.engine) as session:
            row = Message(user_id=user_id, text=text, meta=metadata)
            session.add(row)
            session.commit()
            session.refresh(row)
            return row.id

    def search(self, user_id: str, k: int = 5, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return up to k recent messages for user, optionally filtering by LIKE query.

        This method is a simple recency-based context fetch. For RAG, see `SemanticMemory` below.
        """
        with Session(self.engine) as session:
            stmt = select(Message).where(Message.user_id == user_id)
            if query:
                like = f"%{query}%"
                stmt = stmt.where(Message.text.like(like))
            stmt = stmt.order_by(Message.created_at.desc()).limit(k)
            rows = session.execute(stmt).scalars().all()
            return [
                {
                    "id": r.id,
                    "user_id": r.user_id,
                    "text": r.text,
                    "metadata": r.meta,
                    "created_at": r.created_at.isoformat(),
                }
                for r in rows
            ]


class SemanticMemory:
    """Lightweight in-process RAG using embeddings.

    This is a placeholder showing how to integrate a vector search later (e.g., mem0/Pinecone/FAISS).
    For now it falls back to recency if embeddings are unavailable.
    """

    def __init__(self, base: Optional[SQLiteMemory] = None) -> None:
        self.base = base or SQLiteMemory()
        try:
            import numpy as np  # type: ignore
            self._np = np
        except Exception:
            self._np = None

    def embed(self, text: str) -> Optional[list]:
        # Placeholder: returns None to skip semantic ranking
        return None

    def search(self, user_id: str, k: int = 5, query: Optional[str] = None) -> List[Dict[str, Any]]:
        # If no embeddings, defer to recency search
        return self.base.search(user_id=user_id, k=k, query=query)


class Mem0Memory:
    """Adapter for mem0 HTTP API (save/search). Minimal shape to match our SQLiteMemory API.

    Expects MEM0_BASE_URL and MEM0_API_KEY in settings. If unavailable, falls back to SQLiteMemory.
    API is assumed as:
      POST {base}/memories -> { user_id, text, metadata? }
      GET  {base}/memories/search -> params: user_id, q, k
    Adjust endpoints to your actual mem0 deployment if different.
    """

    def __init__(self, fallback: Optional[SQLiteMemory] = None) -> None:
        from app.utils.config import get_settings

        self.settings = get_settings()
        self.base = self.settings.mem0_base_url
        self.key = self.settings.mem0_api_key
        self.fallback = fallback or SQLiteMemory()

    def _headers(self) -> Dict[str, str]:
        hdrs = {"Content-Type": "application/json"}
        if self.key:
            hdrs["Authorization"] = f"Bearer {self.key}"
        return hdrs

    def save(self, user_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        if not self.base or not self.key:
            return self.fallback.save(user_id, text, metadata)
        try:
            resp = requests.post(
                f"{self.base.rstrip('/')}/memories",
                json={"user_id": user_id, "text": text, "metadata": metadata or {}},
                headers=self._headers(),
                timeout=8,
            )
            resp.raise_for_status()
            data = resp.json()
            return int(data.get("id", 0))
        except Exception:
            return self.fallback.save(user_id, text, metadata)

    def search(self, user_id: str, k: int = 5, query: Optional[str] = None) -> List[Dict[str, Any]]:
        if not self.base or not self.key:
            return self.fallback.search(user_id, k, query)
        try:
            resp = requests.get(
                f"{self.base.rstrip('/')}/memories/search",
                params={"user_id": user_id, "q": query or "", "k": k},
                headers=self._headers(),
                timeout=8,
            )
            resp.raise_for_status()
            items = resp.json() or []
            results: List[Dict[str, Any]] = []
            for it in items[:k]:
                results.append(
                    {
                        "id": it.get("id", 0),
                        "user_id": user_id,
                        "text": it.get("text", ""),
                        "metadata": it.get("metadata"),
                        "created_at": it.get("created_at", ""),
                    }
                )
            return results
        except Exception:
            return self.fallback.search(user_id, k, query)


