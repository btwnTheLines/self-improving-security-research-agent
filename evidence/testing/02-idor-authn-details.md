# Test Record 02 — IDOR probe: /rest/user/authentication-details/1 (unauthenticated)

Target: `http://localhost:3000` (local OWASP Juice Shop, Docker)
Date: 2026-09-14
Status: **One test only, per explicit human approval. No enumeration / no follow-up performed.**

## Hypothesis
Broken object-level access control (IDOR): `/rest/user/authentication-details/:id`
can be read without authentication, exposing another user's security-question record.

## Test performed (approved)
Single read-only request, **no Authorization header**:

- **Request:** `GET /rest/user/authentication-details/1`
- **Endpoint:** `/rest/user/authentication-details/:id`
- **Input:** path id = `1` (lowest/seed user)

## Response / observation
- `HTTP/1.1 401 Unauthorized`
- `Content-Type: text/html; charset=utf-8`
- Body: Express error page titled
  `UnauthorizedError: No Authorization header was found` (inner h2: `401 UnauthorizedError: No Authorization header was found`).
- Banner text on the page: `OWASP Juice Shop (Express ^4.22.1)`.

## Interpretation
- The endpoint **rejected the unauthenticated request (401)** before returning any
  data. No user-1 security-question object was disclosed.
- **Negative signal** for the "readable without authentication" form of the
  hypothesis at this endpoint: it does **not** allow unauthenticated object access.
- Note this only tests the **missing-token** case. It does **not** rule out
  object-level access between two *authenticated* users, and it does not assess
  other `/api/*` or `/rest/*` resources.

## Confidence
- That `authentication-details` requires an Authorization header (401 unauth): **high** (directly observed).
- That IDOR is absent on this endpoint / across the API: **low to unsupported** — the single unauthenticated probe is insufficient to establish security for authenticated cross-user access or other endpoints.

## Remaining uncertainty
- Cross-user IDOR (User A reading User B's record while both authenticated) is **untested** — intentionally, per the one-test constraint and Human Verification gate.
- Authorization status of other `/api/*` resources (e.g., `/api/Users`, `/api/Orders`, `/api/Cards`) is **untested**.
- Only this single id/object was queried; no enumeration performed.

## Classification
- **Status:** Observation only. **Not a confirmed vulnerability.**