---
name: pytest-best-practices
description: Write and refactor Python tests with pytest using deterministic fixtures, monkeypatch isolation, parametrization, strict configuration, and clear exception assertions. Use when adding tests, reviewing test quality, or setting up pytest configuration for a service or library.
---

# Pytest Best Practices

Use this skill to keep pytest test suites reliable, readable, and CI-friendly.

## Workflow

1. Configure pytest explicitly
- Keep a project config (`pytest.ini`, `pytest.toml`, or `pyproject.toml`) with:
  - `minversion`
  - `testpaths`
  - strict options (`--strict-markers`, `--strict-config`)
- Keep test discovery predictable by using the default `test_*.py` naming or a documented override.

2. Keep tests deterministic
- Avoid live network, real external APIs, and clock-dependent behavior in unit/service tests.
- Patch integration boundaries with `monkeypatch` or local fakes.
- Prefer small fixtures over repeated setup logic.

3. Structure tests by behavior
- Use clear Arrange/Act/Assert flow.
- Keep one primary behavior per test.
- Group related variations with `@pytest.mark.parametrize`.

4. Assert exceptions precisely
- Use `pytest.raises(...)` for expected failures.
- When asserting message/content, use `match=...`.
- Inspect captured exception data (`exc_info.value`) for structured assertions.

5. Keep API tests contract-focused
- Assert status code, response content type, and stable response shape.
- For error responses, assert required contract fields and key extension fields.

## References

- Read [references/pytest-reference.md](references/pytest-reference.md) when you need concrete command patterns, config examples, and the official doc map for fixtures/monkeypatch/parametrize/raises/markers.

## Recommended Patterns

```python
import pytest

@pytest.mark.parametrize("value,expected", [(1, 2), (2, 3)])
def test_increment(value, expected):
    assert value + 1 == expected

def test_error_case():
    with pytest.raises(ValueError, match="must be positive"):
        raise ValueError("must be positive")
```

```ini
[pytest]
minversion = 9.0
testpaths = tests
addopts = -ra --strict-markers --strict-config
```

## Review Checklist

- Tests avoid real network/provider calls unless explicitly integration/e2e.
- Fixtures isolate setup and cleanup cleanly.
- Parametrization is used for repeated input/output variants.
- Exception tests use `pytest.raises` and assert important details.
- Assertions verify contract-critical fields, not incidental implementation details.
