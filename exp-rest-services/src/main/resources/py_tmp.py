from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.adapters.llm_client import LLMClient
from app.adapters.payment_client import PaymentClient
from app.services.chat_service import ChatService
from app.services.validation_service import ValidationService
from app.config import settings

# Dependency: provide DB session
def get_db_session() -> Session:
    db = next(get_db())
    return db

# Dependency: LLM Client (reused per request)
def get_llm_client() -> LLMClient:
    return LLMClient()

# Dependency: Payment Client (reused per request)
def get_payment_client() -> PaymentClient:
    return PaymentClient()

# Dependency: Chat Service (combines logic + API)
def get_chat_service(
    llm_client: LLMClient = Depends(get_llm_client),
    db: Session = Depends(get_db_session),
) -> ChatService:
    return ChatService(llm_client, db)

# Dependency: Validation Service
def get_validation_service(
    payment_client: PaymentClient = Depends(get_payment_client)
) -> ValidationService:
    return ValidationService(payment_client)

# Dependency: Auth Context (example)
def get_user_context(request: Request) -> dict:
    # You can parse JWT or API key here
    token = request.headers.get(\"Authorization\")
    return {\"user_id\": \"demo\", \"token\": token}
