# WG-05 — Stored/Reflected XSS: Unencoded Attacker Markup in HTML Output

## 1. Title
Cross-Site Scripting (XSS) sink — attacker-supplied `<script>` markup is emitted
unencoded into an HTML rendering context

## 2. Summary
A message/guestbook-style endpoint takes attacker-controlled text and embeds it into
the application's HTML serialization without HTML-encoding or sanitization. A
`<script>alert(1)</script>` payload was returned inside the page output as live markup,
i.e. an XSS sink that executes attacker-controlled script in a victim's browser when
rendered.

## 3. Confirmation status
**Confirmed vulnerability** (XSS sink / improper output encoding). Browser execution
was not observed over HTTP (see Limitations).

## 4. Affected component
`GET /WebGoat/CrossSiteScripting/attack5a` (assignment `CrossSiteScriptingLesson5a`),
parameters `field1`/`field2` (guestbook / "shopping receipt" context). The server
stores and reflects these values into generated HTML.

## 5. Preconditions
- An authenticated session on the local target.
- Ability to supply markup in `field1`.

## 6. Steps to reproduce
1. Establish an authenticated session.
2. Send:
   `GET /WebGoat/CrossSiteScripting/attack5a?QTY1=1&QTY2=1&QTY3=1&QTY4=1&field1=%3Cb%3Ewg-xss-marker-a1%3C%2Fb%3E%3Cscript%3Ealert(1)%3C%2Fscript%3E&field2=111`
3. Observe that the response output contains the literal `<script>alert(1)</script>`
   markup (only `/` JSON-escaped), not an HTML-encoded form such as `&lt;script&gt;`.

## 7. Expected behavior
If output encoding/sanitization were correct, attacker-supplied `<`/`>` would be
HTML-escaped (`&lt;script&gt;`) so the browser renders them as inert text, never as
executable markup.

## 8. Actual behavior
The `output` field contained the injected HTML as live markup:
```
...We have charged credit card:<b>wg-xss-marker-a1</b><script>alert(1)</script>...
```
The assignment completed specifically because the injected `<script>` was treated as
executable markup, confirming the sink.

## 9. Security impact
Stored/reflected XSS: an attacker can cause script of the attacker's choice to run in
the browser context of any user who views this output (session theft, UI redressing,
credential capture). This is the client-side injection class triggered by insecure
output handling.

## 10. Evidence / PoC
Raw artifact: `evidence/reporting/raw/wg_xss_guestbook.txt`

Request:
```
GET /WebGoat/CrossSiteScripting/attack5a?QTY1=1&QTY2=1&QTY3=1&QTY4=1&
   field1=%3Cb%3Ewg-xss-marker-a1%3C%2Fb%3E%3Cscript%3Ealert(1)%3C%2Fscript%3E&field2=111
```
Response (abridged):
```
{"assignment":"CrossSiteScriptingLesson5a","attemptWasMade":true,
 "feedback":"Congratulations, but alerts are not very impressive...",
 "lessonCompleted":true,
 "output":"...charged credit card:<b>wg-xss-marker-a1</b><script>alert(1)</script>..."}
```

## 11. Remediation
Context-aware, safe output encoding for every user-controlled value (HTML-encode in
HTML contexts), and input/sanitization as defense-in-depth. Never emit user content
into an HTML context without encoding.

## 12. Severity rationale
XSS is a high-impact client-side class (script execution in the victim's session).
Deterministic sink demonstrated; severity is standard for a reflected/stored XSS sink
in an application with authenticated session cookies lacking other protections.

## 13. Limitations / remaining uncertainty
- Only the **sink** (unencoded reflection/storage into HTML) is evidenced over HTTP.
  Actual script *execution* in a browser was not observed (no browser automation
  available in the toolset), so we document the sink rather than a completed
  exploit chain.
- The payload was a benign, self-referential marker (`alert(1)` with no external
  callout) and was stored/reflected within the lab UI.
