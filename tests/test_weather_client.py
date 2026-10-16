"""Tests for the WeatherClient endpoints against the stub server."""

import pytest

from app.weather_client import WeatherAPIError


def test_geocode(client):
    data = client.geocode("Amsterdam")
    assert data["city"] == "Amsterdam"
    assert data["lat"] == 52.3676
    assert data["country"] == "NL"


def test_current(client):
    data = client.current("Amsterdam")
    assert data["temp_c"] == 7.5
    assert data["condition"] == "cloudy"
    assert data["humidity"] == 82


def test_forecast(client):
    data = client.forecast("Amsterdam", 3)
    assert len(data["days"]) == 3
    assert data["days"][0]["date"] == "2026-10-17"


def test_history(client):
    data = client.history("Amsterdam", "2026-01-15")
    assert data["date"] == "2026-01-15"
    assert data["condition"] == "clear"


def test_current_utrecht_error(client):
    with pytest.raises(WeatherAPIError) as exc:
        client.current("Utrecht")
    assert exc.value.status == 503
