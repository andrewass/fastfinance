---
name: uvicorn
description: Configure and operate Uvicorn for production FastAPI services, including worker model, proxy headers, socket binding, timeouts, and logging controls.
---

# Uvicorn Runtime Skill

Use this skill to make ASGI server configuration explicit, safe, and production-ready.

## Scope and Precedence

- This skill is authoritative for Uvicorn process/runtime behavior.
- Use this skill for CLI flags and serving configuration (`workers`, `host`, `port`, proxy headers, timeout settings, log settings).
- For FastAPI route and app-architecture design, pair with `fastapi`.

## Workflow

1. Confirm serving topology
- Confirm whether traffic reaches Uvicorn directly or through a reverse proxy/load balancer.
- Confirm deployment environment (container, VM, or process manager).

2. Refresh source guidance before large changes
- Use [references/uvicorn-reference.md](references/uvicorn-reference.md) as baseline.
- Re-check official docs via Context7 when changing process model, proxy behavior, or server limits.

3. Apply process model standards
- Use `--workers`/`WEB_CONCURRENCY` for production replication.
- Do not combine `--reload` with multiple workers.
- Keep worker count and process strategy aligned with available CPU/memory.

4. Apply network and proxy standards
- Set explicit bind config (`--host`, `--port`, `--uds`, or `--fd`) for the target platform.
- If behind proxies, enable `--proxy-headers` and restrict trust with `--forwarded-allow-ips`.
- Prefer TLS termination at the proxy edge unless there is a clear direct-TLS requirement.

5. Apply resilience and observability standards
- Set keep-alive and graceful shutdown timeouts intentionally.
- Apply capacity controls (`--limit-concurrency`, `--limit-max-requests`, backlog tuning) where needed.
- Set explicit log level/access logging behavior and config source.

6. Verify
- Confirm startup command has production-safe flags.
- Confirm proxy header trust is not over-broad.
- Confirm timeout/limit/log settings are intentional and documented.

## Team Checklist

Before finishing, confirm:
- Production command does not use development reload mode.
- Worker and socket settings match deployment topology.
- Proxy trust settings are constrained to known infrastructure.
- Timeout and limit settings reflect expected traffic profile.

