# Facilitator notes — DO NOT SHARE WITH LEARNERS

## Verdict

The repo _looks_ like level 3a: a stub server runs during the tests, a contract is
generated and committed, and the suite is green. It is actually **level 2** — the
contract is coupled to neither the app's real behaviour nor a verified provider
interface. It is a **false 3a**.

## The buckets

All 8 stubs live in one catalog (`stub_server/stubs.json`), are served by the stub server,
and are serialized into the contract. The split is purely about whether a test
exercises them.

| Stub | Endpoint                                         | In contract? | Exercised by a test? | Bucket      |
| ---- | ------------------------------------------------ | ------------ | -------------------- | ----------- |
| P1   | `GET /v1/geocode?city=Amsterdam`                 | yes          | yes                  | both        |
| P2   | `GET /v1/current?city=Amsterdam`                 | yes          | yes                  | both        |
| P3   | `GET /v1/forecast?city=Amsterdam&days=3`         | yes          | yes                  | both        |
| L1   | `GET /v1/history?city=Amsterdam&date=2026-01-15` | yes          | yes                  | both        |
| L2   | `GET /v1/current?city=Utrecht` (503)             | yes          | yes                  | both        |
| P4   | `GET /v1/alerts?city=Amsterdam`                  | yes          | **no**               | **dormant** |
| P5   | `GET /v1/current?city=Rotterdam`                 | yes          | **no**               | **dormant** |
| P6   | `GET /v1/air-quality?city=Amsterdam`             | yes          | **no**               | **dormant** |

**5 both, 3 dormant, 0 test-only.**

## Why it _feels_ like 3a

- A stub server actually runs during the test session.
- A contract file is generated and committed, with 8 interactions that look two-sided.
- The tests pass.

That combination reads as "consumer-driven contract testing". But the contract is
generated from a **static catalog**, not from what the tests actually call or assert.
P4-P6 were never exercised — they are fantasy interactions the app does not depend on,
yet they inflate the contract and make it look comprehensive.

## Three detection moves (with expected results)

1. **Coverage cross-check.** After `uv run pytest`, diff the contract's 8 interactions
   against the distinct stub ids in `stub_server/server.log`.
   _Expected:_ hits for P1, P2, P3, L1, L2; **zero** hits for P4, P5, P6 → 3 dormant.

2. **Mutation test.** Change a dormant interaction's response (e.g. P5 Rotterdam
   `temp_c` 8.1 → -40), regenerate the contract (`uv run python contract/generate_contract.py`),
   run the suite again.
   _Expected:_ **still green** — no test reads that stub, so the contract change is inert.

3. **Deletion test.** Remove P4, P5, P6 from `stub_server/stubs.json`, regenerate, run the suite.
   _Expected:_ **still green** — nothing depended on them. (Contrast: deleting P2 breaks
   `test_current` and `test_summary`.)

## The fix (describe, do not implement)

Generate the contract from **matched** interactions — the requests the tests actually
make and the responses they assert — not from a static catalog. Then the contract can
only contain interactions the consumer really exercises, and a dormant stub cannot
silently pad it. (In real Pact this is exactly what the consumer test run records.)

## Debrief questions

- Where did the "3a feeling" come from? (A server ran + a contract existed + green tests.)
- Why does green prove nothing here? (The contract was never checked against the log.)
- How would you word the Detector question to catch this? ("Which contract interactions
  were actually exercised in this run?")
- What is the provider-side analogue? (A provider verifying against a contract that
  lists interactions no consumer ever sends — while missing ones it does.)
