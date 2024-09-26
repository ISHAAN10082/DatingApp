import pytest
from unittest.mock import MagicMock
from backend.crud import fetch_and_store_users
from sqlalchemy.orm import Session

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    db.query.return_value.count.return_value = 0
    return db

@pytest.fixture
def mock_requests_get(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {
                'results': [
                    {
                        'login': {'uuid': '12345'},
                        'email': 'user@example.com',
                        'name': {'first': 'John', 'last': 'Doe'},
                        'gender': 'male',
                        'location': {
                            'coordinates': {'latitude': '45.0', 'longitude': '-75.0'}
                        }
                    }
                ]
            }
        @staticmethod
        def raise_for_status():
            pass

    monkeypatch.setattr('requests.get', lambda *args, **kwargs: MockResponse())

def test_fetch_and_store_users(mock_db, mock_requests_get):
    response = fetch_and_store_users(mock_db, 1)
    assert response['message'] == 'Added 1 new users. Total users: 1'
    assert mock_db.add_all.call_count == 1
    assert mock_db.commit.call_count == 1

import pytest
from unittest.mock import MagicMock
from backend.crud import fetch_and_store_users
from sqlalchemy.orm import Session

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    db.query.return_value.count.side_effect = [0, 1]
    return db

@pytest.fixture
def mock_requests_get(monkeypatch):
    def side_effect(*args, **kwargs):
        raise requests.RequestException('Network error')
    monkeypatch.setattr('requests.get', side_effect)

def test_fetch_and_store_users_network_error(mock_db, mock_requests_get):
    response = fetch_and_store_users(mock_db, 3)
    assert response['message'] == 'Added 0 new users. Total users: 0'
    assert mock_db.add_all.call_count == 0
    assert mock_db.commit.call_count == 0

import pytest
from backend.crud import get_random_user
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

@pytest.fixture
def mock_db():
    db = MagicMock(spec=Session)
    mock_user = MagicMock()
    db.query.return_value.order_by.return_value.first.return_value = mock_user
    return db

def test_get_random_user_returns_user(mock_db):
    user = get_random_user(mock_db)
    assert user is not None
    mock_db.query.assert_called_once()
    mock_db.query.return_value.order_by.assert_called_once()

import pytest
from backend.crud import get_random_user
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

@pytest.fixture
def empty_mock_db():
    db = MagicMock(spec=Session)
    db.query.return_value.order_by.return_value.first.return_value = None
    return db


def test_get_random_user_no_users(empty_mock_db):
    user = get_random_user(empty_mock_db)
    assert user is None
    empty_mock_db.query.assert_called_once()
    empty_mock_db.query.return_value.order_by.assert_called_once()

import pytest
from backend.crud import get_random_username
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_random_user():
    user = MagicMock()
    user.first_name = 'John'
    user.last_name = 'Doe'
    return user

def test_get_random_username_with_valid_user(mock_db, monkeypatch, mock_random_user):
    monkeypatch.setattr('backend.crud.get_random_user', lambda db: mock_random_user)
    username = get_random_username(mock_db)
    assert username == 'John Doe'

import pytest
from backend.crud import get_random_username
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    return MagicMock()

def test_get_random_username_with_no_user(mock_db, monkeypatch):
    monkeypatch.setattr('backend.crud.get_random_user', lambda db: None)
    username = get_random_username(mock_db)
    assert username is None

import pytest
from backend.crud import get_nearest_users
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    db = MagicMock()
    user1 = MagicMock(email='user1@example.com', latitude=40.748817, longitude=-73.985428)
    user2 = MagicMock(email='user2@example.com', latitude=40.758817, longitude=-73.975428)
    user3 = MagicMock(email='user3@example.com', latitude=41.748817, longitude=-74.985428)
    db.query.return_value.filter.return_value.first.return_value = user1
    db.query.return_value.all.return_value = [user1, user2, user3]
    return db


def test_get_nearest_users_with_nearby_users(mock_db):
    result = get_nearest_users(mock_db, 'user1@example.com', 2)
    assert len(result) == 2
    assert result[0].email == 'user2@example.com'
    assert result[1].email == 'user3@example.com'

import pytest
from backend.crud import get_nearest_users
from unittest.mock import MagicMock

@pytest.fixture
def mock_db():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    return db


def test_get_nearest_users_no_user_found(mock_db):
    result = get_nearest_users(mock_db, 'nonexistent@example.com', 2)
    assert result == []

