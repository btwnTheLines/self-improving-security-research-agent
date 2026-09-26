# Self-Review — DVWA Assessment (cycle 4 post-auth)

## Questions and answers
- **Objective?** Confirm vulnerabilities with evidence and generate per-finding reports using the new template.
- **What actually happened?** Mapped authentic/full surface, confirmed 9 distinct findings across classes, preserved raw evidence, wrote 9 reports + summary.
- **What worked?** A single consistent cookie session fixed the login token mismatch; methodical two-round evidence (baseline control + proof) made findings reproducible and each difference attributable to the injected input.
- **What went wrong?** (1) Initial login 403 was my own session/token mismatch (bad: different cookie jars for extraction vs submission), corrected. (2) First `info.php` guess was a 404 — a bad made-up path; corrected by using the actual authenticated `setup.php` surface.
- **Did I follow the applicable rules?** Yes — scope confined to the local target; no brute-force/auth-bypass/destructive actions; human approval gates not bypassed; consecutive unexpected-"findings" attribution errors avoided by pairing each proof with a baseline control.
- **Unsupported assumptions?** Clearly separated inferred impact (upload RCE, LFI→RCE, PHPSESSID predictability) from demonstrated impact; flagged app-reported version info as unverified.
- **Efficient use?** Reasonable; stopped live testing once 9 classes were evidenced rather than continuing to maximize (minimum-testing principle).
- **Stopping condition met?** Yes — after sufficient evidence for each class.
- **Reusable lesson?** (a) For state-bound anti-CSRF/CSRF/session tokens, use ONE consistent client state (cookie jar + headers) for both token retrieval and submission — otherwise the failure is a self-inflicted session mismatch, not an application finding. (b) A single tool-consumed response is not proof; a probe plus a matched baseline control makes the attribution reliable. (c) When server keeps only client-side checks for uploads, confirm with a benign non-executable file and stop short of dropping an executable webroot artifact.
- **Generalization to other targets?** Yes — all three lessons are application-agnostic (single-state for state-bound tokens; control-paired probes; minimal non-executable upload proof).

## Guardrail preservation check
No weakening of scope, approval gates, evidence, minimum-testing, or stopping rules. Reports are for human review; no auto-submission. Purely additive artifacts created under `knowledge/` (Phase 1) and `evidence/reporting/` (Phase 2); no core rules modified during the assessment.

## Improvement proposals (recorded only — NOT applied; require human approval)
1. **Token/session consistency guidance:** add a general note to reconnaissance/testing rules — when a state-bound token is required, keep one cookie jar and headers consistent for retrieval and submission to avoid self-inflicted session mismatches.
2. **Control-paired evidence:** codify "pair each probe with a matched baseline control and record both" as a standing evidence practice.
3. **De-duplication rule:** when the same class appears across multiple input channels (e.g., blind vs error-based SQLi), report it as one class-level finding unless independent impact is shown.

## Final artifact verification
Re-read the nine reports and the summary to confirm structure, evidence accuracy, and that no guarded rule was weakened (see next step).