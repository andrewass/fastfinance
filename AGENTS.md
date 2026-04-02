# Agents Guide

This file gives short, practical instructions for working in this repository.

## Project Snapshot
- Domain: Finance data API backed by Yahoo Finance (`yfinance`)
- Stack: FastAPI, Uvicorn, Pydantic v2, Redis (optional cache persistence)
- Runtime baseline: Python 3.14.3 (Dockerfile default); supported range is Python 3.12 to 3.14.

## Repository Layout
- `/home/andreas/IdeaProjects/fastfinance/app` application code
- `/home/andreas/IdeaProjects/fastfinance/app/main.py` FastAPI entrypoint and router registration
- `/home/andreas/IdeaProjects/fastfinance/app/*/*router.py` API routers by feature
- `/home/andreas/IdeaProjects/fastfinance/app/*/*service.py` business/data-fetch logic
- `/home/andreas/IdeaProjects/fastfinance/app/settings` app and Redis settings
- `/home/andreas/IdeaProjects/fastfinance/app/cache` cache abstraction/decorator/persistence
- `/home/andreas/IdeaProjects/fastfinance/k8s` Kubernetes manifests
- `/home/andreas/IdeaProjects/fastfinance/docker-compose.yml` local Redis service

## Common Commands
- Create venv: `python3 -m venv .venv` (with `python3 --version` in range 3.12 to 3.14)
- Activate venv: `source .venv/bin/activate`
- Install deps: `pip install -r requirements.txt`
- Run API (dev): `uvicorn app.main:app --reload`
- Run API (prod-like): `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- Start local Redis: `docker compose up -d redis`
- Build image: `docker build -t fastfinance-image .`
- Run with Skaffold: `skaffold dev`

## Python and verification policy
- Prefer Python 3.14.3 for local parity with Docker image runtime; Python 3.12 to 3.14 are supported.
- Use a project-local virtual environment (`.venv`) for all local development commands.
- Keep dependency updates explicit in `requirements.txt`; do not introduce undeclared transitive assumptions.
- After code changes, run at least a syntax/import sanity check: `python -m compileall app`.
- For endpoint behavior changes, run a local smoke test with Uvicorn and call touched endpoints.
- If validation needs external services (for example network access to Yahoo Finance or Redis), report blockers clearly.
- Never claim tests/checks passed if they were not executed.

## Conventions
- Keep routers thin; put data fetching/transformation logic in feature service modules.
- Use request/response models for API boundaries and keep response shape stable for existing endpoints.
- Keep required API contract fields strict. Do not mark expected/required response fields as `None`/optional just to avoid failures.
- Keep cache behavior explicit and deterministic; cached service functions should return model objects compatible with `.model_dump()`.
- Prefer small, focused modules by feature (`price`, `holders`, `profile`, `statistics`).
- Centralize environment-driven settings under `app/settings`.

## Quality & Checks
- No repository-wide lint/test command is currently configured in this repo.
- For behavior changes, add or update tests where practical (typically by introducing `tests/` + `pytest` in the same change when requested).
- Preserve backward compatibility for existing route paths unless the task explicitly calls for a breaking API change.

## Dependency & import hygiene
- When introducing a new library, add it to `requirements.txt` in the same change.
- Remove unused imports from touched Python files before finishing.
- Prefer explicit imports from local modules over star imports.

## Commit conventions
- Commit messages must start with a capital letter.

## Working Notes
- `yfinance` calls are network-bound and may fail or return partial fields.
- Wrap outbound `yfinance` operations with `app/integration/yfinanceclient.py::call_yfinance` so transport/TLS/provider exceptions are translated to controlled `502` responses.
- For expected upstream fields, fail fast with explicit, controlled API errors (for example `502`) and include which fields are missing.
- Reserve optional/nullable response fields for domain-optional data only, not as a fallback for upstream inconsistencies.
- Cache persistence defaults to in-memory via `Settings.persistence`; Redis behavior depends on active persistence wiring.
- If changing cache serialization shape, verify compatibility with both memory and Redis persistence implementations.
- Be careful with long-running blocking work in request handlers; document tradeoffs when keeping sync calls in async routes.

## Skills
- Skills under `.agents/skills/**` should be repo-agnostic by default so they can be reused across projects.
- Place reusable skills in `.agents/skills/**` as the default location.
- Do not hardcode repository names, repo-specific paths, or project-only assumptions in reusable skills.
- If project-specific behavior is needed, keep it clearly marked as optional project overlay guidance.
- If `.agents/skills/**` is not writable, stop and ask the user how to proceed before creating skills in any alternate directory.

## Skill folder grouping
- Group skills by domain under `.agents/skills/**` to keep the root tidy.
- Preferred groups:
  - `core/` framework and language fundamentals
  - `runtime/` serving/runtime process behavior
  - `api/` endpoint contract and API standards
  - `data/` persistence and storage patterns
  - `integration/` outbound API/client behavior
  - `ops/` deployability and observability
  - `test/` testing strategy and specialized test skills

## Skill update guardrails
- If `skills-lock.json` is added later, treat every locked skill as read-only by default.
- Do not modify locked skills unless the user explicitly asks to override lock for a specific skill.
- Do not add or modify `skills-lock.json` unless explicitly requested.

## Skill routing
- If the user says `use relevant skills`, automatically select and apply all matching skills from `.agents/skills/**`.
- If the user names a skill explicitly (for example `$fastapi`), always include it.
- Activate `fastapi` for endpoint contracts, dependency wiring, validation/error handling, and app lifecycle guidance.
- Activate `uvicorn` for runtime configuration, worker/process model, proxy headers, socket binding, and timeout/logging controls.
- For mixed tasks, combine all relevant skills rather than choosing only one.
- Use this priority when guidance conflicts: API correctness and safety (`fastapi`) before runtime tuning (`uvicorn`) before style/ergonomics.
