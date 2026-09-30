# Release 1.0 — Local SMS classification experiment

This is a completed release within the scope below. Version 1.0 does not imply public-service readiness, unlimited traffic, security certification or an uptime guarantee.

## Supported use
Local SMS classification experiment. Start commands and examples are in [README.md](README.md). Use Python 3.11 or newer in a clean virtual environment with the pinned requirements. Browser interfaces are available where documented; the health probe is a command-line tool.

## Verification
4 tests. Run `python -m unittest discover -s tests -v` from this repository. A green result with skipped PostgreSQL tests does not count as PostgreSQL verification; use the isolated database job in CI for that coverage. Never run destructive test fixtures against an operational database.

## Storage and recovery
Training artifacts in results; retain source dataset and pinned dependencies. Missing model returns 503. Malformed dataset rows are rejected before training. Preserve deduplication, split boundaries and dataset attribution.

For a SQLite database, use Python's `sqlite3.Connection.backup()` to an independent destination rather than copying an open database file. Restore only while all writers are stopped, keep the current database as a fallback, and test the restored copy before replacing it. For PostgreSQL, use a dedicated role and the provider's documented export/restore process. Never commit database copies, tokens, passwords, real customer records or uploaded files.

## Operating boundaries
English SMS baseline, not a current scam detection guarantee. Do not expose the unauthenticated API publicly or load untrusted model artifacts.

## Change control
Run the full tests before publishing a change. Keep existing measurements and attribution. A benchmark rerun is a new observation, not permission to replace an unfavorable result. Store secrets in environment variables. Roll back to a known working commit only after checking compatibility with any schema changes; do not force push or erase newer unrelated work.

## Security reports
Never put credentials, private datasets or customer receipts in public issues. A sanitized issue can describe the affected version, expected behavior and a minimal synthetic reproduction. No independent security audit is claimed.
