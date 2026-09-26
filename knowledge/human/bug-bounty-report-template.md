# Bug-Bounty Report Template (Human-Readable)

A generalized, application-agnostic template for producing submission-ready,
evidence-backed vulnerability reports from confirmed findings. It is a decision
support asset in the `knowledge/` layer — it does not authorize testing and does
not submit reports. The behavioral contract (what may be tested, evidence
standards, approval, stopping) is `.clinerules/`.

## Confirmation gate

A report is generated **only** for a **confirmed** finding. "Confirmed" means the
evidence demonstrates the claimed security impact actually exists, per the
evidence standard in `.clinerules/00-core.md`. If a finding is only an
observation, hypothesis, or evidence-lacking suspicion, it is **not** reported as
a vulnerability; it is recorded as such (e.g., in an assessment log / hypotheses
list).

Reporting also requires that the **HUMAN MANUAL VERIFICATION** gate (per
`.clinerules/06-verification.md`) has passed. A machine/agent-confirmed finding is
**NOT reportable** until a human has manually reproduced and validated it.

## Human verification outcome (required)

Every report must record exactly one outcome for the human-verification gate:

- **Not verified** — no human manual verification has (yet) been performed;
  the finding is not reportable.
- **Human verified** — a human manually reproduced and validated the finding;
  reportable subject to all other reporting requirements.
- **Verification failed / not reproduced** — human reproduction did not confirm
  the finding; it is not reportable and should be re-opened at the test stage.

## Evidence hierarchy (label explicitly inside the report)

Use exactly one of these statuses for the finding and keep the categories
distinct throughout:

- **Observation** — something directly seen (a response, header, page, field).
- **Hypothesis** — a proposed explanation not yet confirmed.
- **Evidence** — request/response pairs and other concrete artifacts collected.
- **Confirmed vulnerability** — evidence supports the claimed security impact.
- **Impact** — the real, supported security consequence, not maximum theoretical.
- **Uncertainty / limitations** — what remains unknown or unverified.

Never invent evidence, impact, reproduction steps, or affected behavior. If a
field cannot be filled from evidence, mark it clearly as unknown/not-applicable.

## Reproduction evidence

Include the exact requests and responses used (method, path, parameters, headers,
tokens, body) so the finding is reproducible and verifiable. Treat these
specifics as evidence to be preserved.

## Submission readiness (human review gate)

- This report must be read and approved by a human operator before any external
  submission to a bug-bounty platform.
- This system never performs automatic (API/automated) submission. The human
  operator owns all final submission decisions and actions.

---

# Report

## 1. Title
Short, class-level, descriptive. Example pattern: `<Class>: <component>`. No
target-specific jargon unless the evidence requires it.

## 2. Summary
1–3 sentences: the class of weakness, where it occurs, and the supported impact.

## 3. Confirmation status
One of: Observation / Hypothesis / Evidence / **Confirmed vulnerability** / Impact.

## 3a. Human verification outcome
One of: **Not verified** / **Human verified** / **Verification failed — not reproduced**
(required per `.clinerules/06-verification.md` and `.clinerules/05-reporting.md`).
A finding that is not "Human verified" must not be presented as report-ready.

## 4. Affected component
The specific function/page/endpoint and its role in the application, stated from
observed evidence (not a guessed stack).

## 5. Preconditions
The conditions required to reproduce (authentication state, role, security
settings, input values, order of operations).

## 6. Steps to reproduce
Ordered, concrete, reproducible steps. Each step states the exact request/input
sent and the expected response. Use evidence-grounded specifics.

## 7. Expected behavior
What the application should do if the control were correct (state this in
class-level, technology-agnostic terms).

## 8. Actual behavior
What was observed, with the evidence. Distinguish this from the expected.

## 9. Security impact
The real, evidence-supported impact. State supported impact only; mark
speculative or unexercised impact as theoretical/not-demonstrated.

## 10. Evidence / PoC
Exact request → response pairs, sanitized only where necessary (never alter the
security-relevant payload/parameters/tokens). Label each as observation, and note
the control used to make the result meaningful.

## 11. Remediation
Class-level fix guidance (e.g., parameterization, context-safe output encoding,
server-side authorization, input validation), stated application-agnostically.

## 12. Severity rationale
Reasoned severity based on: preconditions, exploitability as demonstrated,
supported impact, and any mitigating factors. Acknowledge what was not exercised.

## 13. Limitations / remaining uncertainty
What was not tested (and why), what is unverified, and anything that could change
the conclusion.