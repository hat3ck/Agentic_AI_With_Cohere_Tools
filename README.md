# Amir_Khaleghi_Async_Take_Home_Assessment

# LLM Integration with Wikipedia Tool

This project is a FastAPI-based application that integrates with Cohere’s LLMs and adds support for tool use.  
In particular, it demonstrates how to extend a chat endpoint with a **Wikipedia search tool**, allowing the LLM to fetch relevant information before generating a final answer.

The system is designed with extensibility in mind — new LLM providers and tools can be added easily.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized execution)
- PostgreSQL database (this project uses a free Supabase instance in development)

### Setup

1.  Clone this repository:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Set up environment variables:
    This project uses .env files for configuration. For convenience in this assignment, .env files are included in the repo.
    Normally you should not commit .env files with secrets.

5.  Run database migrations (if needed):

    1.  To create a new migration after modifying models, run:

            ```bash
            ENV=[ENV] DB_HOST=[DB_HOST] DB_USER=[DB_USER] DB_PORT=[DB_PORT] DB_PASSWORD=[DB_PASSWORD] DB_NAME=[DB_NAME] COHERE_API_KEY=TEST alembic revision --autogenerate -m "MESSAGE"
            ```
    2.  To apply existing migrations, run:

            ```bash
            ENV=[ENV] DB_HOST=[DB_HOST] DB_USER=[DB_USER] DB_PORT=[DB_PORT] DB_PASSWORD=[DB_PASSWORD] DB_NAME=[DB_NAME] COHERE_API_KEY=TEST  alembic upgrade head
            ```

6. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Access the API documentation at `http://localhost:8000/docs`

## Video Walkthrough

A short video explaining the code and design decisions can be found here:

[Watch the Video Walkthrough](https://drive.google.com/file/d/1Qk7PxUI0H4SL3AeNIOXAySVwx53FjOqR/view?usp=sharing)


# Design Decisions & Limitations

**Database choice**:
Used Postgres (via Supabase) for reliability and performance.
MongoDB could have worked too, but Postgres was simpler and better supported within the time limits.

**Schema design**:
Two main tables:
- **llm_providers**: stores provider configs (API keys, limits, models).

- **llm_prompts**: stores user inputs and responses.
Included fields like calls_per_minute and tokens_per_minute to support future rate limiting.

**API keys**:
Stored as plaintext for this experiment. In production, keys should be encrypted at rest.

**Auth & tokens**:
Since Cohere trial uses static API keys instead of OAuth2, no refresh logic was implemented.
The schema allows adding refresh tokens later if needed.

**Logging**:
Used simple print() statements for now. Would switch to a structured logger (e.g., Python logging or Loguru) for production.

**Error tracking**:
Added unique 10-character IDs to error messages for easier troubleshooting.

**Database migrations**:
Managed with Alembic for upgrade/downgrade safety.

**Testing**:
Used mocked DB sessions for unit tests.
Couldn’t set up full integration tests due to hitting free Supabase limits.

**Security**:
.env files and plain API keys are committed here for simplicity. This should never happen in production.

**LLM architecture**:
Abstracted providers to allow plugging in multiple LLM vendors (e.g., Cohere, OpenAI).

**Tool use**:
Implemented chat_with_tools that integrates Cohere’s Tool Use API.
Added wikipedia_search as a first tool. Can easily be extended with more tools.

**Containerization**:
Provided a Dockerfile for easier deployment.

# What I’d Change Before moving to Production

- Encrypt API keys in the database, or use a secrets manager.

- Remove .env files from the repo and use a secrets manager (Vault, AWS Secrets Manager, etc.).

- Replace print() statements with a structured logger.

- Add rate limiting based on calls_per_minute and tokens_per_minute.

- Expand test coverage with integration tests against a staging DB.

- Improve error handling and add user feedback.

- Add authentication and authorization to protect endpoints.

- Configure CI/CD pipeline for deployment.

# Resources Used
- [Cohere API Docs](https://docs.cohere.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/en/20/)
- [Alembic Docs](https://alembic.sqlalchemy.org/en/latest/)
- [Wikipedia API Docs](https://www.mediawiki.org/wiki/API:Main_page)
- [Docker Docs](https://docs.docker.com/)

# Endpoints Overview
- `GET /api/llm/chat`: Main chat endpoint that accepts user input and returns LLM responses. Supports tool use.
- `GET /api/llm/prompts`: Retrieve all prompts and responses stored in the database.
- `GET /api/llm/chat_with_tools`: Chat endpoint that demonstrates tool use (e.g., Wikipedia search).



# Docker
## How to build docker image?

```bash
docker build -t cohere-assessment:[VERSION] .
```

## How to update docker image?

```bash

        docker login ghcr.io -u [USERNAME] -p [ACCESS_TOKEN]
        docker tag cohere-assessment:[VERSION] ghcr.io/[USERNAME]/cohere-assessment:[VERSION]
        docker push ghcr.io/[USERNAME]/cohere-assessment:[VERSION]
```

## How to run the app from docker?

```bash
docker run -d --name cohere-assessment \
    -e ENV=[ENV] \
    -e APP_PORT=[APP_PORT] \
    -e DB_HOST=[DB_HOST] \
    -e DB_USER=[DB_USER] \
    -e DB_PORT=[DB_PORT] \
    -e DB_PASSWORD=[DB_PASSWORD] \
    -e DB_NAME=[DB_NAME] \
    -e COHERE_API_KEY=[COHERE_API_KEY] \
    -p 8000:8000 \
    cohere-assessment:[VERSION]

```