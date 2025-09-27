from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class LlmPrompts(Base):
    __tablename__ = 'llm_prompts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    provider_id: Mapped[int] = mapped_column(nullable=False)
    prompt: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[int] = mapped_column(nullable=False)
    response: Mapped[str | None] = mapped_column(nullable=True)
    tokens_used: Mapped[int | None] = mapped_column(nullable=True, default=0)