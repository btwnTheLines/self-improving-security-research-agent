# DVWA - Post-Knowledge-Layer Validation

Date: 2026-09-22
Purpose: Evaluate whether the newly implemented `knowledge/` layer improves
adaptive reconnaissance, security-surface identification, hypothesis
generation, tool selection, and reasoning versus prior DVWA recon behavior.

Scope of this artifact:
- Validation of the workflow, NOT vulnerability testing.
- No exploitation, no authentication attempts, no bypass probes.
- Authorized target only: `http://localhost:8080`.

--------------------------------------------------------------------------------
## 1. Scope confirmation
--------------------------------------------------------------------------------

- Authorized target (per operator in the current task, overriding the stale
  `localhost:3000` in `01-scope.md` per its Per-Environment Scope rule):
  `http://localhost:8080`.
- In scope: this application, its endpoints, its locally running functionality,
  local request/response interaction during validation.
- Out of scope: other ports/services/containers, external domains/IPs, the host
  OS, third-party services.
- A footer link to an external domain (`www.dvwa.co.uk`) was observed but NOT
  followed (scope boundary).

--------------------------------------------------------------------------------
## 2. Environment characterization (evidence)
--------------------------------------------------------------------------------

Observation (direct request/response, this session):
- `GET /` -> `HTTP/1.1 302 Found`, `Location: login.php`, `Set-Cookie:
  PHPSESSID=...; path=/`, `Set-Cookie: security=low`, `Server:
  Apache/2.4.25 (Debian)`, `Content-Type: text/html; charset=UTF-8`.
- `GET /login.php` -> `200 OK`, server-rendered XHTML login page: a `POST` form
  to `login.php` with `username`, `password`, submit button `Login`, and a
  hidden single-use `user_token` (anti-CSRF token that changes between
  requests).
- `GET /robots.txt` -> `200`, `User-agent: *` / `Disallow: /`.
- `GET /nonexistent-9f3k.aspx` -> `404 Not Found`, Apache default error page,
  `text/html; charset=iso-8859-1`, bare `<h1>Not Found</h1>` (not a JSON or SPA
  response), body discloses `Apache/2.4.25 (Debian) Server at localhost Port
  8080`.

Architecture determination (OBSERVED, not assumed):
- Application type/architecture: classic server-rendered web application
  (PHP + Apache), gated behind a session-based authentication flow. Evidence:
  server-generated XHTML, `PHPSESSID` cookie, `.php` script handling, and the
  404 for an unknown path returning Apache's default HTML (no SPA fallback).
- Interface paradigm: HTML form `POST` (application/x-www-form-urlencoded);
  no JSON/GraphQL/API observed on the pre-auth surface.
- Content types: `text/html` (app pages), `text/plain` (robots.txt), plus
  self-referenced static assets (`dvwa/css/login.css`,
  `dvwa/images/login_logo.png`).
- Input surfaces (pre-auth): only the login form fields `username` and
  `password` (plus the `user_token` hidden field). No other interpreter-facing
  input is reachable pre-authentication.

Self-reported vs observed configuration (U-B):
- OBSERVED directly: server banner `Apache/2.4.25 (Debian)`; presence of
  `PHPSESSID` and `security` cookies; form structure and fields.
- SELF-REPORTED / UNVERIFIED (flagged, not treated as ground truth):
  - Page title "Damn Vulnerable Web Application (DVWA) v1.10 *Development*".
  - The `security=low` cookie value, which implies an application security-level
    mechanism whose real effect is not corroborated.

Vantage/availability note: the target was initially unreachable (connect
refused) and was only reachable after the operator confirmed/started the
instance; earlier probing produced only `http_code=000` and was not treated as
an attack surface.
--------------------------------------------------------------------------------
## 3. Authentication / session observations
--------------------------------------------------------------------------------

- Session model: cookie-based `PHPSESSID` (PHP session). A session cookie is
  issued on an unauthenticated `GET /` and `GET /login.php` (prior to any
  credential submission).
- Cookie attributes observed: `PHPSESSID` sent with `path=/`; **no
  `HttpOnly`** attribute observed in the response header; `Secure` is not set
  (moot for cleartext localhost, but notable). Both the `PHPSESSID` and
  `security` cookies are set by the application.
- Login form: single-realm credential form (`username`/`password`) plus a
  hidden single-use `user_token` (anti-CSRF token), suggesting some CSRF
  awareness on the login action.
- No other authentication flows (registration, password reset, MFA) were
  reachable or observed on the pre-auth surface.

U-A discipline: The reachable pre-authentication surface was characterized
completely (root redirect, login form, robots.txt, 404 behavior, session cookie
issue). Authentication-gated areas (any authenticated modules/functions,
post-login navigation) are recorded as explicit UNKNOWNS; their presence was not
confirmed and they were not enumerated.

--------------------------------------------------------------------------------
## 4. Functional surface (pre-auth)
--------------------------------------------------------------------------------

Reachable, observed:
- `GET /` -> redirect to `login.php`.
- `GET /login.php` -> login form (rendering + anti-CSRF token issuance).
- Static assets referenced by the login page (`dvwa/css/login.css`,
  `dvwa/images/login_logo.png`).
- `GET /robots.txt`.

Not reachable / unknown (auth-gated or not confirmed):
- Any authenticated application functionality after login.
- Any files/upload, API, messaging, or workflow surfaces beyond the login form.
- Any object-identifying endpoints (none observed).

Content discovery was intentionally NOT run (see tool-selection reasoning).
--------------------------------------------------------------------------------
## 5. Request / response observations
--------------------------------------------------------------------------------

| Request | Response (observed) | Notes |
| --- | --- | --- |
| `GET /` | 302 -> login.php; PHPSESSID + security=low cookies | session issued pre-auth |
| `GET /login.php` | 200 text/html, server-rendered login form | single-use user_token; changes per request |
| `GET /robots.txt` | 200 text/plain, Disallow: / | minimal disclosures |
| `GET /nonexistent-9f3k.aspx` | 404, Apache default HTML | confirms server-rendered, discloses server banner+path |

No page content was stored or retained; only headers and small sampled bodies
were examined. Cookies from private sessions were held in a temporary cookie jar
used only for this validation and cleaned up.

--------------------------------------------------------------------------------
## 6. Security-relevant observations
--------------------------------------------------------------------------------

- No `HttpOnly` flag on `PHPSESSID` in the observed response.
- No `X-Frame-Options`, `Content-Security-Policy`, or `X-Content-Type-Options`
  observed on the login page response.
- Anti-CSRF token (`user_token`) present on the login form.
- Server banner and full server/path info disclosed by the default 404 page.
- A `security=low` cookie set by the application (self-reported; real effect
  unverified).
- `robots.txt` disallows all crawling (`Disallow: /`), which is non-disclosing
  (does not reveal paths).

These are header/behavioral observations. None constitute a confirmed
vulnerability.

--------------------------------------------------------------------------------
## 7. Knowledge-router activation (evidence-grounded)
--------------------------------------------------------------------------------

Router (`knowledge/index.md`) was consulted only after surface observation. On
the observed pre-auth evidence, it activated:

| Observed surface characteristic | Activated module(s) |
| --- | --- |
| auth/session flow, login form, session cookie | authentication |
| CSRF-relevant login POST, hidden token | web (CSRF) |

Cross-cutting: login credential fields also place `injection`/`authentication`
on the border, but because this is an authentication boundary (not an arbitrary
interpreter input) and recon forbids login/probing, it is recorded as latent,
not tested.

Deliberately NOT activated (no supporting evidence pre-auth):
- `authorization` / BOLA-IDOR (no object identifiers observed),
- `api` (no structured/JSON interface observed),
- `files` (no upload/download observed),
- `business-logic` (no multi-step workflow observed),
- `modern-apps` (server-rendered, not SPA),
- `protocol`, `cloud` (no relevant surface).

This run exercised the router's anti-checklist property: it did not pull in
`injection`/`authorization` merely because a web form or a "security" cookie
exists; it requires observed evidence.
--------------------------------------------------------------------------------
## 8. Evidence-grounded hypotheses (candidate list - NONE tested)
--------------------------------------------------------------------------------

Pre-auth reachable (observation-level / low-risk to later verify):

- H1 (authentication / session flags): Session cookie `PHPSESSID` is issued
  pre-auth without an `HttpOnly` flag; if any XSS exists anywhere in the app, a
  session-theft path could be relevant. Evidence: observed `Set-Cookie` header.
  Status: header observation only; not an exploit.

- H2 (web / CSRF): The login action carries an anti-CSRF `user_token`,
  suggesting CSRF awareness on this action. Hypothesis: token protection against
  state-changing requests may or may not be applied consistently to
  authenticated actions. Status: UNTESTED (requires authentication).

- H3 (authentication / credential handling): No account-lockout mechanism was
  observable pre-auth. Brute-force-resistance is unknown. Status: UNKNOWN;
  further probing is a credential attack / availability-adjacent and is NOT
  authorized at this stage.

Auth-gated / latent (candidates requiring approval; NOT tested):

- H4 (injection): IF an authenticated function accepts user input consumed by an
  SQL / OS / template interpreter, then interpreter-injection classes apply
  (SQL injection, command injection, template/expression injection). No such
  interpreter input is observed pre-auth, so this remains latent and gated on
  future observed surface + approval.

- H5 (authorization / BOLA): IF an authenticated function exposes object
  identifiers without consistently enforced ownership checks, then
  horizontal/vertical access-control issues could apply. No object identifiers
  observed pre-auth; latent, gated on future evidence + approval.

- H6 (files): IF authenticated file upload/processing surface exists, file
  handling classes apply. Not observed pre-auth; latent.

- H7 (configuration): The `security=low` cookie is self-reported configuration
  whose real effect (e.g., whether it alters input-handling behavior or is
  merely nominal) is unverified. Corroboration would be required and is not
  attempted here.

None of H1-H7 were investigated during this validation (no fingerprint/condition
tests). They are hypotheses only; none is a confirmed vulnerability.
--------------------------------------------------------------------------------
## 9. Tool-selection reasoning (least-powerful tool)
--------------------------------------------------------------------------------

- Chosen: `curl.exe` (HTTP_ANALYSIS). It fully answered the characterization
  questions (headers, redirects, cookies, body structure, error behavior). No
  other tool was needed.
- Deliberately NOT used:
  - `nmap` (SERVICE_DISCOVERY) - no network/service discovery question; the only
    authorized target is a single known port already being queried with HTTP.
  - `ffuf` (CONTENT_DISCOVERY) - content fuzzing would add request volume without
    evidence that the pre-auth surface is incomplete; no approval/license for
    boundary-less enumeration; not needed to characterize the surface.
  - Burp / browser - no interception/replay/modification question pre-auth.
  - No Kali-side network utilities - nothing to do outside the single HTTP
    target, and tool presence does not imply authorization.
- Balance: requests were limited to the minimal set that characterized the
  surface (root, login page, robots.txt, one 404 probe). No page was downloaded
  wholesale; only headers + small body samples were inspected.

--------------------------------------------------------------------------------
## 10. Unknowns and uncertainties
--------------------------------------------------------------------------------

- The exact full set of authenticated functions/endpoints (auth-gated; U-A
  role).
- Whether any object-identifier, file, API, or workflow surface exists beyond
  the login form.
- Real-world effect of the `security=low` cookie (self-reported, unverified).
- Whether the observed anti-CSRF token is present/consistent across
  authenticated actions.
- Whether application behavior (e.g., input validation) is uniform or varies by
  security-level/cookie.
- The application's identity (`DVWA v1.10 *Development*`) is self-reported; it
  was not assumed to imply specific endpoints or fixes, and no known-vuln
  knowledge was used.
--------------------------------------------------------------------------------
## 11. Self-review of the knowledge-layer validation
--------------------------------------------------------------------------------

Did the knowledge router activate relevant concepts?
- Yes. From observed auth/session + CSRF-token evidence it activated
  `authentication` and `web` (CSRF) and cross-links. Evidence: Sections 2, 3, 7.

Did it avoid irrelevant vulnerability classes?
- Yes. It did not drag in `injection`/`authorization`/`api`/`files`/
  `business-logic`/`modern-apps`/`protocol`/`cloud` pre-auth because none had
  observed evidence (Section 7 "deliberately NOT activated"). It confirmed the
  router's anti-checklist property rather than forcing every module.

Did it reduce unsupported assumptions?
- Yes. Environment characterization was derived from observed requests/responses
  (server banner, cookies, form structure, 404 behavior), and self-reported
  facts (version, `security=low`) were explicitly flagged as unverified (U-B).
  No assumed framework, auth mechanism, endpoint, or known-vulnerability list was
  imported.

Did it improve hypothesis provenance?
- Yes. Every hypothesis (H1-H7) is tied to a stated observation or a clearly
  labeled general principle, and consequential ones (injection/authorization/
  files) were explicitly gated on future observed surface + approval. No
  hypothesis was transplanted from a prior app or from a "known DVWA endpoint"
  list.

Did it improve tool selection?
- Yes. `curl.exe` alone answered the characterization; higher-power tools
  (nmap/ffuf/Burp) were explicitly evaluated and bypassed because they answered
  no current question (Section 9).

Did it avoid unnecessary requests/actions?
- Yes. A small, purposeful request set (4 requests) characterized the pre-auth
  surface; no content fuzzing, no asset downloading beyond small samples, no
  repeated probes, and no setup/destructive control was even requested.
Did it preserve all existing safety and approval controls?
- Yes. No exploitation, no auth/login, no bypass probe, no state-changing POST,
  no out-of-scope navigation (external footer link not followed), no fuzzing,
  and all consequential hypothesis-areas (H4-H7) were recorded as requiring
  approval rather than tested. Scope confirmed to the single authorized target.

What appears genuinely improved vs prior DVWA recon?
- Router-driven class selection with explicit "not activated" reasoning (prior
  recon engaged a broader surface pattern; here the router kept modules latent
  without evidence).
- Stronger observation/inference/provenance discipline backed by the router
  cross-cutting rules (auth+session, identifiers->authorization, etc.).
- Deliberate non-use of discovery scanning tools (explicit tool-selection
  reasoning that avoids request volume).

What still appears weak or inefficient?
- The login page itself self-reports the application identity, which carries
  prior-app bias risk; the router guidance did not itself pre-empt that, but
  U-B flagging handled it. This shows the human/operator framing, not the router,
  still carries the main anti-assumption load for strongly branded apps.
- Pre-auth recon is inherently shallow (nothing beyond a login gate), so the
  router's deeper classes are unexercised; a post-auth validation is required to
  truly stress selection of the cutting classes (injection/authorization/files).

What evidence supports each conclusion?
- Each claim above is supported by the recorded request/response observations in
  Sections 2-5 and the router mapping in Section 7, with hypotheses and their
  status in Section 8. No claim rests on an executed exploit; all consequential
  hypotheses remain untested and labeled as such.