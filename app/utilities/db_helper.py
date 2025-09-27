from app.models import LlmPrompts as LlmPromptsDBModel
from app.schemas.llm_prompts import LlmPromptUserResponse, LlmPromptsCreate
from app.models import LlmProviders as LlmProvidersDBModel
from app.schemas.llm_providers import LlmProvidersCreate, LlmProvider
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class DBHelper:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_llm_prompts(self):
        # fetch all results with only prompt, response, and tokens_used fields
        result = await self.db_session.execute(
            select(LlmPromptsDBModel.prompt,
                   LlmPromptsDBModel.response,
                   LlmPromptsDBModel.tokens_used)
                   )
        prompts = result.all()
        # convert to list of Pydantic models
        prompts_converted = [LlmPromptUserResponse(
            prompt=p[0], response=p[1], tokens_used=p[2]) for p in prompts]

        return prompts_converted

    async def create_llm_provider(self, provider: LlmProvidersCreate):
        db_provider = LlmProvidersDBModel(**provider.model_dump())
        self.db_session.add(db_provider)
        # let the caller commit
        await self.db_session.flush()
        return db_provider
    
    async def get_llm_provider_by_name_model(self, name: str, model: str):
        result = await self.db_session.execute(
            select(LlmProvidersDBModel).where(
                LlmProvidersDBModel.name == name,
                LlmProvidersDBModel.model == model
            )
        )
        provider = result.scalars().first()
        # convert to Pydantic model
        provider_converted = LlmProvider.model_validate(provider) if provider else None
        return provider_converted
    
    async def increment_llm_provider_token_usage(self, provider_id: int, tokens_used: int):
        result = await self.db_session.execute(
            select(LlmProvidersDBModel).where(LlmProvidersDBModel.id == provider_id)
        )
        provider = result.scalars().first()
        if not provider:
            raise HTTPException(status_code=404, detail="LLM Provider not found; location D5BqiJuNEb")
        provider.total_used_tokens += tokens_used
        self.db_session.add(provider)
        await self.db_session.flush()
        return
    
    async def create_llm_prompt(self, prompt: LlmPromptsCreate):
        db_prompt = LlmPromptsDBModel(**prompt.model_dump())
        self.db_session.add(db_prompt)
        # await self.db_session.flush()
        return