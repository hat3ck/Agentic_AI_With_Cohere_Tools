from pydantic import BaseModel, ConfigDict

class LlmPromptsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    provider_id: int
    prompt: str
    created_at: int
    response: str | None = None
    tokens_used: int | None = 0

class LlmPromptsCreate(LlmPromptsBase):
    pass

class LlmPrompts(LlmPromptsBase):
    id: int

class LlmPromptUserResponse(BaseModel):
    prompt: str
    response: str | None = None
    tokens_used: int | None = 0