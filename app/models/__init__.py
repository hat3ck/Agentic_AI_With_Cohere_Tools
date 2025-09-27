from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here to ensure they are registered with Alembic
from .llm_providers import LlmProviders
from .llm_prompts import LlmPrompts