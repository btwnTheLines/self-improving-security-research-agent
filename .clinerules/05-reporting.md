# Reporting Rules

## Reproducible Evidence

Include the exact requests and responses used to establish a finding, and treat
request/response specifics as evidence to be preserved.

## Class-Level Framing

Frame impact and root cause in technology-agnostic, class-level terms (per
`04-validation.md`). Do not tie a finding to a single application or technology
unless the evidence does.

## Report Generation

Generate a submission-ready bug-bounty report only for a **confirmed** finding
(evidence demonstrates the claimed security impact, per `00-core.md` Evidence
Standard). Never invent evidence, impact, reproduction steps, or affected
behavior; keep observation / hypothesis / evidence / confirmed / impact /
uncertainty distinct within the report.

A machine/agent-confirmed finding is **NOT reportable** until the **HUMAN MANUAL
VERIFICATION** gate (per `06-verification.md`) has passed. A report must record
the human-verification outcome, one of: **Not verified** / **Human verified** /
**Verification failed — not reproduced**. "Confirmed" alone does not satisfy the
reporting prerequisite; only a finding that is **human verified** (or a stated
exception explicitly approved by the human operator) may be reported.

Use the generalized template at `knowledge/human/bug-bounty-report-template.md`,
covering: Title, Summary, Confirmation status, Affected component, Preconditions,
Steps to reproduce, Expected behavior, Actual behavior, Security impact,
Evidence / PoC, Remediation, Severity rationale, Limitations / uncertainty.

Every report is for human review before any external submission. Do not implement
or perform automatic bug-bounty submission. Reports stay application-agnostic and
do not weaken the scope, safety, approval, evidence, or stopping rules.
