from fastapi import Request, HTTPException
from typing import Dict


def extract_auth_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
    return auth_header.split(" ")[1]


def get_user_context(request: Request) -> Dict[str, str]:
    token = extract_auth_token(request)
    # This is a placeholder; in a real system you'd decode and verify token
    user_id = "user-from-token"
    return {
        "user_id": user_id,
        "token": token
    }






import logging
import sys

def setup_logger(name: str = "app", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = setup_logger()








import uuid
from datetime import datetime
from typing import Any


def generate_uuid() -> str:
    return uuid.uuid4().hex


def current_utc_timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, (str, list, dict, set, tuple)):
        return len(value) == 0
    return False


def safe_get(d: dict, keys: list, default=None) -> Any:
    value = d
    try:
        for key in keys:
            value = value[key]
        return value
    except (KeyError, TypeError):
        return default
