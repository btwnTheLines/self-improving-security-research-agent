# Test Record 05 — H4 verification: does persisted role:"admin" grant real admin authorization?

Target: `http://localhost:3000` (local OWASP Juice Shop, Docker)
Date: 2026-09-14
Status: **Executed exactly the two approved requests. No enumeration / follow-up performed.**
Reuses throwaway account `mma_probe@test.local` (id 25) from Test Record 04.

## Purpose
Verify whether the `role:"admin"` persisted via mass assignment (Test Record 04)
is honored by the runtime authorization layer (i.e., yields real admin privileges).

## Requests & responses (both approved)

### Step 1 — authenticate as the throwaway account
**Request:**
```
POST /rest/user/login
{"email":"mma_probe@test.local","password":"JU1ceTesTPa$$"}
```
**Response:** `HTTP/1.1 200 OK`, returned a JWT (`RS256`) whose payload `data`
included `"role":"admin"`, `"id":25`, `"isActive":true`. (Confirmed the stored
role is embedded in the issued token.)

### Step 2 — admin-gated resource with the returned token
**Request:**
```
GET /api/Users
Authorization: Bearer <token from step 1>
```
**Response:** `HTTP/1.1 200 OK` (Content-Length 6905) returning the **full user
collection**, including the seed admin accounts (e.g., `admin@juice-sh.op`,
`bjoern.kimminich@gmail.com`, `support@juice-sh.op`) and our throwaway
`mma_probe@test.local` (id 25, `role:"admin"`).

## Interpretation
- The token issued to the mass-assigned account carried `role:"admin"`, and that
  account could successfully read the **admin-only** `/api/Users` listing.
- This confirms the persisted `role` is **honored by the authorization layer**:
  mass assignment at registration yields **effective administrator privileges**
  (privilege escalation). The full H4 chain is validated end-to-end:
  register with injected `role` → admin stored → admin token → admin-gated data access.

## Confidence
- That the account (id 25) holds **effective admin authorization**: **high** —
  directly observed via `200` on an admin-gated resource with the account's token.
- That the mass-assignment registration is the cause: **high** (Test Record 04
  established the injected field was persisted; this record shows it is honored).

## Remaining uncertainty
- **No control test** was run: we did not verify that a normal `customer` token is
  rejected (`401/403`) on `GET /api/Users`. The admin-gated nature of this endpoint
  is assumed from Juice Shop's design; a control would raise confidence further.
- Scope of admin powers beyond user-listing (e.g., `/administration`, `accounting`,
  `feedback` moderation) was **not** enumerated. Not performed by instruction.

## Classification
- **Status:** H4 **confirmed at the impact level** — a self-registered account can
  obtain effective administrator privileges via mass assignment on `POST /api/Users`.
- Final determination remains with the human operator. A suggested optional control
  (customer-token denial check) is offered but was not run and requires separate
  approval.