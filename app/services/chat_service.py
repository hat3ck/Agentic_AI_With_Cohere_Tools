from app.settings import get_settings
from sqlalchemy import text
from app.schemas.llm_prompts import LlmPromptsCreate
from app.schemas.llm_providers import LlmProvider, GenerateTextResponse
from app.utilities.db_helper import DBHelper
from app.utilities.cohere_utilities import CohereUtilities
import time

class ChatService(object):
    def __init__(self, db_session):
        self.session = db_session
        self.settings = get_settings()
        self.db_helper = DBHelper(db_session)
        self.llmProviders = {
            "cohere": CohereUtilities(),
            # Add other LLM providers here as needed
            # "openai": OpenAI_utilities,
        }

    async def get_all_prompts(self):
        return await self.db_helper.get_all_llm_prompts()

    async def send_message(self, prompt: str):
        try:
            # We can implement prompt validation here if needed
            # get llm provider from the database
            providerConfig = await self.db_helper.get_llm_provider_by_name_model(
                name=self.settings.default_llm_provider_name,
                model=self.settings.default_llm_provider_model
            );
            if not providerConfig:
                raise Exception("LLM Provider not configured correctly; location Y6MBnq9CtP")
            
            response = await self.llmProviders[providerConfig.name].generate_text(prompt, providerConfig)
            # update token usage
            await self.db_helper.increment_llm_provider_token_usage(providerConfig.id, response.token_usage)
            # commit the session because we consumed tokens regardless of success or failure
            await self.session.commit()

            # save the prompt and response
            await self.create_prompt(providerConfig, prompt, response)
            
            return response.response_text
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error in send_message: {str(e)}; location egZ5V7ZJgE")
        
    async def chat_with_tools(self, prompt: str):
        try:
            # We can implement prompt validation here if needed
            # get llm provider from the database
            providerConfig = await self.db_helper.get_llm_provider_by_name_model(
                name=self.settings.default_llm_provider_name,
                model=self.settings.default_llm_provider_model
            );
            if not providerConfig:
                raise Exception("LLM Provider not configured correctly; location Y6MBnq9CtP")
            
            # Call Cohere utilities chat_with_tools
            response = await self.llmProviders[providerConfig.name].chat_with_tools(prompt, providerConfig)
            # update token usage
            await self.db_helper.increment_llm_provider_token_usage(providerConfig.id, response.token_usage)
            # commit the session because we consumed tokens regardless of success or failure
            await self.session.commit()

            # save the prompt and response
            await self.create_prompt(providerConfig, prompt, response)

            return response.response_text
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error in chat_with_tools: {str(e)}; location HERSLWiHCr")
        
    async def create_prompt(self, 
                            providerConfig:LlmProvider, 
                            prompt: str,
                            response: GenerateTextResponse):
        try:
            prompt_entry = LlmPromptsCreate(
                provider_id=providerConfig.id,
                prompt=prompt,
                response=response.response_text,
                created_at=int(time.time()),
                tokens_used=response.token_usage
            )
            await self.db_helper.create_llm_prompt(prompt_entry)
            await self.session.commit()
            return prompt_entry
        except Exception as e:
            await self.session.rollback()
            raise Exception(f"Error in create_prompt: {str(e)}; location NzNrWQ4HMk")