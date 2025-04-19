from app.adapters.payment_client import PaymentClient
from typing import List, Dict, Any


class ValidationService:
    def __init__(self, payment_client: PaymentClient):
        self.payment_client = payment_client

    async def validate_static(self) -> Dict[str, Any]:
        results = []
        static_data = await self.payment_client.get_static_config_data()

        if not static_data:
            return {"status": "error", "message": "No static configuration found"}

        for item in static_data.get("items", []):
            if not item.get("status") or item["status"] != "active":
                results.append({
                    "item": item.get("id"),
                    "issue": "Inactive or missing status"
                })

        return {
            "status": "ok",
            "issues": results
        }

    async def validate_transactional(self) -> Dict[str, Any]:
        issues = []
        transactions = await self.payment_client.get_transaction_data()

        if not transactions:
            return {"status": "error", "message": "No transactions found"}

        for txn in transactions:
            if not txn.get("amount") or txn["amount"] <= 0:
                issues.append({
                    "txn_id": txn.get("id"),
                    "issue": "Invalid transaction amount"
                })

            if not txn.get("timestamp"):
                issues.append({
                    "txn_id": txn.get("id"),
                    "issue": "Missing timestamp"
                })

            if txn.get("status") not in ["completed", "pending"]:
                issues.append({
                    "txn_id": txn.get("id"),
                    "issue": f"Unexpected status: {txn.get('status')}"
                })

        return {
            "status": "ok",
            "issues": issues
        }
