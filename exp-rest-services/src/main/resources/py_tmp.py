import uvicorn
from fastapi import FastAPI
from app.services.chat_service import chat_router
from app.services.scheduler import start_scheduler
from app.utils.logger import logger

app = FastAPI(title="LLM Validator App")

app.include_router(chat_router, prefix="/chat")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting LLM Validator App...")
    start_scheduler()
    logger.info("Scheduler started.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down LLM Validator App...")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

