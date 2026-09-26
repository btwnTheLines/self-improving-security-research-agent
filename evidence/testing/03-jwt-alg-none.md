# Test Record 03 — JWT alg:none (signature-bypass) probe on /rest/user/whoami

Target: `http://localhost:3000` (local OWASP Juice Shop, Docker)
Date: 2026-09-14
Status: **One test only, per explicit human approval. No token variations / enumeration / privilege-escalation performed.**

## Hypothesis
The server does not enforce JWT signature verification and accepts `alg:"none"`
unsigned tokens, allowing forgery of any user id without credentials.

## Test performed (approved)
Single read-only request with a hand-built **unsigned** (`alg:none`) JWT:

- Header: `{"alg":"none","typ":"JWT"}` → `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0`
- Payload: `{"uid":1}` → `eyJ1aWQiOjF9`
- Signature: (empty) → trailing `.`
- Token: `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1aWQiOjF9.`

**Request:**
```
GET /rest/user/whoami
Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1aWQiOjF9.
```

## Response / observation
- `HTTP/1.1 200 OK`
- `Content-Type: application/json; charset=utf-8`
- `Content-Length: 11`
- Body: `{"user":{}}`

This body is **identical** to the earlier unauthenticated `whoami` baseline
(`{"user":{}}`).

## Interpretation
- The forged **unsigned** token was **not honored** — `whoami` returned an empty
  `user` object, i.e., the token did not resolve to an identified/in-authenticated
  user. **No authentication bypass observed** with this single test.
- Ambiguity: `{"user":{}}` could mean either (a) the token was rejected due to
  algorithm/signature enforcement, or (b) the token was parsed but `uid` was not
  recognized as a valid identity claim. A single observation cannot distinguish
  these without further (unapproved) testing.

## Confidence
- That this specific `alg:none`+`uid:1` token was not honored at `whoami`: **high** (directly observed; matches unauthenticated baseline).
- That JWT signature/algorithm enforcement is fully secure: **low to unsupported** — only `alg:none` was attempted; other weaknesses (weak/HMAC secret, claim manipulation, algorithm-confusion variants) remain untested, and the uid-claim ambiguity was not resolved.

## Remaining uncertainty
- Whether the token was rejected for signature/algorithm reasons vs. parsed-and-uid-not-found. **Not tested.**
- Weak-HMAC-secret and other JWT pitfalls **not tested** (would require a genuine token, not available).
- No enumeration or additional token variations performed, per instruction.

## Classification
- **Status:** Observation only. **Not a confirmed vulnerability.**