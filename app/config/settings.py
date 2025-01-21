from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Database
    DATABASE_URL: str = "postgresql://localhost/ai_pipelines"

    class Config:
        env_file = ".env"

settings = Settings()