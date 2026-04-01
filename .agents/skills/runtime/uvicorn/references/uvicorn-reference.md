# Uvicorn Reference Baseline

Last refreshed: 2026-04-02

Resolved Context7 library ID:
- `/kludex/uvicorn`

Use this file as the baseline for Uvicorn guidance used by the `uvicorn` skill.

## Official Documentation Highlights

- Runtime settings for process model, networking, timeouts, limits, and logging.
- Deployment guidance for production serving patterns.
- Proxy/header trust behavior for reverse-proxy environments.

## Source Links

- https://www.uvicorn.org/settings/
- https://www.uvicorn.org/deployment/
- https://github.com/kludex/uvicorn/blob/main/docs/settings.md

## Working Rules

- Treat the links above as authoritative for Uvicorn CLI/runtime behavior.
- If task scope includes process count, proxy trust, or timeout/limit tuning, refresh via Context7 before implementing.
- Keep skill guidance repo-agnostic unless project-specific behavior is explicitly requested.

