# Approved Improvements — Applied to .clinerules

- **Date:** 2026-09-14
- **Status:** All improvements A–F approved by the human operator and **applied**.
- **Source:** `evidence/self-improvement/01-h4-review.md` (proposed) → approved.
- **No security testing was performed** while making these changes.

---

## What changed and why

### A. Verify generated artifacts — added to `04-validation.md` (§ "Verify Generated Artifacts")
- **Why:** In the H4 reporting phase, `reports/h4-mass-assignment.md` was initially
  written with sections out of order and was caught only by re-reading. Multi-edit
  artifacts are error-prone.
- **Change:** *After creating or editing an evidence, findings, or report file,
  re-read it to confirm the intended content and structure before proceeding.*

### B. Inspect raw context before pattern-mining — added to `02-recon.md` (§ "Context Before Pattern-Mining")
- **Why:** During recon, multiple regex extractions returned `count=0` (wrong
  assumed string format) before a raw sample was inspected. Mining should be
  grounded in the observed format.
- **Change:** *First inspect a small raw sample of the target strings to learn
  their actual syntax before writing search/extraction logic; base extraction on
  the observed format, not guessed patterns.*

### C. Minimal controls to disambiguate tests — added to `03-testing.md` (§ "Disambiguation")
- **Why:** Several single-probe results were ambiguous (negative could mean
  "blocked" or "wrong validation path"), e.g., a `401` without a control.
- **Change:** *When safe and within approved scope, pair a probe with a minimal
  control so a negative result is more informative, and record both.*

### D. Confirm the session/token model before auth tests — added to `03-testing.md` (§ "Authentication Context")
- **Why:** The JWT test relied on a guessed claim name rather than a captured
  token, reducing reliability.
- **Change:** *Before constructing authentication or authorization tests, confirm
  the session/token structure empirically from a genuine token when available.*

### E. Generalized lessons free of app-specific vectors — added to `04-validation.md` (§ "Generalized Lessons")
- **Why:** Some "canonical" vectors were application-specific and could be mistaken
  for general rules.
- **Change:** *Express generalized lessons as vulnerability classes and security
  principles, without referencing specific endpoints, claim names, role values, or
  other application-specific details.*

### F. Preserve guardrails — added to `04-validation.md` (§ "Preserve Guardrails")
- **Why:** Improvements must never erode existing safety controls.
- **Change:** *When adopting or extending rules, do not weaken existing safety,
  scope, human-approval, evidence, minimum-testing, or stopping requirements.*

---

## Requirements verification

- **Existing safety/scope/approval/evidence/stopping rules intact:** Yes — no
  existing text was removed or altered; `04-validation.md` now explicitly
  reinforces non-weakening (F). `00-core.md` and `01-scope.md` were not modified.
- **No application-specific / Juice Shop-specific rules or vector added:** Yes —
  all five added sections are universal and technology-agnostic.
- **Improvements universal:** Yes, expressed as classes/principles only.
- **No constraint weakened:** Yes — all additions are additive/restrictive.
- **Concise, no duplication:** Yes — each improvement landed in exactly one
  appropriate file (B→02-recon; C,D→03-testing; A,E,F→04-validation). `05-reporting.md`
  was not modified (no improvement mapped to it).
- **Re-read after editing:** All three modified files were re-read and confirmed;
  a missing blank-line separator in `03-testing.md` was corrected for consistency.

## Files modified

- `.clinerules/02-recon.md` (was empty) — added Reconnaissance Rules + B.
- `.clinerules/03-testing.md` — appended C and D (no existing text changed).
- `.clinerules/04-validation.md` (was empty) — added Validation Rules with A, E, F.