# WebGoat — Authenticated Read-Only Recon (Learning Path & API Surface)

- Date: 2026-09-26
- Status: Recon / authenticated read-only surface characterization, including **completed
  read-only enumeration of all lesson assignment endpoints**. **No assignment
  submissions, no state-changing POSTs other than the approved register+login, no
  destructive controls invoked.**
- **Post-assessment update (2026-09-26):** Following this read-only phase, an
  authorized active-testing assessment of `127.0.0.1:8080/WebGoat/` was performed
  (broad, boundary-limited authorization) and produced six (6) confirmed findings,
  reports and raw evidence under `evidence/reporting/wg-*.md` /
  `evidence/reporting/raw/wg_*.txt`, summarized in
  `evidence/reporting/wg-00-assessment-summary.md`. This file remains the read-only
  characterization log from the pre-assessment phase.
- Scope: `http://127.0.0.1:8080/WebGoat/` (OWASP WebGoat, loopback-only lab). See
  `01-scope.md` and `webgoat-pre-auth-recon.md`.
- Account used: throwaway lab account `wgprobe55726128` (scratch/throwaway; **do not
  reuse**). Registered and logged in under the human-approved authenticated phase.
- Rules observed: `00-core.md`, `01-scope.md`, `02-recon.md`, `04-validation.md`,
  `05-reporting.md`; knowledge router `knowledge/index.md`.


## 1. Scope of this phase (approved)

- Human approved authenticated **read-only recon**: read lesson/API surface,
  characterise architecture.
- Allowed here: benign `GET`s (pages, JS modules, JSON/HTML service endpoints,
  lesson content). Registration + login of the throwaway account were explicitly
  approved and performed once (`webgoat_auth3.py`).
- **Not** allowed yet (requires further approval): submitting assignment answers,
  exploit-probing any endpoint, invoking destructive/admin controls,
  authorization/authentication-bypass testing.

## 2. Method (least-powerful tool)

- Python 3.14 stdlib `urllib` only (cookie jar, redirects); loopback-only. No
  software installed.
- New raw artifacts under `evidence/reporting/raw/`:
  - `webgoat_read_welcome.txt` — `GET /WebGoat/welcome.mvc` (redirects to
    `start.mvc?username=...`).
  - `webgoat_read_mailcount.txt` — `GET /WebGoat/mail/count` → JSON `{"count":1}`.
  - `webgoat_read_mail.txt` — `GET /WebGoat/mail` → mailbox HTML for `wgprobe55726128@webgoat.org`.
  - `webgoat_read_mainjs.txt` — `GET /WebGoat/js/main.js` (RequireJS entry).
  - `webgoat_read_goatapp.js`, `webgoat_read_goatrouter2.js`,
    `webgoat_read_lessoncontroller.js`, `webgoat_read_menucontroller.js`,
    `webgoat_read_lessoncontentmodel.js`, `webgoat_read_lessoninfomodel.js`,
    `webgoat_read_menuview.js`, `webgoat_read_menucollection.js` — sampled core
    front-end modules (static-asset sampling, bounded).
  - `webgoat_read_lessonmenu.mvc` — `GET /WebGoat/service/lessonmenu.mvc`
    (JSON lesson catalog, observed).
  - `webgoat_read_labels.mvc` — `GET /WebGoat/service/labels.mvc` (i18n JSON).
  - `webgoat_read_webgoatintro.lesson` — `GET /WebGoat/WebGoatIntroduction.lesson`
    (control GET confirming `.lesson` content + assignment-form endpoints).

## 3. Architecture (observed, not assumed)

- **SPA client**: RequireJS/Backbone SPA. `js/main.js` boots `goatApp/goatApp`
  which builds `GoatRouter` (`goatApp/view/GoatRouter`). Routes observed:
  `welcome`, `lesson/:name`, `lesson/:name/:pageNum`, `reportCard`, `adminPanel`.
- **Lesson content is loaded dynamically** via `goatApp/model/LessonContentModel`
  → `GET /WebGoat/<LessonName>.lesson` (HTML with paginated pages and
  `form.attack-form` assignment forms).
- **Menu** from `goatApp/model/MenuCollection` → `GET /WebGoat/service/lessonmenu.mvc`
  (JSON catalog of categories → lessons).
- **Server-rendered shells** exist too: `/WebGoat/start.mvc`, `/WebGoat/welcome.mvc`,
  `/WebGoat/mail` (mailbox), `/WebGoat/login`, `/WebGoat/registration`.

## 4. Observed authenticated surface (recorded as observed)

### Service endpoints (observed in JS models / code)
| Endpoint | Method | Purpose (as observed) |
| --- | --- | --- |
| `/WebGoat/<LessonName>.lesson` | GET | Lesson content HTML incl. assignment forms |
| `/WebGoat/service/lessonmenu.mvc` | GET | Lesson catalog JSON |
| `/WebGoat/service/lessoninfo.mvc/<lesson>` | GET | Lesson metadata/info (per `LessonInfoModel`) |
| `/WebGoat/service/labels.mvc` | GET | i18n labels JSON |
| `/WebGoat/service/restartlesson.mvc/<lesson>` | GET | **Resets lesson progress — destructive control, OFF-LIMITS (not invoked)** |
| `/WebGoat/mail/count` | GET | JSON unread-mail count |
| `/WebGoat/mail` | GET | Mailbox HTML for current user |

### Assignment submission protocol (observed in code, NOT executed)
- Forms have class `attack-form` with `method` + `action` attributes; submitted via
  jQuery AJAX (per-form `method`). Response is JSON with `feedback`, `output`,
  `attemptWasMade`, `lessonCompleted`, `assignmentCompleted`.
- No CSRF token field/header was observed in the client submission path
  (`onFormSubmit` in `LessonContentView.js`). **Unverified** — to be confirmed only
  by later, approved testing; not a claim of absence.
- Content-Type defaults to `application/x-www-form-urlencoded`; `multipart/form-data`
  handled when the form `enctype` is set (e.g. file-upload lessons).

### Mailbox lesson assignment endpoints (observed in `WebGoatIntroduction.lesson`)
- `POST /WebGoat/WebGoat/mail` — submit `uniqueCode`.
- `POST /WebGoat/WebGoat/mail/send` — send email (field `email`).
- Note the doubled `/WebGoat/WebGoat/` prefix in the rendered action path — an
  observed detail to preserve exactly; not "corrected".
- Observed mailbox semantics: mail to `<user>@webgoat.org`; the UI states only the
  user part matters, domain can be anything.

## 5. Observed lesson catalog (from `service/lessonmenu.mvc`)

Categories → `<Lesson>.lesson` links observed (all `#lesson/...`, i.e. SPA route to
`GET /WebGoat/<Lesson>.lesson`):

- category.introduction: `WebGoatIntroduction`, `WebWolfIntroduction`
- category.general: `HttpBasics`, `HttpProxies`, `ChromeDevTools`, `CIA`,
  `LessonTemplate`, `OpenRedirect`
- category.a1: `HijackSession`, `IDOR`, `MissingFunctionAC`, `SpoofCookie`
- category.a2: `Cryptography`
- category.a3: `SqlInjection`, `SqlInjectionAdvanced`, `SqlInjectionMitigations`,
  `CrossSiteScripting`, `CrossSiteScriptingStored`, `CrossSiteScriptingMitigation`,
  `PathTraversal`
- category.a5: `CSRF`, `SecurityMisconfiguration`, `XXE`
- category.a6: `VulnerableComponents`
- category.a7: `AuthBypass`, `InsecureLogin`, `JWT`, `PasswordReset`, `SecurePasswords`
- category.a8: `InsecureDeserialization`
- category.a9: `LogSpoofing`
- category.a10: `SSRF`
- category.client.side: `BypassRestrictions`, `ClientSideFiltering`, `HtmlTampering`
- category.challenge: `ChallengeIntro`, `Challenge1`, `Challenge5`, `Challenge7`,
  `Challenge8`

This catalog is **observed data** (a GET of the menu endpoint), not a guess.

## 6. Observation vs hypothesis vs unknown

- **Observation (confirmed):** The authenticated app is a Backbone SPA driven by
  lesson-plans fetched from server MVC endpoints; lesson names/links are exposed in
  `service/lessonmenu.mvc`; lesson content is `GET /WebGoat/<Lesson>.lesson`
  (verified with a benign control GET of `WebGoatIntroduction.lesson`).
- **Observation (confirmed):** Assignment endpoints are embedded in lesson content
  as posted `form.attack-form` actions; the mailbox lesson's two POST endpoints and
  their parameter names are observed.
- **Observation (confirmed):** `service/restartlesson.mvc/<lesson>` exists as a
  progress-reset control → treated as destructive/administrative and off-limits.
- **Observation (confirmed):** Other lessons each expose a small set of assignment
  `POST`/`GET`/`PUT` endpoints of the form `<LessonName>/<assignmentAction>`
  (confirmed across all 39 menu lessons; full map in
  `webgoat-lesson-endpoint-map.md`). Method mix observed: mostly `POST`, plus GET
  (`OpenRedirect/safe`, `IDOR/profile`, `IDOR/profile/{userId}`,
  `CrossSiteScripting/attack5a`) and one `PUT` (`SqlInjectionAdvanced/register`).
- **Hypothesis (untested):** No anti-CSRF token is required for assignment
  submission (based on absence in client code). Unverified; do not rely on.
- **Unknown (explicit):** Behavior/validation of each assignment endpoint, any
  admin/report-card surface, and whether lessons enforce any server-side data
  access control — all gated on actually submitting assignments, which is **not**
  performed in this read-only phase.
- **Unknown (explicit):** Whether `service/lessoninfo.mvc` and other service
  endpoints are authorization-checked per user; not tested here.

## 7. Knowledge-router activation (evidence-supported only)

- **modern-apps (activated):** SPA/Backbone client, browser `localStorage`
  (`locale` in `goatApp.js`), dynamic lesson loads.
- **api (activated):** structured JSON menu/labels/mail `service/*.mvc` endpoints.
- **authentication (activated, latent):** confirmed register/login/session; session
  cookie `JSESSIONID` (`path=/WebGoat`, not `Secure`, `HttpOnly`).
- **injection / authorization / client / web / files / business-logic /
  configuration / protocol / cloud:** NOT activated yet — the lesson-specific
  surfaces (SQL, XSS, XXE, path traversal, file upload, etc.) are only **named** in
  the menu; exploit/validation behavior is unobserved (read-only phase). They can be
  activated individually later only with observed per-lesson evidence. The `web`
  (CSRF/redirect) class is only latent: a `CrossSiteScripting` lesson POST and mail
  redirect-send forms are named but not exercised.

## 8. Session & hygiene notes

- Single cookie-jar state maintained per run; each sampler re-logs-in for a fresh
  `JSESSIONID`.
- Throwaway account `wgprobe55726128` is session-scoped/arbitrary; treat as
  disposable and do not reuse.
- No data mutation beyond the approved account creation and login.

## 9. Destructiveness / data concerns

- `service/restartlesson.mvc/<lesson>` (progress reset) — **recognized as
  destructive; not invoked.**
- No assignment submitted; no exploit payloads sent; no availability-impacting
  requests made.

## 10. Lesson endpoint enumeration — COMPLETED (status update)

- Executed `work/webgoat_lesson_enum.py`: benign `GET /WebGoat/<Lesson>.lesson` for all
  39 menu lessons (200 OK each); parsed `form.attack-form` assignment endpoints.
- Artifacts: raw pages under `evidence/reporting/raw/webgoat_read_<Lesson>.lesson`
  (40 `.lesson` files incl. earlier `WebGoatIntroduction` control);
  machine map `work/lesson_endpoint_map.json`;
  evidence map `evidence/recon/webgoat-lesson-endpoint-map.md`
  (39 lessons, 117 assignment attack-forms + the 2 mailbox forms).
- **No form was submitted and no endpoint was exercised; endpoint definitions are
  observed, behavior/validation is untested.**
- Notable observations (recorded as observed; **not exercised**):
  - Method mix is mostly `POST`; GET endpoints exist (`OpenRedirect/safe`,
    `IDOR/profile`, `IDOR/profile/{userId}`, `CrossSiteScripting/attack5a`); one
    `PUT` (`SqlInjectionAdvanced/register`).
  - Some forms carry `{userId}` path placeholders (`IDOR/profile/{userId}`) —
    templated identifiers; presence of a path-parameterized read endpoint is an
    observation, not an authorization claim (untested).
  - JWT lesson embeds full self-supplied example JWTs in two form `action` URL query
    strings (`JWT/jku/delete?token=…`, `JWT/kid/delete?token=…`). These are the
    application's own example tokens present in lesson content; recorded only.
  - SqlInjectionMitigations page references two additional sibling lessons
    (`SqlOnlyInputValidation`, `SqlOnlyInputValidationOnKeywords`) with their own
    `/attack` endpoints.
  - No assignment endpoint was invoked, so none of these surfaces has known behavior.

## 11. Next steps (require human approval before execution)

1. (**Done**) Read-only enumeration of lesson endpoints — completed; map recorded.
2. (**Done**) Authorized active-testing assessment performed under broad,
   boundary-limited authorization (the operator's explicit WebGoat range grants);
   see `evidence/reporting/wg-00-assessment-summary.md` for confirmed findings,
   and `evidence/reporting/wg-01..06` + `raw/wg_*` for evidence.
3. Do **not** invoke `restartlesson.mvc` or any destructive/admin control; the
   `service/restartlesson.mvc/<lesson>` progress-reset control remains
   destructive and was not used during the assessment.


