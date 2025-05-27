import pytest
from unittest.mock import MagicMock, patch
import app.cacheRedis as cacheRedis

@pytest.fixture
def mock_redis_client():
    with patch("app.cacheRedis.RedisCache.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        yield mock_client

def test_set_to_cache_success(mock_redis_client):
    mock_redis_client.set.return_value = True
    result = cacheRedis.RedisCache.set("ticket:123", '{"id": "123", "title": "Test"}')
    mock_redis_client.set.assert_called_once()
    assert result is None or result is True  # set returns None if successful

def test_get_from_cache_hit(mock_redis_client):
    mock_redis_client.get.return_value = '{"id": "123", "title": "Test"}'
    result = cacheRedis.RedisCache.get("ticket:123")
    mock_redis_client.get.assert_called_once_with("ticket:123")
    assert result == '{"id": "123", "title": "Test"}'

def test_get_from_cache_miss(mock_redis_client):
    mock_redis_client.get.return_value = None
    result = cacheRedis.RedisCache.get("ticket:999")
    assert result is None

def test_ping_success(mock_redis_client):
    mock_redis_client.ping.return_value = True
    assert cacheRedis.RedisCache.ping() is True

def test_ping_failure(mock_redis_client):
    mock_redis_client.ping.side_effect = Exception("fail")
    assert cacheRedis.RedisCache.ping() is False