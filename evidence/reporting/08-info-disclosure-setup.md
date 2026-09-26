# Report 08 — Information Disclosure on an unauthenticated setup page

## Summary
A setup/administration page is reachable **without authentication** and discloses internal server paths, database account name, database/host, environment details, and a writable upload path.

## Confirmation status
**Confirmed vulnerability** (config/informational; corroborated).

## Affected component
`/setup.php` (Database Setup page), reachable with no session cookie.

## Preconditions
None (no authentication). Observed with a fresh, cookie-less request.

## Steps to reproduce
1. `GET /setup.php` with no session cookie → HTTP 200.

## Expected behavior
Administrative/setup pages and their environment details should not be visible to unauthenticated users.

## Actual behavior
Unauthenticated response disclosed: absolute path `/var/www/html/config/config.inc.php`; `[User: www-data] Writable folder /var/www/html/hackable/uploads/`; `MySQL username: app`; `MySQL database: dvwa`; `MySQL host: 127.0.0.1`; OS type `*nix`; backend `MySQL`. (Reported Apache/PHP versions are self-reported and unverified.)

## Security impact
Information disclosure aiding further attacks (the disclosed DB account `app`/host `127.0.0.1`/database `dvwa` was independently corroborated by the read-only SQL injection result `app@localhost`/`dvwa`). Impact supported: internal-path and DB-account disclosure to unauthenticated users.

## Evidence / PoC
`GET /setup.php` (no cookies) → `HTTP/1.1 200 OK`, body containing the paths, `MySQL username: app`, `MySQL database: dvwa`, host `127.0.0.1`, writable upload path (raw: `evidence/reporting/raw/setup_anon.txt`). Corroboration: SQLi `UNION SELECT user(),database()` returned `app@localhost`/`dvwa`.

## Remediation
Require authentication for administrative/setup pages, avoid echoing deployment paths/DB account details, mask internal identifiers, and restrict environment-status output to admins.

## Severity rationale
Disclosed data is moderate but unauth-reachable and self-corroborated; reported Low/Medium (informational with attack-lubricant effect). The password itself was masked (`******`).

## Limitations / remaining uncertainty
Password was masked, not disclosed. Reported PHP version and flags are application-reported and were treated as unverified (not relied upon).