"""Consumer client for the Weather API.

The base URL is read from the WEATHER_BASE_URL environment variable (or passed
directly to the constructor). All endpoints are simple JSON GETs.
"""

import os

import requests


class WeatherAPIError(Exception):
    """Raised when the Weather API returns a non-200 response."""

    def __init__(self, status, body):
        self.status = status
        self.body = body
        super().__init__(f"weather API returned {status}: {body}")


def _safe_body(resp):
    try:
        return resp.json()
    except ValueError:
        return resp.text


class WeatherClient:
    def __init__(self, base_url=None):
        url = base_url or os.environ.get("WEATHER_BASE_URL") or ""
        self.base_url = url.rstrip("/")
        if not self.base_url:
            raise ValueError("base_url is required (pass one or set WEATHER_BASE_URL)")

    def _get(self, path, params):
        resp = requests.get(f"{self.base_url}{path}", params=params, timeout=5)
        if resp.status_code != 200:
            raise WeatherAPIError(resp.status_code, _safe_body(resp))
        return resp.json()

    def geocode(self, city):
        return self._get("/v1/geocode", params={"city": city})

    def current(self, city):
        return self._get("/v1/current", {"city": city})

    def forecast(self, city, days):
        return self._get("/v1/forecast", {"city": city, "days": days})

    def history(self, city, date):
        return self._get("/v1/history", {"city": city, "date": date})

    def summary(self, city):
        """Compose geocode -> current -> forecast into a single view."""
        geo = self.geocode(city)
        cur = self.current(city)
        fc = self.forecast(city, 3)
        return {
            "city": geo["city"],
            "lat": geo["lat"],
            "lon": geo["lon"],
            "temp_c": cur["temp_c"],
            "condition": cur["condition"],
            "forecast_days": len(fc["days"]),
        }
