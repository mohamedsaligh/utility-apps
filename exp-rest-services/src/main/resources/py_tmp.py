# chat
from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    user: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    user: str
    reply: str



# payment
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class Transaction(BaseModel):
    id: str
    amount: float
    status: str
    timestamp: Optional[datetime]
    metadata: Optional[dict] = None


class StaticConfigItem(BaseModel):
    id: str
    name: str
    status: str
    details: Optional[dict] = None


class TransactionListResponse(BaseModel):
    items: List[Transaction]


class StaticConfigResponse(BaseModel):
    items: List[StaticConfigItem]



# validation
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ValidationIssue(BaseModel):
    item: Optional[str]
    issue: str
    details: Optional[Dict[str, Any]] = None


class ValidationResult(BaseModel):
    status: str
    issues: List[ValidationIssue]


class ValidationRequest(BaseModel):
    type: str
    parameters: Optional[Dict[str, Any]] = None
