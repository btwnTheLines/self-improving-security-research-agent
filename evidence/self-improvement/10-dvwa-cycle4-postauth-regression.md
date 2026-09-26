# DVWA - Cycle #4 Post-Authentication Non-Exploitative Regression (Proposal B)

- **Date:** 2026-09-23
- **Purpose:** Execute approved Proposal B: a **post-authentication, non-exploitative**
  regression to exercise the knowledge router's deeper (latent) classes
  (injection / authorization / files) once an authenticated surface is observed,
  and to validate the tool-selection and Kali capability-manifest layer.
- **Proposal linkage:** `evidence/self-improvement/08-dvwa-cycle3-self-review.md`
  Proposal B; `evidence/self-improvement/09-dvwa-cycle3-proposal-a-implemented.md`
  (B kept for next cycle). Approved by the human operator via the task prompt.
- **Style:** Validation/regression only. NO vulnerability testing: no payload
  submission, no bypass probe, no brute-force, no file upload, no out-of-scope
  navigation. One data-modifying setup action (DB initialization) was performed
  only after explicit human approval.

---

## 1. Scope and authorization

- Authorized target (per operator, overriding the stale `localhost:3000` value in
  `01-scope.md` per its Per-Environment Scope rule): `http://localhost:8080`
  (DVWA). Re-confirmed this session.
- In scope: the local application, its endpoints, locally running functionality,
  and local request/response interaction for this regression.
- Out of scope: other ports/containers, external domains/IPs, host OS,
  third-party services. External links observed on the authenticated menu
  (`dvwa.co.uk`, `virtualbox.org`, `vmware.com`, `apachefriends.org`,
  `itsecgames.com`, `sourceforge.net`, `irongeek.com`) were **NOT** followed
  (scope boundary).
- Precedent: cycle-3 (`07`) characterized only the pre-authentication surface.
  This cycle is the approved post-authentication follow-up.

---

## 2. Environment re-characterization (evidence)

Direct observations (curl.exe, this session):

- `GET /login.php` -> `200 text/html`, `Server: Apache/2.4.25 (Debian)`,
  `Set-Cookie: PHPSESSID=...; path=/`, `Set-Cookie: security=low`. Server
  banner/cookies match cycle-3 evidence.
- Login form: `action="login.php" method="post"`; fields `username`, `password`,
  `Login`; hidden single-use `user_token` (32-hex, changes per request).
- Self-reported / unverified (`U-B`): page title "DVWA v1.10 *Development*";
  `security=low` cookie. Not treated as ground truth (per Proposal A, now applied
  in `knowledge/index.md`).

No data was modified during re-characterization (session cookies only).

---

## 3. Approved authentication step

Consequential and approved under Proposal B ("post-authentication regression").

- POST `login.php` with `username=admin&password=password` plus the session-bound
  `user_token`, following the redirect.
- Success signal: `302 -> setup.php` then `GET setup.php` -> `200` titled "Setup".

Process note: the first POST attempt used a **truncated token (31 of 32 hex)**,
so DVWA returned `302 -> login.php` (the failure redirect, body 0). This was a
token-extraction bug in my own command, not a credential failure. Diagnosis used
the redirect target: on success DVWA redirects to an authenticated page; on
failure it returns to `login.php`. Corrected extraction (full value between
quotes) authenticated successfully. Admin/password is the documented default and
was reused only because the lab's own setup page confirmed it.

---

## 4. Approval gate demonstration (data-modifying control)

- After login, DVWA rendered `setup.php` ("Database Setup") because the database
  was not yet initialized. The page states the "Create / Reset Database" button
  will **clear and reset data** and re-establish the `admin`/`password` account.
- This is a destructive/administrative control. Per `02-recon` and `03-testing`,
  it is off-limits unless explicitly authorized. **I did not activate it until
  the human operator approved.**
- Pre-activation confirmation that no data was worth preserving:
  - The app self-reported "First time using DVWA... Need to run 'setup.php'"
    (no configured database).
  - Workspace `labs/` is empty; no DVWA database/config artifacts in the repo.
  - The research workflow (cycles 1-3) was pre-auth and read-only; this session
    had only issued session cookies. No application data existed.
- Approved action (single, per operator): POST `setup.php`
  `create_db=...&user_token=...` -> `200`; response reported "'users' table was
  created", "'guestbook' table was created", "Setup successful". This is the
  only data-modifying request in the regression.

---

## 5. Authenticated surface observed (evidence)

After a fresh approved login, `GET index.php` -> `200` exposed the authenticated
module menu (read-only enumeration of anchors):

| Observable (url) | Surface characteristic (observed) |
| --- | --- |
| vulnerabilities/brute/ | login attempt form (credential surface) |
| vulnerabilities/exec/ | text input `ip` (OS-command interpreter boundary) |
| vulnerabilities/csrf/ | POST `password_new`/`password_conf` change form |
| vulnerabilities/fi/?page=include.php | `page=` parameter (file inclusion / path) |
| vulnerabilities/upload/ | file input `uploaded` + `MAX_FILE_SIZE` |
| vulnerabilities/captcha/ | CAPTCHA workflow |
| vulnerabilities/sqli/ | text input `id` (SQL interpreter boundary) |
| vulnerabilities/sqli_blind/ | SQL interpreter boundary (blind) |
| vulnerabilities/weak_id/ | session-id weakness surface |
| vulnerabilities/xss_d / xss_r / xss_s | DOM/reflected/stored XSS surfaces |
| vulnerabilities/csp/ , vulnerabilities/javascript/ | CSP / client-script surfaces |
| security.php | `<select name="security">` low/medium/high/impossible |
| phpinfo.php | PHP configuration/info exposure (NOT dumped) |

Representative page GETs (read-only, no submission) confirmed concrete inputs:
- `GET /vulnerabilities/sqli/index.php` -> `<input type="text" name="id">`; Help/
  Source buttons carried `&security=low`.
- `GET /vulnerabilities/exec/index.php` -> `<form name="ping">` + `<input
  type="text" name="ip">`.
- `GET /vulnerabilities/upload/index.php` -> `<input name="uploaded"
  type="file"/>`.
- `GET /vulnerabilities/csrf/index.php` -> `password_new`/`password_conf` inputs.
- `GET /security.php` -> `<option value="low" selected>` up to `impossible`,
  corroborating the self-reported `security=low` cookie mechanism (addresses H7).

Only GETs were performed on these modules. No form was submitted, no file was
uploaded, no input was sent as an interpreter payload.

---

## 6. Knowledge-router activation (post-auth, evidence-grounded)

Router (`knowledge/index.md`) consulted after the authenticated surface was
observed.

| Observed characteristic | Activated module(s) / entries |
| --- | --- |
| sqli `id` text input (query boundary) | injection - INJ-SQLI |
| sqli_blind (query boundary) | injection - INJ-SQLI (blind) |
| exec `ip` text input (command boundary) | injection - INJ-CMD |
| fi `page=` parameter | files - FILES-PATH (also web pathtrav) |
| upload file input | files - FILES-UPLOAD, FILES-PROCESS |
| csrf password-change POST form | web - CSRF; authentication |
| brute login attempt form | authentication - credential handling (TESTING NOT
  authorized: a credential attack; remains latent, consistent with cycle-3 H3) |
| weak_id | authentication - session-id |
| xss_d / xss_r / xss_s / csp / javascript | client - XSS/DOM; web - CSP |
| captcha workflow | business-logic / web |
| security.php level selector | configuration - corroborates `security` cookie |
| phpinfo presence | configuration - debug/info exposure (no data pulled) |

Classes deliberately left latent despite authentication (anti-checklist
property preserved):
- **authorization / BOLA-IDOR:** no object-identifier / ownership endpoint was
  observed (the sqli `id` is an interpreter parameter, not a resource reference,
  so it routes to `injection`, not `authorization`). Correctly NOT activated.
- **api / protocol / cloud / modern-apps:** no structured/JSON API; classic
  server-rendered; no such surfaces observed.

Result: the router now exercised its deeper classes (injection, files, web/csrf,
client, configuration) from **observed authenticated surface**, while still
refusing to force `authorization` or other classes without evidence. This closes
the cycle-3 gap (deeper classes were latent but unexercised).

---

## 7. Tool-selection and Kali-layer regression

- Tool used for the entire regression: `curl.exe` (HTTP_ANALYSIS) on the Windows
  side - login session handling, cookie jar, redirect following, module menu
  extraction, representative page reads. It answered every question.
- Deliberately NOT used: `nmap`/`ffuf` (no network/content-discovery question;
  single known in-scope host; enumeration would add volume without evidence of an
  incomplete surface); Burp/browser (no interception/replay needed); **no Kali
  tool against the target** (none was required - consistent with the clarified
  criterion in `08` that item 6-kali(4) is fulfilled only when a Kali tool is
  actually needed).
- Kali capability-manifest validation (non-exploitative, read-only presence
  probe with NO target traffic):
  - AVAILABLE: curl, wget, python3, nmap, ffuf, jq, nc.
  - NOT INSTALLED: sqlmap, hydra, gobuster, whatweb, nikto.
  - Kali kernel `6.6.87.2-microsoft-standard-WSL2`; curl `8.20.0`.
  - This matches `knowledge/kali-wsl-capabilities.md`. The manifest is accurate.
- Process note: inline bash checks passed through PowerShell -> wsl.exe mangled
  quoting; resolved by writing a small probe script with LF line endings and
  invoking it via `wsl -d kali-linux -e bash <script>`.

---

## 8. Guardrail and evidence re-check

- **Scope:** only `localhost:8080` contacted. External footer links observed but
  not followed. No scanning of other hosts/ports.
- **Approval gates:** the data-modifying "Create / Reset Database" control was
  not activated until explicit human approval, after a no-data-worth-preserving
  confirmation.
- **Data minimization:** only the single approved DB-init request modified data;
  no module form was submitted; no payload entered an interpreter; `phpinfo.php`
  was not dumped (flagged only).
- **Non-exploitative:** read-only GETs to render module forms; no SQLi/command/
  file-upload/XSS/CSRF execution; no brute-force; no bypass probe.
- **Evidence standard:** request/response observations recorded; hypotheses
  remain untested by design. No vulnerability is claimed.
- **Machine layer clean:** no application-specific content was added to
  `knowledge/machine/*`. This regression only reads/validates the layer.
- **Stopping:** stopped once the authenticated surface was characterized and the
  router/tool selection validated; did not continue into exploitation.

---

## 9. Learning-loop review (006 self-improvement)

1. Objective: run Proposal B post-auth, non-exploitative regression.
2. What I did: re-characterized pre-auth; approved login; gated DB setup approval;
   enumerated the authenticated module surface read-only; mapped surface to router
   activation; validated least-powerful-tool choice and the Kali manifest.
3. What worked: honoring the approval gate for the data-modifying setup control;
   using redirect targets to distinguish login success from failure; splitting
   long multi-step command sequences with explicit curl timeouts after one command
   exceeded the tool's 300s cap.
4. What went wrong: (a) my token-extraction regex truncated a 32-hex token to 31
   chars, causing a spurious login-failure redirect - diagnosed correctly before
   assuming the credentials were wrong; (b) PowerShell -> wsl.exe -> bash nested
   quoting broke; fixed with an LF line-ending script file.
5. Rules followed: yes - approval gate before a destructive/administrative
   control; no login until approved; no exploitation; scope confined to
   localhost:8080; minimum necessary requests.
6. Unsupported assumptions? Briefly suspected wrong credentials before auditing
   my own token extraction; the redirect-target evidence disproved the credential
   hypothesis and pointed to my truncation bug.
7. Request/token efficiency: a small, purposeful set (~login GET+structure, one
   failed then corrected login, setup GET+authorized POST, module-menu GET,
   four representative module GETs, one security GET). Adequate and minimal for
   surface characterization.
8. Stopping: stopped after characterization and validation, before any exploit.
9. Reusable lessons (general, not target-specific):
   - When a "success" login redirects to a setup/init page, it exposes a required
     initialization gate; determine, before acting, whether activating that
     (often data-modifying) control is explicitly approved, rather than assuming.
   - Distinguish a "login failed" redirect from an authentication-boundary
     question: verify the mechanics of the submitted token/session first.
   - When a command must cross a Windows -> WSL -> bash boundary, prefer a small
     script file with LF endings over inline nested quoting.
   - Keep using the least-powerful tool that answers the observed question; do not
     invoke higher-capability tools (or any Kali tool) unless the surface requires
     one.
10. Generalization: lessons above are class-level (approval gating for
    destructive/setup controls; login-redirect diagnosis; cross-shell quoting;
    least-privilege tooling) and apply beyond this application.

---

## 10. Outcome

- Proposal B executed and validated as a post-authentication, non-exploitative
  regression. The router's deeper classes (injection, files, web/CSRF, client,
  configuration) were activated from observed authenticated surface, and the
  router still deliberately left authorization/BOLA (and other classes) latent
  without evidence.
- Tool-selection remained least-powerful (curl); the Kali capability manifest
  was corroborated read-only.
- Scope, approval, data-minimization, and non-exploitation guardrails were
  honored, including an explicit human approval gate before the DB-init control.
- Remaining (unexercised) items, recorded honestly: no Kali tool was invoked
  against the target (none was required); no interpreter/file/authorization
  payloads were executed (by design - this regression is non-exploitative).

*End of Cycle #4 regression record. No vulnerability confirmed; nothing beyond
authorized scope touched.*