# WG-03 — XXE: XML External Entity Resolution (File Read / SSRF Primitive)

## 1. Title
XML External Entity (XXE) — attacker-supplied XML resolves a `file://` external entity

## 2. Summary
An XML-parsing endpoint processes a client-supplied XML document with a `DOCTYPE`
that defines an external entity referencing a local file. The parser resolves the
entity, so an untrusted XML body can cause the server to read a local file. A benign
XML control without the entity does not trigger the behavior.

## 3. Confirmation status
**Confirmed vulnerability** (entity-processing/XXE). Content exfiltration into the
HTTP response was not observed on this build (see Limitations).

## 4. Affected component
`POST /WebGoat/xxe/simple` (`Content-Type: application/xml`), which parses an XML
`<comment>` document and reflects/processes its `<text/>` child, resolving entity
references inline.

## 5. Preconditions
- An authenticated session on `127.0.0.1:8080/WebGoat/`.
- Ability to set an XML `Content-Type` on the request.

## 6. Steps to reproduce
1. Establish an authenticated session.
2. Send:
   `POST /WebGoat/xxe/simple`
   `Content-Type: application/xml`
   ```
   <?xml version="1.0"?><!DOCTYPE comment [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><comment><text>&xxe;</text></comment>
   ```
3. Observe the assignment-completion response (the entity is processed).
4. Repeat with a benign body (`<comment><text>hello</text></comment>`) and observe it is rejected (control).

## 7. Expected behavior
If the parser were securely configured, the `DOCTYPE`/external-entity declaration
would be rejected or ignored, and an entity reference would never cause a server-side
file read.

## 8. Actual behavior
The weaponized body (file-reading external entity) completed the assignment
(`lessonCompleted: true`), while the benign control body was rejected
(`lessonCompleted: false`, "Sorry the solution is not correct"). The only
differential is the injected external entity, indicating the parser resolved it.

## 9. Security impact
XXE: an attacker who can submit XML can induce the server-side XML parser to read
local files from the WebGoat host (`file:///etc/passwd`), which is the classic XXE
file-read primitive. This is the same parser flaw that, depending on configuration,
can also yield internal SSRF or entity-based resource interaction.

## 10. Evidence / PoC
Raw artifacts:
- `evidence/reporting/raw/wg_xxe_simple.txt` (entity payload → completed)
- `evidence/reporting/raw/wg_xxe_simple_control.txt` (benign → rejected)

Request:
```
POST /WebGoat/xxe/simple HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: application/xml

<?xml version="1.0"?><!DOCTYPE comment [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><comment><text>&xxe;</text></comment>
```
Response: `{"assignment":"SimpleXXE","attemptWasMade":true,
"feedback":"Congratulations. You have successfully completed the assignment.",
"lessonCompleted":true,...}`

## 11. Remediation
Disable external entity and DTD processing in the XML parser (the class-level XXE
fix), and validate/sandbox any XML the application parses. Apply the same to any
downstream XML/DTD handling.

## 12. Severity rationale
XXE is a high-severity class when the entity is actually resolved (server-side file
read / SSRF potential). Reliability is high (deterministic payload vs. control). The
severity is bounded because the disclosure impact was demonstrated by entity
processing rather than by visible returned file content in this build.

## 13. Limitations / remaining uncertainty
- The file content was NOT reflected in this build's JSON response; the confirmed
  evidence is that the external-entity pointer was processed (grading succeeded only
  for the weaponized entity payload). Absolute file content exfiltration over HTTP
  was therefore not observed end-to-end.
- Reflecting endpoints in this build varied (`/xxe/json` absent; `/xxe/content-type`
  and `/xxe/simple4` present but did not return file content in the observed path).
- `/etc/passwd` was targeted as a canonical, minimal, single standard file; no
  volume of files was read.
