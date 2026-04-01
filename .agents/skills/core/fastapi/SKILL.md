---
name: fastapi
description: Build and refactor FastAPI applications with clear API contracts, Pydantic validation, dependency injection, lifespan resource management, and production-ready deployment defaults.
---

# FastAPI Skill

Use this skill to keep FastAPI application code consistent, testable, and aligned with current official guidance.

## Scope and Precedence

- This skill is authoritative for FastAPI app and API design in this repository.
- Use this skill for routing, request/response contracts, validation, dependency wiring, and app lifecycle patterns.
- For ASGI server process and runtime tuning details, pair with `uvicorn`.

## Workflow

1. Confirm baseline
- Confirm FastAPI app entrypoint and router composition.
- Prefer explicit, typed request/response models for every endpoint.

2. Refresh source guidance before large changes
- Use [references/fastapi-reference.md](references/fastapi-reference.md) as baseline.
- Re-check official docs via Context7 when changing deployment, lifespan, or process model behavior.

3. Apply API contract standards
- Use Pydantic models for request and response boundaries.
- Keep handlers thin and move business logic into service modules.
- Use explicit status codes and stable error response shape.

4. Apply dependency and lifecycle standards
- Use FastAPI dependency injection (`Depends`) for pluggable infrastructure concerns.
- Use `lifespan` to initialize and close shared resources (clients, pools, caches).
- Avoid hidden global mutable state when resource lifetime can be app-scoped.

5. Apply deployment defaults
- Prefer production startup with `fastapi run` or `uvicorn` without `--reload`.
- Scale workers explicitly for multi-core production environments.
- Keep configuration environment-driven and documented.

6. Verify
- Validate endpoint contracts (input validation + response shape) for happy and failure paths.
- Confirm startup/shutdown behavior for resources managed in lifespan.
- Confirm deployment command and worker settings are suitable for target environment.

## Team Checklist

Before finishing, confirm:
- Every endpoint has explicit request and response models when applicable.
- Validation errors return predictable, documented responses.
- Shared resources are handled in lifespan and closed correctly.
- Production run mode avoids development-only flags.

