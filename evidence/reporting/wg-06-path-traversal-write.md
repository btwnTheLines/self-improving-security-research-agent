# WG-06 — Path Traversal: Arbitrary File Write via Untrusted Filename

## 1. Title
Path Traversal — file upload stores input outside the intended directory via `../`

## 2. Summary
A file-upload handler uses a client-supplied name when constructing the storage path
without validating it against the intended directory. Putting `../` in the stored
name caused a file to be written outside the per-user upload location, demonstrating
arbitrary file write via path traversal.

## 3. Confirmation status
**Confirmed vulnerability**

## 4. Affected component
`POST /WebGoat/PathTraversal/profile-upload`, a profile-image upload handler. The
stored filename is taken from the submitted `fullName` field and joined to an
absolute per-user upload directory without canonicalization/sanitization.

## 5. Preconditions
- An authenticated session on the local target.
- Ability to submit an upload whose stored name contains path traversal.

## 6. Steps to reproduce
1. Establish an authenticated session (as the throwaway user).
2. Send a multipart upload to `/WebGoat/PathTraversal/profile-upload` with
   `fullName=../wgptmarker` and a small body.
3. Observe the response confirms the file was stored outside the intended directory.

## 7. Expected behavior
If the path-construction control were correct, the stored filename would be confined
to the user's own upload directory regardless of any `../` / `..\` / `/` in the input
(canonicalizing and re-validating the final path).

## 8. Actual behavior
With `fullName="../wgptmarker"` the handler stored the file outside the intended
per-user directory and the assignment completed (`lessonCompleted: true`). Controls:
- `fullName="..\\wgptmarker"` (backslash) → stored inside the user directory, did not
  complete.
- `fullName="../../wgptmarker.png"` → escaped one level too far (landed outside the
  application data dir), reported as "Nice try" — still confirming multi-level
  traversal was reached.

## 9. Security impact
Arbitrary (local) file write via path traversal: an unprivileged user can place files
outside the intended boundary on the WebGoat host. Depending on what the filename and
directory are made to target, this is the classic leading step toward integrity
compromise / latent file overwrite / (in broader configurations) code execution.

## 10. Evidence / PoC
Raw artifact: `evidence/reporting/raw/wg_pt_upload_escape.txt`

Request:
```
POST /WebGoat/PathTraversal/profile-upload HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: multipart/form-data; boundary=xWgB77

--xWgB77
Content-Disposition: form-data; name="uploadedFile"; filename="avatar.png"
Content-Type: image/png

wg-pt-marker-b2-traversal-write
--xWgB77
Content-Disposition: form-data; name="fullName"

../wgptmarker
--xWgB77--
```
Response:
```
{"assignment":"ProfileUpload","attemptWasMade":true,
 "feedback":"Congratulations. You have successfully completed the assignment.",
 "lessonCompleted":true,...}
```

## 11. Remediation
Canonicalize the combined path and confirm it stays under the intended root before
writing; never join user-controlled name fragments into a filesystem path without
validation. Use generated/sanitized filenames and explicit allow-lists.

## 12. Severity rationale
Path traversal (write) is a high-severity class; here demonstrated with a small,
clearly-marked file and confined to the lab filesystem. Impact is direct arbitrary
file-write within the WebGoat host boundary.

## 13. Limitations / remaining uncertainty
- The write was demonstrated as benign marker content; actual overwrite of an
  existing file or code-execution chaining was not performed.
- The written marker file (`..\wgptmarker` intent → landed outside the per-user
  directory) remains as a small lab artifact on the WebGoat host.
- The read-side traversal vector (query param) was container-blocked in this build
  ("Illegal characters are not allowed in the query params"), so the read variant
  was not exploitable via that parameter; this finding documents the write variant.
