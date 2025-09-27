
import json
import cohere
from app.settings import get_settings
from app.schemas.llm_providers import LlmProvider, GenerateTextResponse
from app.utilities.wikipedia_utilities import fetch_wikipedia_search_results

def get_wikipedia_tool_def():
        return {
            "type": "function",
            "function": {
                "name": "wikipedia_search",
                "description": (
                    "Search Wikipedia for information relevant to a query, returning "
                    "titles, snippets, and URLs"
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search term to look up on Wikipedia"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
class CohereUtilities:
    def __init__(self):
        self.settings = get_settings()

    async def generate_text(self, prompt: str, llm_provider: LlmProvider):
        try:
            token_usage = 0
            if not llm_provider.default_api_key:
                raise ValueError("API key is required for Cohere service. location oW9bCqqpc")
            co = cohere.ClientV2(llm_provider.default_api_key)
            response = co.chat(
                model=llm_provider.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            response_text = str(response.message.content[0].text)
            token_usage += int(response.usage.tokens.input_tokens)
            token_usage += int(response.usage.tokens.output_tokens)
            response_object = GenerateTextResponse(
                response_text=response_text,
                token_usage=token_usage
            )
            return response_object
        except Exception as e:
            raise ValueError(f"Failed to initialize Cohere client: {str(e)}; location aqNxMwGz2C")
        
    async def chat_with_tools(self, user_message: str, llm_provider: LlmProvider):
        response_object = GenerateTextResponse(
                response_text="",
                token_usage=0
            )
        
        # define tools
        wikipedia_tool = get_wikipedia_tool_def()

        # initial message list
        messages = [
            {"role": "user", "content": user_message}
        ]

        # send to Cohere with tools
        co = cohere.ClientV2(llm_provider.default_api_key)
        response = co.chat(
            model=llm_provider.model,
            messages=messages,
            tools=[wikipedia_tool] 
        )

        response_object.token_usage += int(response.usage.tokens.input_tokens)
        response_object.token_usage += int(response.usage.tokens.output_tokens)

        # Check if Cohere has requested a tool call
        if response.message.tool_calls:
            # for simplicity, we assume only one tool call is made
            tool_call = response.message.tool_calls[0]
            if tool_call.function.name == "wikipedia_search":
                
                # parse JSON arguments
                args = json.loads(tool_call.function.arguments)
                query_arg = args.get("query")
                
                # run wikipedia search
                wiki_result = await fetch_wikipedia_search_results(query_arg)

                # append the tool result to messages
                messages.append(
                    {
                        "role": "assistant",
                        "content": wiki_result
                    }
                )
                # then let the LLM finalize
                final_response = co.chat(
                    model=llm_provider.model,
                    messages=messages
                )
                response_object.token_usage += int(final_response.usage.tokens.input_tokens)
                response_object.token_usage += int(final_response.usage.tokens.output_tokens)
                response_object.response_text = str(final_response.message.content[0].text)
        else:
            # no tool call needed, return response directly
            response_object.response_text = str(response.message.content[0].text)

        return response_object