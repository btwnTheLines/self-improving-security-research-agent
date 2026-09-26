# Approved Improvements P1–P5 — Generalization of .clinerules

- **Date:** 2026-09-14
- **Status:** P1–P5 approved by the human operator and **applied**.
- **Source:** `evidence/self-improvement/03-generalization-design.md` → approved.
- **No security testing was performed while making these changes.**

---

## Exact changes and rationale

### P1 — Characterize the environment before assuming endpoints → added to `02-recon.md`
- **Change:** New section "Characterize the Environment First": observe the
  application's architecture (server-rendered/SPA/API-only/hybrid), data/interface
  paradigm (REST/GraphQL/RPC/forms/WebSocket), content types, and how inputs travel;
  derive approach from observations, not prior application or assumed technology.
- **Why:** On an unknown app, pre-existing endpoint/tech assumptions silently
  reapply unless recon is explicitly grounded in the observed interface.

### P2 — Hypotheses originate from the observed surface → added to `03-testing.md`
- **Change:** New section "Hypothesis Provenance": generate hypotheses from the
  observed attack surface or from clearly labeled general security principles; do
  not transplant expected vulnerabilities, endpoints, payloads, or auth mechanisms
  from another application/environment.
- **Why:** Prevents seeding tests from a prior app's vulnerability catalog.

### P3 — Re-establish scope per environment → added to `01-scope.md`
- **Change:** New section "Per-Environment Scope": scope is not inherited between
  engagements; re-confirm/record target(s), in-scope functionality, and data
  environment at the start of each new environment; do not assume prior host, port,
  application, endpoints, or auth model carries over.
- **Why:** The scope file is per-target; silent reuse of a prior target is the main
  portability risk.
- **Also (requirement 3):** generalized target wording — replaced the technology-
  specific target description with an application-agnostic note, and replaced
  "Juice Shop instance" scope phrasing with "authorized in-scope target". The
  concrete authorized URL (`http://localhost:3000`) is retained because it defines
  the current authorization (per requirement 1).

### P4 — Generalize "local lab" wording → edited `03-testing.md` (Safe Testing)
- **Change:** "explicitly authorized local lab" → "explicitly authorized test
  environment" (wording only; no behavior change).
- **Why:** Safe-testing permission should be expressed for the authorized
  environment generally, regardless of hosting.

### P5 — Reporting baseline → added to `05-reporting.md`
- **Change:** New file with "Reproducible Evidence" (include exact requests/responses
  as evidence) and "Class-Level Framing" (impact/root cause in technology-agnostic,
  class-level terms per `04-validation.md`).
- **Why:** The reporting file was empty; explicit rules keep findings reproducible
  and generic.

---

## Requirements verification

- **Existing safety/scope/approval/evidence/stopping rules preserved:** Yes — no
  existing rule text was removed or weakened; all changes are additive or
  wording-only. `00-core.md` and `04-validation.md` were not modified.
- **No constraint weakened:** Yes.
- **Juice Shop / technology-specific assumptions removed from rules:** Yes — a scan
  of `.clinerules` shows no remaining Juice Shop/OWASP/Angular/"local lab" references.
  The only `localhost:3000` occurrences are the concrete current target in
  `01-scope.md`, which is required for authorization and framed as per-environment.
- **Scope explicitly re-established per environment:** Yes — new `Per-Environment
  Scope` section in `01-scope.md`.
- **Hypotheses from observed evidence or clearly labeled general principles:** Yes —
  new `Hypothesis Provenance` section in `03-testing.md`.
- **Concise, non-duplicative:** Yes — each improvement placed in the single most
  appropriate file; cross-references (`01-scope` from `03-testing`;
  `04-validation` from `05-reporting`) used instead of restating text.
- **Re-read every modified file after editing:** Yes — `02-recon.md`, `03-testing.md`,
  `01-scope.md`, and `05-reporting.md` re-read and confirmed; formatting issues from
  line-based insertion (a section landing mid-list in `01-scope.md`, missing blank
  lines) were detected and corrected.
- **Internally consistent:** `02` (observe-before-assume) ↔ `03` (hypothesis
  provenance, auth-context, disambiguation) ↔ `01` (per-environment scope) ↔
  `05` (class-level framing, cross-referencing `04`) are mutually consistent.

## Files modified

- `.clinerules/02-recon.md` — added "Characterize the Environment First" (P1).
- `.clinerules/03-testing.md` — added "Hypothesis Provenance" (P2) and generalized
  the Safe Testing wording (P4).
- `.clinerules/01-scope.md` — generalized target/scope wording and added
  "Per-Environment Scope" (P3).
- `.clinerules/05-reporting.md` — created with reporting baseline (P5).

## Files intentionally left unchanged

- `.clinerules/00-core.md`, `.clinerules/04-validation.md` — already universal; not
  touched.
- Historical `evidence/` and `reports/` files retain prior Juice Shop/tech references
  as factual records and were **not** altered.