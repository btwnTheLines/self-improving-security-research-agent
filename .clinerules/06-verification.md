# Verification Recipe Rules

## Purpose

Every **confirmed** finding must be accompanied by a human-readable **Verification
Recipe** before any report is produced. The recipe lets a human operator
independently re-run the minimal test and verify the finding without relying on
this system's internal context. It is the explicit manual-verification approval
gate between "confirmed" and "reported".

## Canonical workflow

```
Recon → Hypothesis → Automated Test → Differential Validation → Confirmed Finding
      → Verification Recipe Generation → HUMAN MANUAL VERIFICATION
      → Evidence Review → Report
```

The Verification Recipe stage is **mandatory**. A finding must not move to the
Report stage until a human has manually verified it against the recipe.

The agent generates the recipe and then **STOPS**. It does not perform, repeat,
or substitute for the human's manual verification, and it must not treat its own
reproduction of the finding as satisfying this gate.

## Recipe requirements

For every confirmed vulnerability, generate a verification recipe that covers:

- Finding and vulnerability class
- Target endpoint/surface
- Preconditions and required authorization
- Exact reproduction steps (self-contained; reproducible without this system's
  internal context)
- Minimal test input/request needed to demonstrate the issue
- Benign control test
- Expected vulnerable vs. safe behavior
- Evidence to capture
- Safety limits and stop conditions
- Cleanup requirements
- Reporting notes

Use the generalized template at
`knowledge/human/verification-recipe-template.md`. Recipes are written in
technology-agnostic, class-level terms where the evidence permits.

## Verification outcome (deterministic)

```
Machine-confirmed
    → Verification Recipe Generation
    → HUMAN MANUAL VERIFICATION
        → PASS → finding remains confirmed → eligible for reporting
        → FAIL → not reproduced → not reportable → hypothesis reopened
```

### PASS — Human verified

- The finding remains **confirmed**.
- It is eligible for reporting subject to all existing reporting requirements
  (per `05-reporting.md`), including the mandatory human-verification outcome.

### FAIL — Not reproduced / verification failed

- The finding is **NOT reportable** and is **NOT** "human verified".
- Record the failure reason and any captured evidence; do **not** silently
  discard the finding.
- The finding does not silently retain a "confirmed" status without support; the
  hypothesis is **reopened at the appropriate testing stage** and re-tested with
  a control.
- The agent may **not** decide that the failed reproduction is acceptable, and
  must not unilaterally downgrade or preserve a "confirmed" status to bypass the
  failed gate.

## Hard rules

1. **A generated recipe is NOT proof of a vulnerability.** It is an instruction
   sheet for a human to verify something the system believes is confirmed. It
   never upgrades the status of a finding.
2. **Never automatically submit a bug-bounty report.** Manual human verification
   is a non-negotiable approval gate before any report is produced or submitted.
3. **Use the minimum necessary exploitation** to demonstrate the impact; the
   recipe must specify the smallest test input that establishes the issue.
4. **Preserve raw evidence separately** (under `evidence/reporting/raw/`). The
   recipe references raw evidence; it does not replace or duplicate it.
5. Recipes must be **reproducible and self-contained** — a human can follow them
   using only the recipe and raw evidence references, with no access to this
   system's working session.
6. Recipes must state **safety limits, stop conditions, and cleanup**
   requirements as first-class sections.
7. If a required section cannot be filled from evidence, mark it explicitly as
   unknown/not-applicable. Never invent inputs, responses, or impact.
8. Adding or changing this rule, the recipe template, the recipe generator
   (`work/verification_recipe_generator.py`), or its regression test
   (`work/test_verification_recipe.py`) requires human approval.
