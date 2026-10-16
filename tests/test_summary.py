"""Composite test: the summary() orchestration against the stub server."""


def test_summary(client):
    result = client.summary("Amsterdam")
    assert result["city"] == "Amsterdam"
    assert result["lat"] == 52.3676
    assert result["temp_c"] == 7.5
    assert result["condition"] == "cloudy"
    assert result["forecast_days"] == 3
