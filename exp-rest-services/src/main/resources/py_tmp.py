from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LLM_API_URL: str
    LLM_API_KEY: str
    PAYMENT_API_URL: str
    PAYMENT_API_KEY: str
    DB_PATH: str = "./app/database/app.db"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
