# DVWA Security Assessment — Summary

Target: `http://localhost:8080` (authorized, locally controlled training environment).
Scope in effect: application/interfaces only; no external systems. Security level: low (default); no config/database changes made.
Assessment method: evidence-driven, minimal, read-only/benign proofs.

## Confirmed findings (9) — reports generated
| # | Class | Surface | Proof basis | Report |
|---|-------|---------|-------------|--------|
| 1 | SQL Injection | `sqli` | error near `''1'''`; `UNION SELECT user(),database()` → `app@localhost`/`dvwa` | `01-sql-injection.md` |
| 2 | Command Injection | `exec` | `&& echo CMDINJ-CONFIRMED` executed | `02-command-injection.md` |
| 3 | Reflected XSS | `xss_r` | `<script>` reflected unencoded | `03-reflected-xss.md` |
| 4 | Stored XSS | `xss_s` | stored `<b>` marker rendered unencoded to viewers | `04-stored-xss.md` |
| 5 | Unrestricted file upload | `upload` | non-image `.txt` stored & served from webroot | `05-unrestricted-file-upload.md` |
| 6 | Local file inclusion / traversal | `fi` | `../../hackable/uploads/proof.txt` read | `06-local-file-inclusion.md` |
| 7 | CSRF (password change) | `csrf` | tokenless GET → `Password Changed.` | `07-csrf-password-change.md` |
| 8 | Info disclosure (unauthenticated) | `setup.php` | paths, DB account `app`/`dvwa`/`127.0.0.1`, writable upload path | `08-info-disclosure-setup.md` |
| 9 | Weak/predictable session identifier | `weak_id` | `dvwaSession=1,2,3` sequence | `09-weak-session-id.md` |

Raw request/response artifacts preserved under `evidence/reporting/raw/`.

## Hypotheses investigated but NOT confirmed
- **Predictability of the primary `PHPSESSID`** — not established; only the app-generated `dvwaSession` token was shown predictable.
- **Upload RCE / LFI→RCE** — the unrestricted-upload/LFI mechanisms imply code-execution potential, but no executable artifact was uploaded or included; impact is inferred, not demonstrated.
- **Full SQLi write/exfiltration** — read-only metadata proof only; no data read/write beyond identity/metadata.
- **DOM XSS (`xss_d`)** — identified as a client sink surface; not taken to confirmation this pass.

## Authentication / session observations (not separate findings)
- `Set-Cookie: PHPSESSID=...; path=/` and `security=low` — observed cookies carry **no `HttpOnly`/`Secure` flags** in `login_head.txt`/login response. Combined with XSS surfaces, this raises session-exposure risk; recorded as an observation (the primary cookie's value itself was not shown predictable).

## Deliberately NOT exercised (and why)
- **`brute` (login brute-force)** — credential/brute-force attacks disallowed without human approval.
- **`setup.php` "Create/Reset Database"** — destructive administrative control off-limits; would destroy/reset data and needs prior preservation determination.
- **Middle/high/impossible security levels** — out of scope (default low kept).
- **Authentication/authorization bypass probing** — not performed per scope/approval gates.

## Surfaces identified but not assessed this pass
`sqli_blind` (same SQLi class → folded into finding 1), `xss_d` (DOM), `captcha` (Insecure CAPTCHA), `csp` (CSP bypass), `javascript`, `phpinfo.php`. Recorded as unknowns/follow-up.

## Minimum-testing / safety compliance
All proofs: benign `echo` markers, read-only UNION, controlled in-scope files, password set to its current value (no net change), non-destructive. One clearly-labeled benign stored-XSS marker (`<b>INJ-stored-marker-ab12</b>`) and one in-scope test upload (`proof.txt`) remain as test artifacts, flagged as such.

## Remaining uncertainty / limitations
- Version/flags (`PHP 7.0.30-0+deb9u1`, module flags) are application-reported and unverified.
- Findings are demonstrated non-destructively; maximal impact (write, RCE, cookie theft, cross-user access) is not exercised.