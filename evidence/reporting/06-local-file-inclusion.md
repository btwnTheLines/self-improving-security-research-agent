# Report 06 — Local File Inclusion / Path Traversal in a page parameter

## Summary
A page parameter is passed to a server-side include with no path restriction, allowing directory-traversal arbitrary file read.

## Confirmation status
**Confirmed vulnerability** (traversal read demonstrated with an in-scope, controlled file).

## Affected component
Authenticated "File Inclusion" exercise (`/vulnerabilities/fi/`), GET parameter `page`.

## Preconditions
Authenticated session. Security level: low (in effect).

## Steps to reproduce
1. `GET /vulnerabilities/fi/?page=../../hackable/uploads/proof.txt&Submit=Submit`.

## Expected behavior
The parameter should be constrained to a safe include allowlist so a traversal cannot address an arbitrary path.

## Actual behavior
The request resolved two directories above the include directory and returned the target file's content (`UPLOAD-PROOF-INJ-MARKER`), demonstrating arbitrary, directory-traversing file read/include.

## Security impact
Arbitrary local file read on the server (proven with a controlled in-scope file). Combined with the upload vector (Report 05), this can enable remote-code execution; impact supported: arbitrary file read.

## Evidence / PoC
`page=../../hackable/uploads/proof.txt` → response contained `UPLOAD-PROOF-INJ-MARKER` (raw: `evidence/reporting/raw/fi_proof.txt`). Control `page=include.php` rendered the normal page.

## Remediation
Use an allowlist of includeable files and resolve/normalize the path server-side, rejecting any `..`/absolute components; avoid including user-supplied paths.

## Severity rationale
Arbitrary file read is High (LFI). Demonstrated read of an in-scope file only; no OS-sensitive file contents were read, so full impact is not exercised.

## Limitations / remaining uncertainty
Only a controlled in-scope file was read to establish traversal; system files (e.g., `/etc/passwd`) were intentionally not read, and remote-code execution via include was not attempted.