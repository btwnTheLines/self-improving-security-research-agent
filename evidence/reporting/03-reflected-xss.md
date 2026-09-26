# Report 03 — Reflected Cross-Site Scripting in a name parameter

## Summary
A name parameter is reflected into an HTML response without context-safe output encoding, allowing script injection that executes in a victim's browser.

## Confirmation status
**Confirmed vulnerability** (benign, non-harmful marker; no browser cookie access attempted).

## Affected component
Authenticated "XSS (Reflected)" exercise (`/vulnerabilities/xss_r/`), GET parameter `name`.

## Preconditions
Authenticated session; the target visitor must follow a crafted link. Security level: low (in effect).

## Steps to reproduce
1. `GET /vulnerabilities/xss_r/?name=abc` → `Hello abc`.
2. `GET /vulnerabilities/xss_r/?name=<script>var _xmark=1</script>` → response contains `Hello <script>var _xmark=1</script>` unencoded.

## Expected behavior
The reflected input should be HTML-encoded for its context (or stripped of markup) so it cannot form a live script/tag.

## Actual behavior
The server returned `<pre>Hello <script>var _xmark=1</script></pre>` — the input is echoed verbatim, forming an executable script element in the page.

## Security impact
Arbitrary script execution in the context of the application for any user who opens the crafted link; session/token compromise is possible in principle (data theft). Impact supported: client-side script injection (reflected XSS).

## Evidence / PoC
Response line: `<pre>Hello <script>var _xmark=1</script></pre>` (raw: `evidence/reporting/raw/xssr_proof.txt`). Baseline control (`name=abc`) reflected inert text, so the difference is attributable to the injected markup.

## Remediation
Apply context-aware output encoding for every reflection and stored value, set a restrictive Content-Security-Policy, and validate input.

## Severity rationale
Exploitation requires a user to click a crafted link; impact is script execution in the user's session. Reported Medium (authenticated surface, reflected, browser-executed).

## Limitations / remaining uncertainty
Markup is reflected by the server; actual browser execution and cookie theft were not performed. The DOM/ stored forms are reported separately.