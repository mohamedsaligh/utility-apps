from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.session import SessionContext


def get_session_by_id(db: Session, session_id: str) -> SessionContext | None:
    return db.query(SessionContext).filter(SessionContext.session_id == session_id).first()


def create_or_update_session(db: Session, session_id: str, user: str, context: dict) -> SessionContext:
    session = get_session_by_id(db, session_id)
    if session:
        session.context = context
        session.last_updated = datetime.utcnow()
    else:
        session = SessionContext(
            session_id=session_id,
            user=user,
            context=context,
            last_updated=datetime.utcnow()
        )
        db.add(session)

    db.commit()
    db.refresh(session)
    return session


def cleanup_old_sessions(db: Session, days: int = 30) -> int:
    expiry = datetime.utcnow() - timedelta(days=days)
    deleted = db.query(SessionContext).filter(SessionContext.last_updated < expiry).delete()
    db.commit()
    return deleted
