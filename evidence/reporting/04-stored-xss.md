# Report 04 — Stored Cross-Site Scripting in a guestbook

## Summary
Attacker-controlled text stored in a guestbook is rendered to later viewers without HTML encoding, enabling script injection that executes in any other user's browser.

## Confirmation status
**Confirmed vulnerability** (benign, clearly-labeled marker artifact left in the guestbook).

## Affected component
Authenticated "XSS (Stored)" exercise (`/vulnerabilities/xss_s/`), guestbook fields `Name` and `Message`.

## Preconditions
Authenticated session (any role). Security level: low (in effect).

## Steps to reproduce
1. `POST /vulnerabilities/xss_s/` with `Name=INJ-Test-User`, `Message=<b>INJ-stored-marker-ab12</b>` (and the page's CSRF token).
2. Reload `/vulnerabilities/xss_s/`; the stored message is rendered.

## Expected behavior
Stored output should be HTML-encoded so markup is shown as inert text.

## Actual behavior
The stored message renders as a live literal tag: `<b>INJ-stored-marker-ab12</b>` (encoded form absent). Stored attacker markup is output unencoded.

## Security impact
Script/markup stored by one user executes for every other viewer of the guestbook — a stored XSS affecting other users (session/data impact in principle). Impact supported: stored HTML/script injection rendered to other users.

## Evidence / PoC
After the POST, reload contained: `INJ-Test-User<br />Message: <b>INJ-stored-marker-ab12</b><br />` with no HTML-encoding of the tag (raw: `evidence/reporting/raw/xss_s_after.txt`). Control was the safe rendering check (encoded form `False`).

## Remediation
HTML-encode stored user content at output time for its context; apply a restrictive CSP; validate/limit stored field content.

## Severity rationale
Stored XSS affecting other users is higher impact than reflected. Reported High (stored, other-user render), with the caveat that the payload was a benign bold tag, not a harmful script.

## Limitations / remaining uncertainty
A benign `<b>` marker (not a malicious script) was stored and is left in the guestbook as a clearly-labeled test artifact. Real third-party execution/cookie theft were not performed.