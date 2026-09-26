# Verification Recipe

> :warning: THIS RECIPE IS NOT PROOF OF A VULNERABILITY.
> It is an instruction sheet for a human to verify a finding the system
> believes is confirmed. A human must manually reproduce and validate the
> finding before it may be reported. This system never submits bug-bounty
> reports automatically.

## 0. Status banner
Status: **Instruction sheet only — NOT proof. Requires human manual verification.**

## 1. Recipe identification
- Recipe ID: WG-03-XXE-recipe
- Source finding: evidence/reporting/wg-03-xxe.md
- Confirmation status: Confirmed vulnerability
- Generated on: 2026-09-26
- Generator version: 1.0.0

## 2. Finding and vulnerability class
Injection (XML External Entity, XXE) — external entity resolved to a local file read primitive

## 3. Target endpoint/surface
POST /WebGoat/xxe/simple (Content-Type: application/xml), parses a client-supplied XML <comment> document and resolves entity references inline

## 4. Preconditions and required authorization
- An authenticated session on 127.0.0.1:8080/WebGoat/ within the authorized lab boundary only.

- Ability to set an XML Content-Type on the request.

- Scope: only 127.0.0.1:8080/WebGoat/. No external hosts, WebWolf, or other ports.

## 5. Exact reproduction steps
- Establish an authenticated session to the WebGoat app.

- Send the weaponized XML body below to /WebGoat/xxe/simple with Content-Type: application/xml.

- Observe the response: the assignment completes (lessonCompleted: true), indicating the external entity was processed.

- Repeat with the benign control body, observe it is rejected (lessonCompleted: false).

- Record both the probe and the control response exactly.

## 6. Minimal test input/request
```
POST /WebGoat/xxe/simple HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: application/xml

<?xml version="1.0"?><!DOCTYPE comment [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><comment><text>&xxe;</text></comment>
```

## 7. Benign control test
Same endpoint with a benign body that declares no external entity:
<comment><text>hello</text></comment>
Expected control outcome: rejected (lessonCompleted: false), isolating the injected external entity as the only differential cause of the vulnerable behavior.

## 8. Expected vulnerable vs. safe behavior
If the parser resolves external entities, the weaponized body completes the assignment (file-read primitive), while the benign control is rejected.

If the parser were securely configured, DOCTYPE/external-entity declarations would be rejected or ignored and the weaponized entity would not complete the assignment.

## 9. Evidence to capture
What to capture:
- Full request and response for the weaponized payload (status line, headers, body).

- The lessonCompleted/feedback JSON fields in the response.

- Full request and response for the benign control (must reject).

- Only WebGoat's own synthetic data and the single canonical /etc/passwd file; no volume of files.
Referenced raw evidence (existing, preserved separately):
- `evidence/reporting/raw/wg_xxe_simple.txt`
- `evidence/reporting/raw/wg_xxe_simple_control.txt`

## 10. Safety limits and stop conditions
- Within 127.0.0.1:8080/WebGoat/ only; no external/outbound requests at any point.

- No DoS, no destructive actions, no resource exhaustion.

- Do not read a large volume of files; the single canonical /etc/passwd demonstrates the primitive.

- STOP if the entity resolution causes any outbound connection to a system outside the WebGoat boundary.

- STOP as soon as sufficient evidence (entity-resolved / control-rejected) has been captured.

- STOP rather than attempting to exfiltrate large or unrelated files.

## 11. Cleanup requirements
- No persistent data is created by this probe; any temporary session files used during reproduction should be cleared.

- Verify no unexpected artifacts were written on the WebGoat host.

## 12. Reporting notes
Frame at class level (XML parser resolves external entities → file-read / SSRF primitive). Note in the report the limitation that absolute file-content exfiltration into the HTTP response was not observed in this build; the confirmed evidence is that the external-entity pointer was processed (weaponized-only grading success with a rejected benign control).
