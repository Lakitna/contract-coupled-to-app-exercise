"""Generate the consumer/provider contract from the stub catalog.

Reads ``stub_server/stubs.json`` and writes a pact-style ``weather-contract.json``.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STUBS_PATH = REPO_ROOT / "stub_server" / "stubs.json"
CONTRACT_PATH = REPO_ROOT / "contract" / "weather-contract.json"


def build_contract(stubs):
    interactions = []
    for stub in stubs:
        interactions.append(
            {
                "description": f"{stub['id']} {stub.get('description', '')}".strip(),
                "providerState": stub.get("description", ""),
                "request": {
                    "method": stub["method"],
                    "path": stub["path"],
                    "query": stub.get("query", {}),
                },
                "response": {
                    "status": stub["response"].get("status", 200),
                    "body": stub["response"].get("json", {}),
                },
            }
        )
    return {
        "consumer": "weather-app",
        "provider": "weather-api",
        "interactions": interactions,
    }


def main():
    with open(STUBS_PATH, "r", encoding="utf-8") as f:
        stubs = json.load(f)
    contract = build_contract(stubs)
    with open(CONTRACT_PATH, "w", encoding="utf-8") as f:
        json.dump(contract, f, indent=2)
        f.write("\n")
    print(f"Wrote {len(contract['interactions'])} interactions to {CONTRACT_PATH}")


if __name__ == "__main__":
    main()
