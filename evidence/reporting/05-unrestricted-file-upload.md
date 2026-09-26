# Report 05 — Unrestricted File Upload (server-side type validation absent)

## Summary
An upload feature labeled "Choose an image to upload" accepts and serves non-image files, storing them under the web root, with only client-side restriction — creating stored-content / remote-code potential.

## Confirmation status
**Confirmed vulnerability** (benign non-image file; no executable artifact uploaded).

## Affected component
Authenticated "File Upload" exercise (`/vulnerabilities/upload/`), multipart field `uploaded`.

## Preconditions
Authenticated session. Security level: low (in effect).

## Steps to reproduce
1. `POST /vulnerabilities/upload/` with a non-image text file (`.txt`, `Content-Type: text/plain`, body `UPLOAD-PROOF-INJ-MARKER`).
2. Request the stored file at `/hackable/uploads/proof.txt`.

## Expected behavior
Server should validate that the upload is a permitted image type (and reject non-images/forbid executing types).

## Actual behavior
The non-image `.txt` file was accepted, stored, and served over HTTP 200 with its content — no server-side type/extension restriction. Only the client page describes an image restriction.

## Security impact
Attacker can store arbitrary file types in the web root. This enables stored content (further XSS/HTML) and, for executable types, remote-code potential. Impact supported: arbitrary file storage served from webroot; RCE is inferred, not demonstrated.

## Evidence / PoC
`POST` returned the upload page; `GET /hackable/uploads/proof.txt` → `HTTP/1.1 200 OK` and body `UPLOAD-PROOF-INJ-MARKER` (raw: `evidence/reporting/raw/upload_post.txt`, `upload_fetch.txt`).

## Remediation
Enforce server-side validation of file type (extension and magic bytes) and content, store uploads outside the web root with random names, and serve with a non-executing content type/CSP.

## Severity rationale
Demonstrated: arbitrary non-image storage served from webroot. Reported High for the upload class (given webroot storage), noting an executable payload was deliberately not uploaded, so RCE was not directly demonstrated.

## Limitations / remaining uncertainty
A `.php`/executable file was intentionally not uploaded (to avoid creating an executable webroot artifact); remote-code impact is inferred from the same unrestricted mechanism, not proven.