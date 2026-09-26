# WG-04 — Open Redirect (Client-Side / Web)

## 1. Title
Open Redirect — the application redirects to an arbitrary attacker-controlled URL

## 2. Summary
An endpoint accepts a fully attacker-supplied URL and indicates it will redirect the
user's browser to an arbitrary external host. A crafted value such as
`https://evil.example.com/steal` is accepted as a redirect target, enabling a
classic open-redirect (phishing/credential-theft) primitive.

## 3. Confirmation status
**Confirmed vulnerability**

## 4. Affected component
`POST /WebGoat/OpenRedirect/task1` (assignment `OpenRedirectTask1`), parameter `url`.
The endpoint builds a redirect target from the unvalidated `url` value.

## 5. Preconditions
- An authenticated session on the local target.
- No special role required.

## 6. Steps to reproduce
1. Establish an authenticated session.
2. Send:
   `POST /WebGoat/OpenRedirect/task1`
   Body: `url=https://evil.example.com/steal`
3. Observe the response confirms the external redirect.

## 7. Expected behavior
If the open-redirect control were correct, redirect targets would be restricted to
the application's own domain/hosts, and an arbitrary external URL would be rejected.

## 8. Actual behavior
The response reported:
```
"feedback":"You exploited the open redirect! External host accepted.",
"lessonCompleted":true,
"output":"Would redirect to: https://evil.example.com/steal"
```
A control value pointing to the application itself did not complete, confirming the
external-host redirect is the accepted condition.

## 9. Security impact
Open redirect: an attacker can craft a link on the trusted application that silently
forwards the victim to a hostile site (phishing), undermining user trust in the
application's URL origin. No traffic is sent to the external host by this test; the
redirect target alone is returned by the application.

## 10. Evidence / PoC
Raw artifact: `evidence/reporting/raw/wg_open_redirect.txt`

Request:
```
POST /WebGoat/OpenRedirect/task1 HTTP/1.1
Host: 127.0.0.1:8080
url=https%3A%2F%2Fevil.example.com%2Fsteal
```
Response:
```
{"assignment":"OpenRedirectTask1","attemptWasMade":true,
 "feedback":"You exploited the open redirect! External host accepted.",
 "lessonCompleted":true,
 "output":"Would redirect to: https://evil.example.com/steal"}
```

## 11. Remediation
Never build a redirect target from arbitrary user input. Use an allow-list of local
targets/paths only, or server-side mapping, and reject any fully-qualified external
URL that is not expressly permitted.

## 12. Severity rationale
Standard open redirect—low-to-moderate standalone severity (phishing/origin-trust
abuse) but commonly chained in credential-harvesting campaigns. Deterministic and
easily reproduced.

## 13. Limitations / remaining uncertainty
- The redirect was not followed (no outbound traffic); impact is demonstrated by the
  application's own confirmation of the external redirect target.
