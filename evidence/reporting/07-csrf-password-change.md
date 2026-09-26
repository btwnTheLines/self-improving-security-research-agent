# Report 07 — Cross-Site Request Forgery on the password-change form

## Summary
The password-change action is a GET request with no anti-CSRF token and no origin check, so a malicious page can forge a password change that executes with the victim's session.

## Confirmation status
**Confirmed vulnerability** (tokenless change demonstrated; password set to its existing value to avoid a net change).

## Affected component
Authenticated "CSRF" exercise, password-change form (`/vulnerabilities/csrf/`), GET parameters `password_new`/`password_conf`.

## Preconditions
A victim must be logged in and visit the attacker's page.

## Steps to reproduce
1. Ensure the victim's current password is `password`.
2. `GET /vulnerabilities/csrf/?password_new=password&password_conf=password&Change=Change` (from an attacker origin, no token).

## Expected behavior
A state-changing action (password change) should require proof of intentionality (anti-CSRF token, SameSite, or origin verification), and should not be triggerable via GET.

## Actual behavior
The form has no anti-CSRF token and the change is a GET; the tokenless request returned `<pre>Password Changed.</pre>`.

## Security impact
A cross-origin site can change the victim's password (account-takeover vector) if the victim is logged in and loads attacker content. Impact supported: forged state-changing request (password change) without CSRF protection.

## Evidence / PoC
Response: `<pre>Password Changed.</pre>` from a GET containing no token (raw: `evidence/reporting/raw/csrf_change.txt`). The password was changed to the same current value, so no net state change occurred.

## Remediation
Use an anti-CSRF token for all state-changing requests, require POST with correct content-type, enforce SameSite cookies/origin checks, and never expose state changes over GET.

## Severity rationale
Lowered by the requirement that the victim be logged in and browse attacker content; password change = high-impact action. Reported Medium/High; demonstrated non-destructively.

## Limitations / remaining uncertainty
The password was set to its current value (no net change) to avoid a real credential alteration. Actual cross-origin browser delivery was not performed.