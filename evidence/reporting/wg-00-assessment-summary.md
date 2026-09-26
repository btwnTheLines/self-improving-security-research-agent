# WG-00 — WebGoat Full-Capability Assessment: Summary & Self-Review

Target: `http://127.0.0.1:8080/WebGoat/` (isolated local range). Assessment performed
with broad authorized active testing confined to that single service (see
Boundary/Authorization section). Reports are class-level and evidence-backed against
raw artifacts under `evidence/reporting/raw/wg_*`.

## 1. Comprehensive assessment summary

Characterized the application as an authenticated, server-rendered lesson framework
(39 menu lessons) with `*.lesson` pages and assignment endpoints under
`/WebGoat/<Lesson>/<action>`. Method mix: mostly `POST`, some `GET`, one `PUT`.
Formed hypotheses per the knowledge router from observed surface characteristics and
tested the highest-value distinct classes. Six (6) findings were **confirmed** with
request/response evidence. Several surfaces were recorded as negative results or
un-assessable within scope (details below).

Test method applied throughout: benign markers, controlled in-scope objects, minimal
payloads, and a control/differential where possible. No external traffic, no
destructive actions, no DoS.

## 2. Confirmed findings

| # | Class (router) | Surface | Confirmed impact | Report |
|---|----------------|---------|------------------|--------|
| 1 | injection (SQLi) | `SqlInjection/attack8` | Data read: dumped entire internal user table (incl. salary + auth-token cols) | `wg-01-sql-injection.md` |
| 2 | authorization (function-level) | `access-control/users` (addUser) | Broken function-level AC: non-admin invokes admin function, `admin:true` honored → privilege escalation primitive | `wg-02-missing-function-level-ac.md` |
| 3 | injection (XML/XXE) | `xxe/simple` | XXE: `file:///etc/passwd` external entity resolved by the XML parser (control rejected) | `wg-03-xxe.md` |
| 4 | web (open redirect) | `OpenRedirect/task1` | Redirect to arbitrary external URL accepted ("external host accepted") | `wg-04-open-redirect.md` |
| 5 | client (XSS sink) | `CrossSiteScripting/attack5a` | Attacker `<script>` markup emitted unencoded into HTML output (XSS sink) | `wg-05-xss-stored-reflected.md` |
| 6 | files (path traversal) | `PathTraversal/profile-upload` | Arbitrary file write outside intended directory via `../` in stored name (controlled differential) | `wg-06-path-traversal-write.md` |

## 3. Exploitation / impact demonstrated for each

1. SQLi — full table dump returned in `output`; grader explicitly states
   "compromised the confidentiality of data by viewing internal information".
2. Function-AC — non-admin session served the admin `addUser` handler and the server
   honored a client-supplied `admin:true` (and `admin:false` control).
3. XXE — weaponized DOCTYPE/entity payload processed (assignment completed) vs benign
   control rejected → the parser resolves external entities (file-read primitive).
4. Open redirect — application returned a redirect target to an attacker-chosen
   external host; internal-host control did not complete.
5. XSS sink — the injected `<script>alert(1)</script>` was returned as live markup,
   unencoded, inside the rendered HTML context.
6. Path-traversal write — `../` escaped the per-user directory (completed); `..\`
   (blocked) and `../../` (one level too far) served as controls.

## 4. Unconfirmed hypotheses

- **IDOR cross-user READ via direct object reference** (`IDOR/profile/{userId}`):
  server-side ownership check enforced — request to another user's id returned a
  "try a different id"/rejection, i.e., the read vector was **gated** (negative).
  Observed instead: the own-profile response **leaks** server attributes `userId` and
  `role` not shown in the UI (mass-assignment / info-leak observation, not a
  confirmed separate finding).
- **JWT privilege escalation via token forgery**: the app embeds two of its own
  example JWTs in form-action query strings (info-disclosure observation). A clean
  forged-token privilege escalation was not completed because the required
  key-handling flow depends on out-of-scope WebWolf; left as an unassessed surface.
- **CSRF**: systemic absence of anti-CSRF tokens on assignment POSTs is confirmed,
  and the session cookie has **no `SameSite` and no `Secure`** flag. However, the
  concrete security-sensitive cross-site state change (message endpoint is JSON-only
  → preflight-gated) was not proven end-to-end, so CSRF is recorded as a
  confirmed weak-protection observation with only minor demonstrated impact.
- **SSRF**: the `SSRF/task1` endpoint merely echoes the URL into an `<img src>`
  (stub; no server-side fetch of the supplied URL observed). `task2` instructs
  fetching an **external** host (`ifconfig.pro`) which is outside the hard boundary;
  therefore SSRF was **not** exercised in a way that could be confirmed and was
  classed as un-assessable/stub.
- **Password reset host-header injection / account takeover**: the reset-link endpoint
  is functional ("e-mail sent") but does not disclose the token in the HTTP response,
  and the full token/email chain is handled through the out-of-scope WebWolf mailbox;
  not confirmed.

## 5. Attack surfaces assessed

- SQLi data read + variant; SQLi login/advanced (register) partially.
- Function-level AC (admin add-user, list-users, config, fixed variants).
- IDOR read (gated) + own-profile attribute leak.
- XXE (simple, control).
- Open redirect (task1, control).
- Reflected/stored XSS guestbook sink.
- Path traversal (write upload; read variant container-blocked).
- CSRF token/session-cookie posture.
- JWT example-token exposure in markup (observation).
- Password reset link generation.
- SSRF task1 stub.

## 6. Important surfaces not assessed and why

- **JWT forgery / privilege escalation**: depends on WebWolf (out of scope).
- **Password-reset full chain / host-header takeover**: token delivery via WebWolf
  (out of scope).
- **SSRF task2**: requires fetching an external host (out of scope).
- **Insecure Deserialization, ZIP-Slip, cryptography, challenges**: not attempted to
  avoid time/risk and because they either require file/state manipulation or are
  lower-value than the six confirmed classes; ZIP-Slip would be a further files-class
  variant of the same traversal theme.
- **WebWolf, other ports/hosts**: out of scope by the hard boundary.

## 7. Reports generated

- `evidence/reporting/wg-00-assessment-summary.md` (this file)
- `evidence/reporting/wg-01-sql-injection.md`
- `evidence/reporting/wg-02-missing-function-level-ac.md`
- `evidence/reporting/wg-03-xxe.md`
- `evidence/reporting/wg-04-open-redirect.md`
- `evidence/reporting/wg-05-xss-stored-reflected.md`
- `evidence/reporting/wg-06-path-traversal-write.md`

(All `wg-` prefixed to avoid collision with the pre-existing DVWA set `00–09,99`.)

## 8. Evidence locations

- Reports: `evidence/reporting/wg-*.md`
- Raw requests/responses: `evidence/reporting/raw/wg_*.txt`
- Recon/map (prior phases): `evidence/recon/webgoat-*.md`, `work/lesson_endpoint_map.json`
- Helper/scripts: `work/webgoat_helper.py`, `work/wg_helper_raw.py`, `work/wg_test_*.py`

## 9. Tool usage and significant tool failures

- Tools: custom Python `urllib`/`http.client` HTTP helpers (no browser/Burp needed for
  these classes). Used raw HTTP to override `Host`.
- Failures/notes: the `path_traversal.js` forms and the `/xxe/json` endpoint are
  missing/absent in this build; PowerShell multiline/escaping issues interfered with
  one one-off command (recovered by using Python for parsing). The `random-picture`
  query traversal was blocked at the container level. No material coverage loss
  beyond documented items.

## 10. Boundary / authorization compliance assessment

All requests were directed at `127.0.0.1:8080/WebGoat/*` only.
- No traffic to the public Internet, other localhost ports, downloads, or WebWolf.
- The external redirect and XXE/local file were only **read** data already served by
  the WebGoat app / its own host; no outbound request was made to external hosts
  (the open-redirect target was returned by the app, not followed).
- `restartlesson.mvc` and any destructive/global-reset/admin controls were **not**
  invoked.
- State changes performed: created admin/non-admin lab user records and wrote a small
  labeled marker file (path-traversal proof) — all benign, in-range, and purposive to
  validate findings. No `.clinerules/` or `knowledge/` files were modified.
- Data touched: only WebGoat's own synthetic lesson data and one canonical
  `/etc/passwd` file read via the XXE primitive; no unrelated host/webgoat data was
  pulled.

## 11. Generalized self-improvement proposals

- When an XML parser is confirmed to resolve external entities, look for a
  response-delivering reflection/error endpoint before recording full file
  exfiltration; entity-resolution alone confirms the class but not content disclosure.
- When a target's "SSRF"/"redirect" lesson turns out to only echo a URL into markup
  rather than performing a server-side fetch, classify it as a stub and avoid
  conflating echo with genuine SSRF (anti-false-positive discipline).
- Check session-cookie flags (`SameSite`/`Secure`) when assessing CSRF, so conclusions
  about cross-site-exploitable state changes are grounded in browser policy.
- For path traversal, test the read and write vectors separately and treat
  container-level query-string filtering (`Illegal characters...`) as a distinct
  control layer from application path-construction.
- Before testing host/gate-dependent flows, enumerate which delivery channels
  (mailbox/WebWolf/metadata endpoints) are in-scope, to avoid committing to an
  un-assessable chain.

### Note on lab artifacts

No destructive or widely-scoped data changes. A few benign, labeled artifacts remain
in the lab: user records `wgatmpwnA1`/`A2`, guestbook marker `wg-xss-marker-a1`, and
a small traversal-write marker on the WebGoat host. These are flagged here rather
than relied upon as findings.
