# Verification Recipe Template (Human-Readable)

A generalized, application-agnostic template for producing a **verification
recipe** for a confirmed finding. The recipe is a human-executable instruction
sheet created **before** a report is produced, and it is the manual-verification
gate. It is a decision-support asset in the `knowledge/` layer — it does not
authorize testing, does not prove a vulnerability, and does not submit reports.
The behavioral contract (evidence standard, approval gates, stopping) is
`.clinerules/`.

The mandatory workflow is defined in `.clinerules/06-verification.md`:

```
Recon → Hypothesis → Automated Test → Differential Validation → Confirmed Finding
      → Verification Recipe Generation → HUMAN MANUAL VERIFICATION
      → Evidence Review → Report
```

## Must-be-explicit status banner

Every recipe MUST begin with this banner:

```
⚠️ THIS RECIPE IS NOT PROOF OF A VULNERABILITY.
It is an instruction sheet for a human to verify a finding the system believes is
confirmed. A human must manually reproduce and validate the finding before it may
be reported. This system never submits bug-bounty reports automatically.
```

## Evidence discipline

- The recipe is generated **only** for a **confirmed** finding (evidence
  demonstrates the claimed security impact, per `.clinerules/00-core.md`).
- The recipe references, and never replaces, raw request/response evidence, which
  is preserved under `evidence/reporting/raw/`.
- Distinctions remain explicit throughout: Observation / Hypothesis / Evidence /
  Confirmed vulnerability / Impact / Uncertainty.
- Never invent inputs, responses, impact, or affected behavior. If a field cannot
  be filled from evidence, mark it clearly as unknown/not-applicable.
- Use the minimal test input that demonstrates the issue.

---

# Recipe

## 0. Status banner
Mandatory banner above (never omitted, never weakened).

## 1. Recipe identification
- Recipe ID
- Source finding report (path) and confirmation status
- Date and generator version used to emit this recipe

## 2. Finding and vulnerability class
Short class-level description (technology-agnostic) plus the specific finding.

## 3. Target endpoint/surface
The specific function/page/endpoint and its role, stated from evidence.

## 4. Preconditions and required authorization
Authentication state, role/privilege, environment, message format, order of
operations, and the exact authorization under which reproduction is permitted.

## 5. Exact reproduction steps
Ordered, self-contained steps. A human must be able to follow them using only
this recipe and the raw evidence references — no internal session context.

## 6. Minimal test input/request
The smallest request/input that demonstrates the issue, exact and complete
(method, path, parameters, headers, body, tokens exactly as used).

## 7. Benign control test
The paired minimal control (e.g., well-formed benign input) that makes the
vulnerable result meaningful; record both probe and control.

## 8. Expected vulnerable vs. safe behavior
State what the application does when vulnerable and what it would do if the
control were correct, in class-level terms.

## 9. Evidence to capture
Exactly what to record during verification (raw artifacts, key response fields,
HTTP status, markers) and the raw-evidence file paths that already exist.

## 10. Safety limits and stop conditions
Explicit in-scope boundary, no-fly actions (no external traffic, no DoS, no
destructive actions), and conditions under which the human must STOP (scope
escape, unexpected external contact, sufficient evidence reached).

## 11. Cleanup requirements
Any lab data, files, or records created during reproduction that must be removed
or flagged afterward.

## 12. Reporting notes
Class-level framing guidance, severity rationale constraints, and what remains
uncertain/undemonstrated (to be carried into any report).
