import pytest
from backend.main import get_db
from unittest.mock import MagicMock
from contextlib import contextmanager

# Mock SessionLocal to simulate database session behavior
@contextmanager
def mock_session():
    db = MagicMock()
    yield db
    db.close()

@pytest.fixture
def db_session(monkeypatch):
    monkeypatch.setattr('backend.main.SessionLocal', mock_session)
    yield get_db()

def test_get_db_scenario1(db_session):
    session = next(db_session)
    assert session is not None

    # Ensure that the session can be used
    assert hasattr(session, 'close')
    session.close = MagicMock()  

    # Close the session and check if close was called
    db_session.close()
    session.close.assert_called_once()

import pytest
from backend.main import get_db
from unittest.mock import MagicMock
from contextlib import contextmanager

@contextmanager
def mock_session():
    db = MagicMock()
    yield db
    db.close()

@pytest.fixture
def db_session(monkeypatch):
    monkeypatch.setattr('backend.main.SessionLocal', mock_session)
    yield get_db()

def test_get_db_scenario2(db_session):
    session = next(db_session)
    assert session is not None

    # Test if the session behaves correctly
    dummy_data = {'key': 'value'}
    session.execute = MagicMock(return_value=dummy_data)

    result = session.execute('SELECT * FROM dummy')
    assert result == dummy_data
    session.close()
    assert session.execute.called
    assert session.close.called
    

