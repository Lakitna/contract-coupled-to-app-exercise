"""
Test runner configuration.

Pytest fixtures: boot the stub server on a random port for the test session.
"""

import os
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from werkzeug.serving import make_server

from app.weather_client import WeatherClient
from stub_server.server import LOG_PATH, create_app


@pytest.fixture(scope="session")
def base_url():
    # Start each run with a clean request log.
    with open(LOG_PATH, "w", encoding="utf-8"):
        pass

    app = create_app()
    server = make_server("127.0.0.1", 0, app)
    port = server.port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{port}"
    os.environ["WEATHER_BASE_URL"] = url
    try:
        yield url
    finally:
        server.shutdown()


@pytest.fixture
def client(base_url):
    return WeatherClient(base_url)
