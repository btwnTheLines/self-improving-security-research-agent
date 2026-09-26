# WebGoat — Pre-Authentication Reconnaissance (Current Environment)

- Date: 2026-09-26
- Status: Recon / pre-auth surface characterization. No exploitation, no account
  registration, no login attempted during this phase.
- Rules observed: `.clinerules/00-core.md`, `01-scope.md`, `02-recon.md`,
  `03-testing.md`, `05-reporting.md`; knowledge router `knowledge/index.md`.

## 1. Authorized target (per-environment scope decision)

- **Target:** `http://127.0.0.1:8080/WebGoat/` — OWASP WebGoat, locally controlled,
  intentionally vulnerable training application.
- The stored `01-scope.md` carries no hardcoded target; per "Per-Environment Scope"
  scope is set per environment and not inherited from prior engagements
  (Juice Shop was `:3000`, DVWA was `:8080`). The operator's ongoing WebGoat task
  plus loopback identification establish the current target.
- Identification evidence: `GET /` on `127.0.0.1:8080` returns Tomcat default 404
  (`HTTP Status 404 – Not Found`); `GET /WebGoat/` returns `<title>Login Page</title>`
  (Spring/Thymeleaf HTML). `127.0.0.1:9090` (WebWolf) is not listening → not reachable
  this session; treated as out of reach / unknown rather than assumed.
- IN SCOPE: `127.0.0.1:8080` WebGoat application and its HTTP/API endpoints. No
  external IP, no public website, no other container.

## 2. Tooling limitation (recorded)

- The **Sail Research `run_commands` tool** failed schema validation on the
  `/commands` argument (`/properties/commands/type`). This is an interface/tooling
  failure, **not** evidence about the target. It was **not** re-attempted with the
  same malformed call (per operator instruction).
- Recon continued using the least-powerful available local tools already present:
  Windows PowerShell + Python 3.14 stdlib `urllib` against loopback only. No
  software was installed and no configuration was modified to work around the
  failure.
- Implication: some automation convenience was lost; this does not change the
  security surface or the evidence standard.

## 3. Method (least-powerful tool)

- Read-only `GET` requests to in-scope loopback paths only.
- Raw artifacts saved under `evidence/reporting/raw/`:
  - `webgoat_login.txt` — `GET /WebGoat/login` full body + headers.
  - `webgoat_registration.txt` — `GET /WebGoat/registration` full body + headers.
- Scratch probe scripts retained under `work/`.

## 4. Observed pre-authentication surface (mapped fully where reachable)

Reachable without a session:

| Path | Method | Behavior observed |
| --- | --- | --- |
| `/WebGoat/` | GET | Renders Login Page (200). |
| `/WebGoat/login` | GET | Login form `POST /WebGoat/login`; fields `username`, `password`. No `Set-Cookie` on GET; no CSRF field in form. |
| `/WebGoat/registration` | GET | Registration form `POST /WebGoat/register.mvc`; fields `username`, `password`, `matchingPassword`, `agree`. No visible CSRF field. |
| `/WebGoat/start.mvc`, `/WebGoat/logout` | GET | Return Login Page when unauthenticated (client-side gate; not an HTTP redirect). |
| `/` (other) | GET | Tomcat default 404. |
| `/WebGoat/css/*`, `/WebGoat/plugins/*`, `/WebGoat/css/img/favicon.ico` | GET | Static assets referenced by pages. |

Headers observed (no `Server:` / `X-Powered-By`): `Content-Type: text/html;charset=UTF-8`,
`Content-Language: en-US`, `Transfer-Encoding: chunked`, `Connection: close`,
`Date`. No cookies set by the shown GETs.

## 5. Observation vs hypothesis vs unknown (evidence-driven)

- **Observation:** Login and registration are the only two pre-auth data-entry forms;
  both are `POST` and carry no anti-CSRF token field in the rendered HTML.
- **Observation:** Stack signal is Tomcat-like (default 404 page); the framework is
  self-identified as WebGoat only by the page content. Version is **not** observed.
- **Hypothesis (auth-gated, untested):** Login credentials are validated against an
  account store; behavior for nonexistent accounts is unobserved (would require an
  account and login). Recorded for later, approved testing.
- **Hypothesis (untested):** Because the login and registration forms lack a visible
  CSRF token, state-changing auth `POST`s may be CSRF-prone. Impact is bounded for
  these self-service forms and must be verified before any claim. Not yet confirmed.
- **Unknown (explicit):** The entire authenticated lesson surface (all WebGoat lesson
  endpoints, `/WebGoat/api/*`, user/session management) is **auth-gated and was NOT
  observed**. It is recorded as an unknown, not an established surface. Per
  `02-recon.md`, no login, registration, or authentication-bypass probing was
  performed during recon.
- **Unknown (explicit):** WebWolf (`127.0.0.1:9090`) not reachable; its surface is
  unknown and not assumed.

## 6. Knowledge-router activation (evidence-supported only)

- **authentication (activated, latent):** observed login + registration flow.
- **web (potentially relevant):** CSRF-relevant state-changing POSTs exist; only a
  hypothesis, not a confirmed surface.
- **configuration (latent):** Tomcat-like 404 observed; version/flags unverified
  (self-reported/absent → do not rely on).
- **injection / authorization / api / modern-apps / files / business-logic / cloud /
  protocol:** NOT activated — insufficient observed evidence pre-auth. Revisit after
  authenticated access is approved and observed.

## 7. Data / destructiveness concerns

- No account was created; no password reset, no login, no data mutation performed.
- Terms-of-use text self-reports that WebGoat "binds to localhost"; this is
  corroborated by the observed loopback binding and treated as self-reported.

## 8. Proposed next steps (require human approval)

1. Grant approved authenticated-testing scope in this lab: human authorizes
   registration of one throwaway lab account (and use of it) for approved reading of
   lessons/APIs. Registration/login/account creation is **not** performed during
   recon per `02-recon.md`; it is deferred to an explicitly approved phase.
2. On approval, re-confirm scope and continue adaptive, evidence-driven assessment
   (broad, not stopping at first finding) with post-auth endpoints routed via
   `knowledge/index.md`.
