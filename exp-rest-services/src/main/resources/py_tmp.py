import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        self.base_url = settings.LLM_API_URL
        self.api_key = settings.LLM_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))

    async def chat(self, message: str, session_context: Optional[dict] = None) -> Dict[str, Any]:
        """
        Sends a message to the LLM with session context.
        """
        await self._ensure_session()

        payload = {
            "message": message,
            "context": session_context or {}
        }

        try:
            async with self.session.post(
                f"{self.base_url}/chat",
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info("LLM responded successfully")
                return result

        except aiohttp.ClientResponseError as http_err:
            logger.error(f"HTTP error from LLM: {http_err.status} - {http_err.message}")
            raise

        except aiohttp.ClientError as client_err:
            logger.error(f"Request error: {client_err}")
            raise

        except Exception as ex:
            logger.error(f"Unexpected error: {ex}")
            raise

    async def ask_knowledge_base(self, question: str) -> Dict[str, Any]:
        """
        Asks a direct question to the long-term knowledge base.
        """
        await self._ensure_session()

        payload = {
            "question": question
        }

        try:
            async with self.session.post(
                f"{self.base_url}/knowledge-base/query",
                headers=self.headers,
                json=payload
            ) as response:
                response.raise_for_status()
                return await response.json()

        except Exception as ex:
            logger.error(f"KB query failed: {ex}")
            raise

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
