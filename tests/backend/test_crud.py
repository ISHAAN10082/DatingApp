import pytest
from backend.crud import fetch_and_store_users
from unittest import mock
from sqlalchemy.orm import Session
from backend import models

@pytest.fixture
def mock_db_session():
    db = mock.Mock(spec=Session)
    yield db

@mock.patch('requests.get')
def test_fetch_and_store_users_success(mock_get, mock_db_session):
    mock_get.return_value.json.return_value = {
        "results": [
            {
                "login": {"uuid": "uuid-1234"},
                "email": "test@example.com",
                "name": {"first": "Test", "last": "User"},
                "gender": "male",
                "location": {
                    "coordinates": {
                        "latitude": "50.0",
                        "longitude": "10.0"
                    }
                }
            }
        ]
    }
    mock_get.return_value.status_code = 200
    response = fetch_and_store_users(mock_db_session, 1)
    assert response['message'] == "Added 1 new users. Total users: 1"
    assert response['run_id'] is not None
    mock_db_session.add_all.assert_called_once()
    mock_db_session.commit.assert_called_once()

import pytest
from backend.crud import fetch_and_store_users
from unittest import mock
from sqlalchemy.orm import Session
from backend import models

@pytest.fixture
def mock_db_session():
    db = mock.Mock(spec=Session)
    yield db

@mock.patch('requests.get')
def test_fetch_and_store_multiple_users(mock_get, mock_db_session):
    mock_get.return_value.json.return_value = {
        "results": [
            {
                "login": {"uuid": "uuid-1234"},
                "email": "test@example.com",
                "name": {"first": "Test", "last": "User"},
                "gender": "female",
                "location": {
                    "coordinates": {
                        "latitude": "50.0",
                        "longitude": "10.0"
                    }
                }
            }
            ,
            {
                "login": {"uuid": "uuid-5678"},
                "email": "another@example.com",
                "name": {"first": "Another", "last": "User"},
                "gender": "male",
                "location": {
                    "coordinates": {
                        "latitude": "51.0",
                        "longitude": "11.0"
                    }
                }
            }
        ]
    }
    mock_get.return_value.status_code = 200
    response = fetch_and_store_users(mock_db_session, 2)
    assert response['message'] == "Added 2 new users. Total users: 2"
    assert response['run_id'] is not None
    mock_db_session.add_all.assert_called_once() 
    mock_db_session.commit.assert_called_once()

import pytest\nfrom backend.crud import get_random_user\nfrom unittest.mock import MagicMock\nfrom sqlalchemy.orm import Session\n\n@pytest.fixture\ndef mock_db() -> Session:\n    db = MagicMock()\n    user_mock = MagicMock(id=1, name='Test User')\n    db.query.return_value.order_by.return_value.first.return_value = user_mock\n    return db\n\ndef test_get_random_user(mock_db):\n    user = get_random_user(mock_db)\n    assert user.id == 1\n    assert user.name == 'Test User'

import pytest\nfrom backend.crud import get_random_user\nfrom unittest.mock import MagicMock\nfrom sqlalchemy.orm import Session\n\n@pytest.fixture\ndef empty_mock_db() -> Session:\n    db = MagicMock()\n    db.query.return_value.order_by.return_value.first.return_value = None\n    return db\n\ndef test_get_random_user_no_users(empty_mock_db):\n    user = get_random_user(empty_mock_db)\n    assert user is None

import pytest
from backend.crud import get_random_username
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    db = MagicMock()
    return db

@pytest.fixture
def mock_get_random_user(monkeypatch):
    def mock_user(db):
        class User:
            first_name = 'John'
            last_name = 'Doe'
        return User()
    monkeypatch.setattr('backend.crud.get_random_user', mock_user)

def test_get_random_username_with_valid_user(mock_db, mock_get_random_user):
    username = get_random_username(mock_db)
    assert username == 'John Doe'

import pytest
from backend.crud import get_random_username
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    db = MagicMock()
    return db

@pytest.fixture
def mock_get_random_user(monkeypatch):
    monkeypatch.setattr('backend.crud.get_random_user', lambda db: None)

def test_get_random_username_with_no_user(mock_db, mock_get_random_user):
    username = get_random_username(mock_db)
    assert username is None

import pytest
from backend.crud import get_nearest_users
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    user = MagicMock()
    user.email = 'test@example.com'
    user.latitude = 40.7128
    user.longitude = -74.0060
    db.query.return_value.filter.return_value.first.return_value = user
    other_user_1 = MagicMock()
    other_user_1.email = 'other1@example.com'
    other_user_1.latitude = 40.730610
    other_user_1.longitude = -73.935242
    other_user_2 = MagicMock()
    other_user_2.email = 'other2@example.com'
    other_user_2.latitude = 34.0522
    other_user_2.longitude = -118.2437
    db.query.return_value.all.return_value = [user, other_user_1, other_user_2]
    return db

def test_get_nearest_users_user_found(mock_db):
    result = get_nearest_users(mock_db, 'test@example.com', 1)
    assert len(result) == 1
    assert result[0].email == 'other1@example.com'



import pytest
from backend.crud import get_nearest_users
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

@pytest.fixture
def mock_db_user_not_found():
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.first.return_value = None
    return db

def test_get_nearest_users_user_not_found(mock_db_user_not_found):
    result = get_nearest_users(mock_db_user_not_found, 'nonexistent@example.com', 3)
    assert result == []



