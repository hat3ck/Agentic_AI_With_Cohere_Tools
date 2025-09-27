from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    env: str = os.getenv("ENV")
    app_port: int = int(os.getenv("APP_PORT", 8000))
    db_user: str = os.getenv("DB_USER")
    db_pass: str = os.getenv("DB_PASSWORD") # Must be provided in the environment
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 5432))
    db_name: str = os.getenv("DB_NAME", "postgres")
    echo_sql: bool = False
    project_name: str = "Amir Khaleghi Take Home Assessment"
    log_level: str = "DEBUG"
    debug_logs: bool = False
    default_llm_provider_name: str = "cohere"
    default_llm_provider_model: str = "command-r"


    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def alembic_database_url(self) -> str:
        return self.database_url.replace("postgresql+asyncpg", "postgresql")
    

@lru_cache
def get_settings():
    return Settings()