# weather-consumer demo

1. Show the consumer app

   ```plain
   ./app/weather_client.py
   ```

2. Show the stub catalog

   ```plain
   ./stub_server/stubs.json
   ```

3. Start the stub server

   ```shell
   uv run python -m stub_server.server
   ```

4. Show the server working

   ```shell
   curl -v "http://127.0.0.1:8000/v1/current?city=Amsterdam"
   curl -v "http://127.0.0.1:8000/v1/current?city=Utrecht"
   curl -v "http://127.0.0.1:8000/v1/unknown"
   ```

   Note: every request is appended to `stub_server/server.log`

   ```log
   2026-10-16T09:00:00Z GET /v1/current?city=Amsterdam -> P2 current amsterdam
   2026-10-16T09:00:03Z GET /v1/unknown -> NO_MATCH
   ```

5. Run the tests while showing the log stream

   Note: the suite boots its own stub server on a random port and rewrites `stub_server/server.log`

   ```shell
   uv run pytest -vv
   ```

   Show test files

   ```plain
   ./tests/test_weather_client.py
   ./tests/test_summary.py
   ```

6. Generate the contract

   ```shell
   uv run python contract/generate_contract.py
   ```

   Show the contract

   ```plain
   ./contract/weather-contract.json
   ```

## What CBT maturity level is the application?

The generated contract (`./contract/weather-contract.json`) is published to the central contract repository.
