import pytest
from backend.main import get_db
from unittest.mock import MagicMock

@pytest.fixture
def mock_session(monkeypatch):
    mock_db = MagicMock()
    SessionLocal = MagicMock(return_value=mock_db)
    monkeypatch.setattr('backend.main.SessionLocal', SessionLocal)
    yield mock_db

def test_get_db_scenario1(mock_session):
    db_gen = get_db()
    db = next(db_gen)
    assert db is mock_session
    db_gen.close()
    mock_session.close.assert_called_once()

import pytest
from backend.main import get_db
from unittest.mock import MagicMock

@pytest.fixture
def another_mock_session(monkeypatch):
    mock_db = MagicMock()
    SessionLocal = MagicMock(return_value=mock_db)
    monkeypatch.setattr('backend.main.SessionLocal', SessionLocal)
    yield mock_db

def test_get_db_scenario2(another_mock_session):
    db_gen = get_db()
    db = next(db_gen)
    assert db is another_mock_session
    db_gen.close()
    another_mock_session.close.assert_called_once()

