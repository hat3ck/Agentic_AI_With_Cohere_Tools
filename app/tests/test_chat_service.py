import json
import os
from unittest.mock import AsyncMock, patch
import pytest
from app.schemas.llm_providers import GenerateTextResponse, LlmProvider
from app.services.chat_service import ChatService
from app.utilities.wikipedia_utilities import fetch_wikipedia_search_results
from app.utilities.cohere_utilities import CohereUtilities

@pytest.mark.asyncio
async def test001_send_message_with_prompt(mock_db_session):
    try:
        # Read provider data from file
        provider_file_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            f"test_001_llm_provider.json"
        )
        with open(provider_file_path, 'r') as file:
            provider_data = json.load(file)

        # update the api key from environment variable
        provider_data['default_api_key'] = os.getenv("COHERE_API_KEY")

        provider_obj = LlmProvider.model_validate(provider_data)
        
        # Patch the DBHelper method to return provider_obj
        from app.utilities.db_helper import DBHelper
        mock_get_provider = AsyncMock(return_value=provider_obj)

        # Mock increment_llm_provider_token_usage to just succeed
        mock_increment = AsyncMock(return_value=None)

        # Mock create_llm_prompt to just succeed
        mock_create_prompt = AsyncMock(return_value=None)

        ## Apply patch
        with patch.object(DBHelper, "get_llm_provider_by_name_model", mock_get_provider), \
            patch.object(DBHelper, "increment_llm_provider_token_usage", mock_increment), \
            patch.object(DBHelper, "create_llm_prompt", mock_create_prompt):
            # don't mock CohereUtilities.generate_text to test real logic
            chat_service = ChatService(mock_db_session)

            prompt = "What is the capital of Turkey?"
            response = await chat_service.send_message(prompt)

            assert isinstance(response, str)
            assert len(response) > 0
            assert "Ankara" in response  # Assuming the model knows this fact
    except Exception as e:
        pytest.fail(f"Test failed due to an exception: {str(e)}")

@pytest.mark.asyncio
async def test002_test_fetch_from_wikipedia():
    try:
        query = "Cristiano Ronaldo"
        results = await fetch_wikipedia_search_results(query)
        assert isinstance(results, str)
        assert "Cristiano Ronaldo" in results
    except Exception as e:
        pytest.fail(f"Test failed due to an exception: {str(e)}")

@pytest.mark.asyncio
async def test003_chat_with_tools():
    try:
        # Read provider data from file
        provider_file_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            f"test_003_llm_provider.json"
        )
        with open(provider_file_path, 'r') as file:
            provider_data = json.load(file)

        # update the api key from environment variable
        provider_data['default_api_key'] = os.getenv("COHERE_API_KEY")

        provider_obj = LlmProvider.model_validate(provider_data)

        prompt = "Where is the birthplace of Maryam Mirzakhani?"
        cohere_util = CohereUtilities()
        response = await cohere_util.chat_with_tools(prompt, provider_obj)
        assert isinstance(response, GenerateTextResponse)
        assert len(response.response_text) > 0
        assert "Iran" in response.response_text  # Assuming the model knows this fact
    except Exception as e:
        pytest.fail(f"Test failed due to an exception: {str(e)}")