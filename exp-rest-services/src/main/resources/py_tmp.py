from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.services.validation_service import ValidationService
from app.adapters.payment_client import PaymentClient
import asyncio
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

payment_client = PaymentClient()
validation_service = ValidationService(payment_client)


async def run_static_validation():
    try:
        result = await validation_service.validate_static()
        logger.info(f"Static validation result: {result}")
    except Exception as e:
        logger.error(f"Static validation failed: {str(e)}")


async def run_transactional_validation():
    try:
        result = await validation_service.validate_transactional()
        logger.info(f"Transactional validation result: {result}")
    except Exception as e:
        logger.error(f"Transactional validation failed: {str(e)}")


def start_scheduler():
    scheduler.add_job(
        lambda: asyncio.create_task(run_static_validation()),
        trigger=IntervalTrigger(minutes=60),
        id="static_validation",
        replace_existing=True
    )

    scheduler.add_job(
        lambda: asyncio.create_task(run_transactional_validation()),
        trigger=IntervalTrigger(minutes=60),
        id="transactional_validation",
        replace_existing=True
    )

    scheduler.start()
