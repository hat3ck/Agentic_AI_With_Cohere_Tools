import os
import pytest
from dotenv import load_dotenv
from app.settings import get_settings
from unittest.mock import AsyncMock, MagicMock

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)
settings = get_settings()

@pytest.fixture
def mock_db_session():
    """
    Returns a mocked async SQLAlchemy session.
    Can be used in ChatService or FastAPI route tests.
    """
    session = AsyncMock()

    # Create a default execute mock returning a MagicMock (for fetchone)
    mock_result = MagicMock()
    mock_result.fetchone.return_value = None  # default: no rows
    session.execute.return_value = mock_result

    return session