from app.adapters.payment_client import PaymentClient
from typing import List, Dict, Any


class PaymentService:
    def __init__(self, payment_client: PaymentClient):
        self.payment_client = payment_client

    async def fetch_transactions(self) -> List[Dict[str, Any]]:
        transactions = await self.payment_client.get_transaction_data()
        return transactions

    async def fetch_static_configurations(self) -> Dict[str, Any]:
        configs = await self.payment_client.get_static_config_data()
        return configs

    async def fetch_transactions_by_filter(self, filter_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        transactions = await self.payment_client.get_transaction_data(filter_params=filter_params)
        return transactions
