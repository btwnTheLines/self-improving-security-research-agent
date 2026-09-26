# Approved Improvements — DVWA Generalization (U-A, U-B, U-C, U-D)

- **Date:** 2026-09-16
- **Status:** U-A, U-B, U-C, U-D approved by the human operator and **applied**.
  U-E was **rejected** as a fixed characterization checklist. No security testing
  was performed while making these changes.
- **Source:** `evidence/self-improvement/05-dvwa-generalization-review.md`
  (U-A…U-E as candidate principles) → approved U-A, U-B, U-C, U-D.

---

## What changed and why

All four approved rules are reconnaissance behaviours and were therefore placed
together in `02-recon.md` as separate, concise, universal sections.

### U-A — Delimit the Surface by Authentication State → `02-recon.md`
- **Why:** When an app is login-gated and no valid session is available, recon
  should fully map the reachable pre-existing surface and record
  authentication-gated areas as explicit unknowns rather than logging in,
  registering, or probing bypasses. Kept as a discipline, **not** a rigid
  checklist.
- **Text added:** new section "Delimit the Surface by Authentication State".

### U-B — Distinguish Observed from Self-Reported Configuration → `02-recon.md`
- **Why:** An application's own reports about its versions, feature toggles, or
  defenses can be wrong or misleading; they must be flagged as unverified and
  corroborated, distinct from directly observed configuration.
- **Text added:** new section "Distinguish Observed from Self-Reported
  Configuration".

### U-C — Optional Static-Asset Sampling → `02-recon.md`
- **Why:** Sampling one small representative static asset is a useful, cheap way
  to classify server-rendered vs client-side, but only as an optional technique,
  not a mandatory step or a reason to download large assets.
- **Text added:** new section "Optional Static-Asset Sampling".

### U-D — Destructive or Administrative Controls Are Off-Limits → `02-recon.md`
- **Why:** During recon, discovered destructive or administrative controls that
  could modify or wipe data must be noted as off-limits and not activated without
  explicit authorization, reinforcing the existing no-destructive rule at recon
  time.
- **Text added:** new section "Destructive or Administrative Controls Are
  Off-Limits".

### U-E — Rejected (as a fixed checklist)
- **What was proposed:** a standard "characterization request set" (root, login,
  setup/registration, robots, 404, one static asset).
- **Why rejected:** too rigid — an API-only or GraphQL app has no setup page,
  registration may not exist, and a static asset may not exist. It can bias an
  unknown target toward a page-based mental model. Kept only as a flexible
  heuristic (not codified) via the U-C optional-technique wording.

---

## Requirements verification

1. **Preserve every existing safety, scope, approval, evidence, stopping rule:** Yes —
   no existing text in any `.clinerules` file was removed or altered.
2. **Do not weaken any existing constraint:** Yes — all additions are additive/restrictive.
3. **All additions universal and technology-agnostic:** Yes — no application, framework,
   endpoint, or version specifics; U-C explicitly framed as optional.
4. **U-A reinforces disciplined pre-auth characterization + explicit unknowns, no rigid
   checklist:** Yes — describes a discipline (map reachable surface, record unknowns, do
   not log in/bypass/register), not a fixed inventory.
5. **U-B clearly distinguishes observed from self-reported/unverified configuration:** Yes —
   explicitly separates directly observed info from application-reported/unverified info.
6. **U-C treats sampling as an optional classification technique, not a mandatory step:** Yes —
   "is an optional technique", "Do not treat sampling as a mandatory step".
7. **U-D reinforces discovered destructive/admin controls are not activated during recon
   unless explicitly authorized:** Yes — "treat it as off-limits", "Do not activate ... unless
   explicitly authorized by the human operator".
8. **No DVWA- or Juice-Shop-specific knowledge added:** Yes — grep of `.clinerules` shows no
   such terms in the added text. `01-scope.md` retains the concrete authorized-target URL
   (`localhost:3000`), which is current-authorization definition text (per prior P3), not
   app-specific rule knowledge; unchanged.
9. **Avoid duplicate rules and unnecessary verbosity:** Yes — each rule added exactly once
   in `02-recon.md`; no duplication with `00-core` (no-destructive), `03-testing`
   (auth-context/human-approval), or `04-validation`.
10. **Re-read every modified file after editing:** Yes — `02-recon.md` re-read and confirmed
    (a missing blank-line separator between sections was detected and fixed).
11. **Consistency across the complete rule set:** Yes — U-A aligns with `03-testing`
    (auth-context, human-approval), U-B stands alone in recon, U-C is optional, U-D aligns
    with `00-core` principle 7 (no destructive testing). No contradictions or duplication.
12. **Record exactly what changed, why, and which proposal was rejected:** Yes — see above.

---

## Files modified

- `.clinerules/02-recon.md` — added four sections: "Delimit the Surface by
  Authentication State" (U-A), "Distinguish Observed from Self-Reported
  Configuration" (U-B), "Optional Static-Asset Sampling" (U-C),
  "Destructive or Administrative Controls Are Off-Limits" (U-D).

## Files intentionally left unchanged

- `.clinerules/00-core.md`, `01-scope.md`, `03-testing.md`, `04-validation.md`,
  `05-reporting.md` — no improvement mapped to them; not modified.
- U-E was not added as a fixed checklist.

---

*End of record. No `.clinerules` files other than `02-recon.md` were modified and no security
testing was performed.*