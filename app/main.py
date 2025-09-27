# Load environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
import uvicorn
from app.api import chat
from app.settings import get_settings
from app.database import get_db
from app.schemas.llm_providers import LlmProvidersCreate
from app.utilities.db_helper import DBHelper
import time
import os

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    # Startup code
    print("Starting up...")
    await add_default_provider()
    yield
    # Shutdown code
    print("Shutting down...")

app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs")

# on start create the default llm provider if it doesn't exist

@app.get("/")
async def read_root():
    return {"message": "Welcome to the LLM Chat API. Visit /api/docs for API documentation."}

# Routers
app.include_router(chat.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=settings.app_port, log_level=settings.log_level.lower())

# Add the default llm provider if it doesn't exist
# THIS BLOCK IS EXPERIMENTAL FOR THE SAKE OF THE ASSESSMENT, NOTMALLY YOU WOULD RUN A DATA MIGRATION SCRIPT
async def add_default_provider():
    default_llm_provider: LlmProvidersCreate = LlmProvidersCreate(
        name="cohere",
        model="command-r",
        default_api_key=os.getenv("COHERE_API_KEY"),
        api_url="https://api.cohere.com/v2",
        tokens_per_minute=350000,
        calls_per_minute=3500,
        total_used_tokens=0,
        is_active=True,
        created_at=int(time.time()),
        access_token=None,
        access_token_expiry=None,
        access_token_type=None
    )
    db_gen = get_db()
    db_session = await anext(db_gen)  # get one yielded session
    try:
        db_helper = DBHelper(db_session)
        # Check if the provider already exists
        existing_provider = await db_helper.get_llm_provider_by_name_model(
            name=default_llm_provider.name,
            model=default_llm_provider.model
        )
        if not existing_provider:
            await db_helper.create_llm_provider(default_llm_provider)
            await db_session.commit()
            print(f"Default LLM provider '{default_llm_provider.name}' added.")
        else:
            print(f"Default LLM provider '{default_llm_provider.name}' already exists.")
    except Exception as e:
        await db_session.rollback()
        print(f"Error adding default LLM provider: {e} ; location 3gF3HyqS2H")
    finally:
    # Make sure to close/cleanup the generator
        await db_gen.aclose()   