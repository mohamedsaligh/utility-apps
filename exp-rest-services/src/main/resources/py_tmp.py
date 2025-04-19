import aiohttp
from typing import Optional, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class PaymentClient:
    def __init__(self):
        self.base_url = settings.PAYMENT_API_URL
        self.api_key = settings.PAYMENT_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.session: Optional[aiohttp.ClientSession] = None

    async def _ensure_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))

    async def get_transaction_data(self, filter_params: Optional[Dict[str, Any]] = None) -> Any:
        await self._ensure_session()
        url = f"{self.base_url}/transactions"
        try:
            async with self.session.get(url, headers=self.headers, params=filter_params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Transaction API call failed: {str(e)}")
            return []

    async def get_static_config_data(self) -> Any:
        await self._ensure_session()
        url = f"{self.base_url}/config/static"
        try:
            async with self.session.get(url, headers=self.headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Static config API call failed: {str(e)}")
            return []

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
