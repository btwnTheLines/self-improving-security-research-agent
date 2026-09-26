# Generalization Design — Workflow for an Unknown Deliberately Vulnerable Application

- **Date:** 2026-09-14
- **Status:** Analysis only. **No security testing performed; no `.clinerules` modified.**
- **Context:** The prior environment was a specific, known training application
  (OWASP Juice Shop). The next environment will be a *different* deliberately
  vulnerable application whose architecture, technology, endpoints, authentication
  model, and vulnerability set are **initially unknown**.
- **Constraint for this analysis:** I must not assume known endpoints, known
  vulnerability locations, known payloads, known auth mechanisms, known framework
  behavior, or prior-application patterns.

---

## 1. What the existing workflow already handles universally

These rules are technology- and target-agnostic and should carry over unchanged:

- **Core behavioral rules (`00-core.md`):** explicit scope discipline, authorization
  is not assumed, minimum necessary testing, data minimization, no destructive
  testing, no DoS unless authorized, no persistence/credential theft, no HackerOne
  submission, and a strict evidence standard that separates observation,
  hypothesis, evidence, confirmed vulnerability, impact, and speculation.
- **Human verification gate (`00-core.md`):** explain hypothesis/evidence/uncertainty,
  propose minimum verification, and wait for approval before consequential testing —
  fully app-agnostic.
- **Scope escalation on discovery (`03-testing.md`):** stop and do not investigate
  newly discovered hosts/domains/services — universal.
- **Approval gate and consequential-testing list (`03-testing.md`):** generic
  categories (auth bypass, authorization bypass, other users' data, privilege
  escalation, data modification, uploads, exploit payloads, credential attacks,
  availability, uncertain safety) — app-agnostic.
- **Minimum-necessary-testing and stop rules (`03-testing.md`, `00-core.md`):** use
  the smallest test; STOP once sufficient evidence — universal.
- **Evidence record template (`03-testing.md`):** hypothesis / test / request /
  response / interpretation / confidence / uncertainty — universal.
- **Disambiguation with controls and auth-context confirmation (`03-testing.md`):**
  empirically confirm the session/token structure and pair probes with a minimal
  control — designed to work on unknown models.
- **Context-before-pattern-mining (`02-recon.md`):** inspect a raw sample of the
  actual format before writing extraction logic — explicitly written for unknown
  formats.
- **Validation rules (`04-validation.md`):** verify generated artifacts; express
  generalized lessons as classes/principles (no app-specific vectors); preserve
  existing guardrails when adopting improvements — universal.
- **Communication (`00-core.md`):** be concise, explicit, never invent
  vulnerabilities/evidence (timely for unknown apps where there is no prior catalog
  to lean on).

**Net:** the safety, evidence, approval, minimum-testing, stop, context-before-mining,
and generalization-of-lessons machinery is environment-independent.

---

## 2. Assumptions that could fail on a different application

### 2.1 Architecture / client-technology assumptions
- Prior recon assumed an **Angular SPA** with a large `main.js` client bundle from
  which routes/endpoints could be mined. A different app may be **server-rendered**,
  **API-only**, **mobile/native API**, **GraphQL** (single endpoint), **WebSocket**,
  or **static + thin client**. Endpoint enumeration strategy differs accordingly and
  a client bundle may not exist.
- Prior assumptions about `/api/...` and `/rest/...` path conventions, and template
  literals with a `${hostServer}` prefix, are app-specific and must **not** be reused.

### 2.2 API / data-paradigm assumptions
- REST JSON may not describe the next app. The interface could be **GraphQL** (one
  POST endpoint, introspection), **JSON-RPC**, **SOAP**, **gRPC**, **URL-encoded
  forms**, **multipart**, or **WebSocket messages**. Content types and how parameters
  travel (query, body, headers, cookies) differ.
- Request/response shapes, error conventions, and where input is validated differ.

### 2.3 Authentication / authorization model assumptions
- JWT-in-`localStorage` + `Authorization: Bearer` is not universal. The next app may
  use **session cookies**, **httpOnly cookies**, **OAuth/OIDC**, **SAML**, **API keys**,
  **basic auth**, **client certificates**, plus **CSRF tokens**. Storage location
  (localStorage vs cookie) changes XSS/CSRF exposure and what a "genuine token" looks
  like.
- The admin/role model (numeric/string roles, `role:"admin"` value, a "list all
  users" admin operation) is app-specific; authorization enforcement may be
  endpoint-, data-, or object-scoped in ways not present before.

### 2.4 Hypothesis-source assumption
- Prior hypothesis selection leaned on prior knowledge that the app was a specific
  deliberately-vulnerable training app with known challenge locations (SQLi in
  search, `alg:none`, admin registration). On an unknown app we **cannot** seed
  hypotheses from such a catalog; hypotheses must be derived from the **observed**
  attack surface and may cover an entirely different vulnerability set.

### 2.5 Scope / environment assumptions
- The scope file currently hard-codes `http://localhost:3000`, the specific app, and
  Docker. These must be re-established; carrying over entities (localhost:3000, the
  same port, the same app) would be an assumption that can fail silently.
- Environment-data assumptions: the prior app had synthetic **seed data**; the next
  app may contain real or sensitive data, changing how "unnecessary data access" is
  weighted.

### 2.6 Registration / business-flow assumptions
- The prior mass-assignment test depended on a registration shape (email, password,
  passwordRepeat, security question/answer, `role`). A different app's registration,
  or absence of self-registration, would invalidate that exact test.
---

## 3. Information to establish before testing (grounding checklist)

Before any consequential test on a new environment, establish the following from
direct observation (and from the operator/system), not from prior-app assumptions:

1. **Authorized scope (re-validated):** target host(s)/port(s), allowed endpoints,
   and the program's rules/rate limits — re-read at the start of the new engagement.
2. **Application architecture/type:** server-rendered vs. SPA vs. API-only static;
   whether a client bundle or visible routes exist; whether it is web, mobile-API, or
   hybrid.
3. **API/data paradigm:** REST, GraphQL, RPC, form-based, or WebSocket; content
   types; how inputs are transmitted (query/body/headers/cookies).
4. **Authentication model (empirical):** mechanism (cookie/session/JWT/OAuth/API
   key/Basic/etc.), where tokens/session state live (including httpOnly/`SameSite`),
   and whether CSRF tokens are present. Obtain/observe a genuine credential/session
   artifact where possible.
5. **Authorization model/roles:** which functional areas exist and which require
   elevated roles (observe from navigation/APIs/errors, not from a catalog).
6. **Functional surface and inputs:** the UI flows and their purpose; which actions
   read vs. modify data; where input is accepted (forms, JSON, file upload, search,
   filters).
7. **Data environment:** seed/synthetic vs. real/sensitive data, to calibrate
   data-minimization weight and the "access another user's data" approval gate.
8. **Baseline request/response formats:** raw sample of headers/body so extraction
   and probes match the observed format (per `02-recon.md`).

---

## 4. Do the `.clinerules` need improvement?

Yes, modestly. The universal core is strong and app-agnostic, but there are gaps that
encode a *single-app mental model* or leave key workflows implicit:

- **Gap 1 — Recon is under-specified for unknown apps.** `02-recon.md` only covers
  "context before pattern-mining." It does not instruct the agent to (a) determine
  the application/architecture type, (b) detect the API/data paradigm, (c) characterize
  the authentication model, (d) map functional areas and inputs, or (e) note whether
  data is real vs synthetic. On an unknown app these are foundational and currently rely
  on inference/prior assumptions.
- **Gap 2 — Hypothesis source is not constrained.** Nothing currently states that
  initial hypotheses must derive from the **observed** surface and must not be
  transplanted from a prior/vulnerable-catalog app. `02-recon.md`'s "not guessed
  patterns" is about extraction, not about hypothesis provenance.
- **Gap 3 — Scope file is per-target and easy to treat as inherited.** `01-scope.md`
  spells out the current target (making it inherently non-portable). A new environment
  must update it; nothing explicitly forbids silently reusing prior target/app/auth
  assumptions.
- **Gap 4 — "local lab" wording.** `03-testing.md` "Safe Testing" says "against the
  explicitly authorized local lab." This is local-lab-flavored and should read as
  "the authorized test environment" for portability (minor).
- **Gap 5 — Reporting rules file is empty (`05-reporting.md`).** For reproducible,
  generic findings, it may be worth a short general rule (exact requests in evidence,
  class-level framing), but this is optional for generalization.

None of these are security-weakening or app-specific; they are about *provenance* and
*explicit grounding* of assumptions before testing.
---

## 5. Proposed improvements (rationale only — NOT applied)

Each proposal is stated generally and would not reference any specific application,
endpoint, claim, or payload.

### P1 — Recon: characterize the application and interface before assuming endpoints
- **Rationale:** On an unknown app, endpoint mining and probes depend on whether it is a
  SPA/server-rendered/API-only app and on its API paradigm (REST/GraphQL/RPC/forms/
  WebSocket). Without explicit characterization, the prior SPA/REST/JWT mental model
  silently reapplies.
- **Proposed wording (Add to `02-recon.md`, "Reconnaissance Approach"):** *Before
  architecting extraction or tests, observe and record the application type, the
  API/data paradigm, the content types, and how inputs are transmitted. Derive the
  approach from these observations, not from any prior application.*

### P2 — Hypotheses must originate from the observed surface
- **Rationale:** Only the observed surface (routes, inputs, role-gated areas, API
  pattern, auth model) can justify initial hypotheses; a prior-app/vulnerability catalog
  must not seed them.
- **Proposed wording (Add to `02-recon.md` or `03-testing.md`):** *Generate hypotheses
  from the observed attack surface. Do not transplant expected vulnerabilities,
  endpoints, payloads, or auth mechanisms from another application or environment.*

### P3 — Re-establish scope and ground truth for each environment
- **Rationale:** The scope file is per-target; silently reusing the prior target or app
  assumptions is the main portability risk.
- **Proposed wording (Add to `00-core.md` or `01-scope.md`):** *At the start of each
  engagement, confirm and record the authorized target and environment. Do not assume
  the prior environment's host, port, application, endpoints, or auth model applies.*

### P4 — Generalize the "local lab" wording
- **Rationale:** Safe-testing permission should be specified against the *authorized
  environment* generally, not a local lab specifically.
- **Proposed wording (`03-testing.md`, "Safe Testing"):** replace "explicitly authorized
  local lab" with "explicitly authorized test environment" (wording change only; no
  behavior change). Since this is a rule-text edit, it would require human approval
  before application.

### P5 — (Optional) Reporting baseline
- **Rationale:** An empty reporting file offers no direction for keeping findings
  reproducible and class-level.
- **Proposed wording (Add to `05-reporting.md`):** *Include the exact requests/responses
  used as evidence and frame impact/root-cause in class-level, technology-agnostic terms
  (per `04-validation.md`).*

### Guardrail note
- All proposals are additive/general and would keep safety, scope, human-approval,
  evidence, minimum-testing, and stopping requirements intact. Per `04-validation.md`
  ("Preserve Guardrails"), none of the above may weaken existing constraints.

---

*End of analysis. No `.clinerules` were modified and no security testing was performed.
Adopting P1–P5 (or any subset) awaits human approval, with a regression check that the
agent still respects scope, approval gates, and the evidence standard on a new target.*