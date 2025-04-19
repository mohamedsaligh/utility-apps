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
