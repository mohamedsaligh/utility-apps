from sqlalchemy import Column, Integer, String, JSON, DateTime, Index
from datetime import datetime
from app.database.db import Base


class SessionContext(Base):
    __tablename__ = "session_context"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    user = Column(String, nullable=False)
    context = Column(JSON, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_session_last_updated", "last_updated"),
    )
