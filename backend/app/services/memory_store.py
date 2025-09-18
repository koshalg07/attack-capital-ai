from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import JSON, Column, DateTime, Integer, String, create_engine, func, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


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
        """Return up to k recent messages for user, optionally filtering by LIKE query."""
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


