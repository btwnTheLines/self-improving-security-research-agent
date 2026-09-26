# Test Record 01 — SQLi single-quote probe on /rest/products/search

Target: `http://localhost:3000` (local OWASP Juice Shop, Docker)
Date: 2026-09-14
Status: **One test only, per explicit human approval. No further testing performed.**

## Hypothesis
The `q` parameter of `GET /rest/products/search` is interpolated into a SQL
query without parameterization (SQL injection).

## Test performed (approved)
Single read-only GET request:

- **Request:**
  `GET /rest/products/search?q=%27`  (i.e. `q='` — one single-quote character)
- **Endpoint:** `/rest/products/search`

## Response / observation
- `HTTP/1.1 200 OK`
- `Content-Type: application/json; charset=utf-8`
- `Content-Length: 30`
- Body: `{"status":"success","data":[]}`

Baseline for contrast (earlier recon record): `q=apple` returned 200 with
matching product rows (`data:[...]` with Apple products).

## Interpretation
- The single quote did **not** yield a DB/SQL error, a non-200 status, or any
  anomaly — the server returned an empty JSON result set with 200.
- Possible readings:
  1. The query is parameterized and treats `'` as literal data with no match
     (not injectable here).
  2. The query is concatenated but the bare quote produced a literal-searching
     query that matched nothing, or DB errors are suppressed/redirected.
- This **single error-based probe produced a negative signal.** It neither
  confirms nor fully rules out SQL injection (boolean/union/time-based variants
  remain untested by design).

## Confidence
- That SQLi is present: **low** (no positive signal obtained).
- That this specific endpoint is not error-based injectable: **moderate**
  (limited to this single probe; error suppression not yet assessed).

## Remaining uncertainty
- Boolean-based/union/time-based injection not evaluated — **intentionally not
  tested** (no further approval given; per Human Verification gate, stop).
- Whether application-level errors are globally suppressed is unknown.
- The exact SQL construction (parameterized vs. string-concatenated) is not
  confirmed.

## Classification
- **Status:** Observation only. Not a confirmed vulnerability.
- A positive signal for this test would have been a non-200 response and/or a
  surfaced DB error; that did not occur.