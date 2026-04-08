# Pytest Reference (Repo Standard)

This file captures the baseline pytest guidance we follow in this repository.

## Version Baseline

- Use `pytest 9.0.x` (current pin in `requirements.txt` is `9.0.3`).
- Verify installed version with:

```bash
pytest --version
```

## Config Baseline

Prefer explicit project config with:

- `minversion`
- `testpaths`
- strict flags in `addopts`

Example:

```ini
[pytest]
minversion = 9.0
testpaths = tests
addopts = -ra --strict-markers --strict-config
```

## Test Design Rules

1. Deterministic first
- No live network/provider access in unit/service tests.
- Patch boundaries with `monkeypatch`.

2. Favor fixtures for setup/teardown
- Keep setup reusable and centralized in `tests/conftest.py` where practical.

3. Use parametrization for input variants
- Prefer `@pytest.mark.parametrize` over duplicated test bodies.

4. Exception assertions
- Use `pytest.raises(...)`.
- Use `match=...` when asserting message content is important.
- Use `exc_info.value` for structured fields.

5. API contract assertions
- Verify status code + content type + response shape.
- For error payloads, verify required problem fields and key extension fields.

## Official Doc Map

- Getting started: `doc/en/getting-started.md`
- Configuration: `doc/en/reference/customize.md`
- Fixtures: `doc/en/how-to/fixtures.md`
- Monkeypatch: `doc/en/how-to/monkeypatch.md`
- Parametrize: `doc/en/how-to/parametrize.md`
- Markers: `doc/en/how-to/mark.md`
- Assertions / raises: `doc/en/how-to/assert.md`, `doc/en/reference/reference.md`
