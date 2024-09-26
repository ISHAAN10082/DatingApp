import pytest
from backend.main import get_db
from unittest.mock import MagicMock

@pytest.fixture
def mock_session_local(monkeypatch):
    mock_session = MagicMock()
    monkeypatch.setattr('backend.main.SessionLocal', lambda: mock_session)
    return mock_session

def test_get_db_scenario1(mock_session_local):
    db_generator = get_db()
    db = next(db_generator)
    assert db == mock_session_local
    db_generator.close()
    mock_session_local.close.assert_called_once()

import pytest
from backend.main import get_db
from unittest.mock import MagicMock

@pytest.fixture
def mock_session_local(monkeypatch):
    mock_session = MagicMock()
    monkeypatch.setattr('backend.main.SessionLocal', lambda: mock_session)
    return mock_session

def test_get_db_scenario2(mock_session_local):
    db_generator = get_db()
    db = next(db_generator)
    assert isinstance(db, MagicMock)
    db_generator.close()
    mock_session_local.close.assert_called_once()

