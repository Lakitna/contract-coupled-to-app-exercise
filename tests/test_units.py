"""Pure unit tests that do not touch the stub server."""

import pytest

from app.weather_client import WeatherAPIError, WeatherClient


def test_client_requires_base_url(monkeypatch):
    monkeypatch.delenv("WEATHER_BASE_URL", raising=False)
    with pytest.raises(ValueError):
        WeatherClient()


def test_base_url_is_normalized():
    client = WeatherClient("http://example.com/")
    assert client.base_url == "http://example.com"


def test_error_message_format():
    err = WeatherAPIError(503, {"error": "down"})
    assert err.status == 503
    assert "503" in str(err)
