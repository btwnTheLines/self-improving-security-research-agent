# Approved Implementation  -  Cycle #3 Proposal A (knowledge router)

- **Date:** 2026-09-22 (Proposal A applied). Proposal B subsequently **executed**
  as a post-authentication regression on 2026-09-23 (see
  `evidence/self-improvement/10-dvwa-cycle4-postauth-regression.md`).
- **Status:** Proposal A approved by the human operator and **applied** to the
  knowledge router. Proposal B (a sequencing decision, not a rule edit) was
  **kept for the next testing cycle, then executed** as a separate,
  approval-gated, non-exploitative post-auth regression in Cycle #4. No
  `.clinerules` files were modified. No security testing was performed while
  making these changes.
- **Source:** `evidence/self-improvement/08-dvwa-cycle3-self-review.md`
  (Proposal A) -> approved.

---

## What changed and why

### Proposal A  -  "Self-reported configuration is not evidence" -> `knowledge/index.md`
- **Why:** Cycle #3 review found the anti-assumption protection for a strongly
  self-identifying surface was carried only by the characterization step
  (recon U-B), not by the routing/activation step. A branded application's
  self-claimed identity, version, or security level could otherwise seed prior-
  app bias or drive module selection on unverified facts.
- **Change:** Added a short, app-agnostic note at the top of the knowledge
  router (`knowledge/index.md`), placed between the cross-cutting routing note
  and the tool-selection section: treat any application-reported identity,
  version, or claimed security/feature level as unverified unless corroborated;
  do not route or reason on it as fact; flag and corroborate before relying on
  it. It **cross-references**, rather than restating, the recon rule
  `.clinerules/02-recon.md` "Distinguish Observed from Self-Reported
  Configuration" (U-B), extending that rule to the activation/reasoning step.
- **Scope of change:** One section added to `knowledge/index.md`. No router
  entries, tool-selection text, or module content changed.

---

## Requirements verification

1. **App-agnostic / technology-agnostic:** Yes  -  wording references no
   application, target, framework, endpoint, or product. It uses only general
   terms (identity, version, security/feature level).
2. **Additive / not weakening:** Yes  -  adds a note only; no existing text in
   `knowledge/index.md` was removed or altered, and no `.clinerules` constraint
   was changed or weakened.
3. **Not duplicative:** Yes  -  cross-references `02-recon.md` U-B by name
   instead of restating it; keeps a single source of truth.
4. **Correct placement (activation step):** Yes  -  sits adjacent to the routing /
   cross-cutting guidance, so it applies when selecting modules and reasoning on
   surface evidence, not only at characterization.
5. **No application-specific content entered the machine layer:** Yes  -  the
   `knowledge/machine/*.md` modules were not modified by this change.
6. **Re-read after editing:** Yes  -  `knowledge/index.md` was re-read and
   confirmed (section present, correctly placed, prose coherent, cross-reference
   accurate).
7. **Consistency with existing rules:** Yes  -  consistent with `02-recon.md`
   (U-B), `00-core.md` (never invent/assume), and `04-validation.md`
   (generalize lessons; preserve guardrails).

---

## Proposal B status

- **Kept for the next testing cycle at the time of Cycle #3, then EXECUTED in
  Cycle #4 (2026-09-23).** A post-authentication, non-exploitative,
  approval-gated regression (to exercise the latent classes' selection and to
  validate the Kali capability-manifest layer) was carried out against the
  authorized local target. Full evidence, router-activation mapping,
  tool-selection analysis, and guardrail re-check are in
  `evidence/self-improvement/10-dvwa-cycle4-postauth-regression.md`. No part of
  Proposal B was acted on during the Cycle #3 change step itself.

---

## Files modified

- `knowledge/index.md`  -  added section "Self-reported configuration is not
  evidence" (Proposal A).

## Files intentionally left unchanged

- `.clinerules/*`  -  no change (Proposal A is a knowledge-layer change; approval
  and other gates remain intact).
- `knowledge/machine/*`, `knowledge/human/*`, `knowledge/README.md`,
  `knowledge/kali-wsl-capabilities.md`  -  unchanged.
- `evidence/self-improvement/08-dvwa-cycle3-self-review.md`  -  reviewed; its
  Proposal A/B status lines updated to record approval/deferral (pointer to this
  record).

---

*End of record. Proposal A implemented and verified. Proposal B deferred to the
next testing cycle at the time of this record, and subsequently executed in
Cycle #4 (2026-09-23) - see 10-dvwa-cycle4-postauth-regression.md. No security
testing performed during the Cycle #3 change step.*