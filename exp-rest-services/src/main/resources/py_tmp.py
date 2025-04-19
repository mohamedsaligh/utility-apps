import httpx
from typing import Optional, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.base_url = settings.LLM_API_URL
        self.api_key = settings.LLM_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # Optional: shared client instance
        self.client = httpx.AsyncClient(timeout=10)

    async def chat(self, message: str, session_context: Optional[dict] = None) -> Dict[str, Any]:
        """
        Sends a chat message to the LLM with optional session context.

        Args:
            message (str): User message to the LLM.
            session_context (dict, optional): Previous conversation context.

        Returns:
            dict: LLM response containing 'reply' and optionally updated 'context'.
        """
        payload = {
            "message": message,
            "context": session_context or {}
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/chat",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            logger.info("LLM responded successfully")
            return result

        except httpx.HTTPStatusError as http_err:
            logger.error(f"HTTP error from LLM: {http_err.response.status_code} - {http_err.response.text}")
            raise

        except httpx.RequestError as req_err:
            logger.error(f"Request failed: {req_err}")
            raise

        except Exception as ex:
            logger.error(f"Unexpected error: {ex}")
            raise

    async def ask_knowledge_base(self, question: str) -> Dict[str, Any]:
        """
        Optionally query the long-term knowledge base (not session-based).

        Args:
            question (str): Direct question to KB.

        Returns:
            dict: Answer from knowledge base.
        """
        payload = {
            "question": question
        }

        try:
            response = await self.client.post(
                f"{self.base_url}/knowledge-base/query",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()

        except Exception as ex:
            logger.error(f"KB query failed: {ex}")
            raise

    async def close(self):
        await self.client.aclose()
