# WG-02 — Missing Function-Level Access Control: Unprivileged User Invokes Privileged Function

## 1. Title
Broken Function-Level Authorization — an ordinary user can invoke an administrator function

## 2. Summary
A function that the UI exposes only under an "Admin" menu—creating a user object
and setting the privileged (`admin`) attribute—is reachable and callable by a normal
authenticated user. The server never verifies the caller's role, so an unprivileged
principal can place an `admin:true` user into the system.

## 3. Confirmation status
**Confirmed vulnerability**

## 4. Affected component
`POST /WebGoat/access-control/users` (controller method `MissingFunctionACUsers.addUser(User)`), an administration function reachable from the hidden "Admin → Users" menu. Called with an authenticated session of an *ordinary* (non-admin) user.

## 5. Preconditions
- An authenticated session as a **non-privileged** user (the standard throwaway account used throughout this assessment).
- No valid admin token/role required.

## 6. Steps to reproduce
1. Log in with a normal user session.
2. Send:
   `POST /WebGoat/access-control/users`
   `Content-Type: application/json`
   Body: `{"username":"wgatmpwnA1","password":"pw123456","admin":true}`
3. Observe the response echoes the created user with `admin:true`.

## 7. Expected behavior
If function-level authorization were enforced, a non-admin session would be denied
(401/403) before reaching the `addUser` handler, and the handler would not accept a
privileged flag from the client for an unprivileged caller.

## 8. Actual behavior
The non-admin session reached the privileged handler and the server accepted and
echoed the submitted `admin:true` flag:

```
{"username":"wgatmpwnA1","password":"pw123456","admin":true}
```
A repeat with `admin:false` was likewise accepted and echoed `admin:false`, showing
the client-supplied privilege attribute is honored directly, with no server-side
role check on the calling session.

## 9. Security impact
Privilege escalation primitive via broken function-level authorization: a user with
no administrator rights can invoke administrator functionality and request that a
user be created with elevated `admin` privileges. This is the vertical (function-level)
access-control failure class.

## 10. Evidence / PoC
Raw artifacts:
- `evidence/reporting/raw/wg_authz_adduser_admin.txt` (`admin:true` accepted)
- `evidence/reporting/raw/wg_authz_adduser_nonadmin.txt` (`admin:false` control value)
- `evidence/reporting/raw/wg_authz_listusers_trace.txt` (the separate list-users function)

Request:
```
POST /WebGoat/access-control/users HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: application/json

{"username":"wgatmpwnA1","password":"pw123456","admin":true}
```
Response: `HTTP/1.1 200` `{"username":"wgatmpwnA1","password":"pw123456","admin":true}`

## 11. Remediation
Enforce authorization on the server for every privileged function (role/ACL check on
the session, never trusting a client-asserted flag). Where role must be settable, it
should be derived/validated server-side and never accepted from the request body for
a caller without appropriate authority.

## 12. Severity rationale
High for a function-level control gap: it converts any low-privilege account into one
that can assert administrator state. Impact is demonstrated here as creation of an
admin-flagged user object; full post-elevation capability (e.g., logging in as that
user) was not chained, so the end-to-end effect is partially unproven.

## 13. Limitations / remaining uncertainty
- End-to-end login using the created `admin:true` user was not performed; the
  demonstrated impact is the successful misuse of the privileged function and the
  honoring of the privileged flag.
- The "list all users" admin function in the same controller returned an empty 500
  for this session and was not relied on for the finding.
- Two throwaway records (`wgatmpwnA1`, `wgatmpwnA2`) were created in the lab and
  remain as benign data artifacts.
