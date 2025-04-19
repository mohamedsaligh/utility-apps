from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.adapters.llm_client import LLMClient
from app.repositories.session_repo import get_session_by_id, create_or_update_session
from app.schemas.chat import ChatRequest, ChatResponse

chat_router = APIRouter()


class ChatService:
    def __init__(self, llm_client: LLMClient, db: Session):
        self.llm_client = llm_client
        self.db = db

    async def handle_chat(self, request: ChatRequest) -> ChatResponse:
        session = get_session_by_id(self.db, request.session_id)
        context = session.context if session else {}

        try:
            llm_response = await self.llm_client.chat(message=request.message, session_context=context)
        except Exception as e:
            raise HTTPException(status_code=500, detail="LLM request failed")

        new_context = llm_response.get("context", context)
        reply = llm_response.get("reply", "[No response]")

        create_or_update_session(
            db=self.db,
            session_id=request.session_id,
            user=request.user,
            context=new_context
        )

        return ChatResponse(session_id=request.session_id, user=request.user, reply=reply)
