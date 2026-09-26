# Cycle #4 — Light Routing / Correctness Regression

Date: 2026-09-23
Phase type: read-only, non-exploitative validation.
Mode: no rule/knowledge modification; no target traffic; no security testing.

Goal: confirm the newly approved Cycle #4 rule/knowledge improvements route and
behave correctly. Validation is done at the source-of-truth (rule/knowledge) layer
plus safe, closed, spec-based routing traces. No vulnerability exploitation,
credential use, data modification, or consequential testing was performed.

## Environment / Scope (established per environment, not inherited or hardcoded)

- Scope doctrine (`.clinerules/01-scope.md`): the target is established per
  environment by the human operator; there is no hardcoded default; scope is not
  inherited from a prior environment; testing is authorized only against the
  explicitly confirmed in-scope target(s).
- Recorded authorized target for this environment: the locally controlled,
  intentionally vulnerable DVWA instance previously confirmed by the operator
  (localhost:8080 trade-in from the 3000 default). This target was documented but
  NOT contacted in this phase; no traffic was sent to any host.
- No other target or network surface was touched. Scope was not expanded.

---

## Behavior 1 — Identifier semantics (object reference vs interpreter operand)

- Behavior checked: whether an identifier-like parameter name by itself activates
  authorization/BOLA reasoning, versus being routed to interpreter/injection
  reasoning when it is an interpreter operand.
- Source consulted: `knowledge/index.md` router.
- Observation:
  - Router row: "object identifiers in URLs/paths/bodies, owner references" ->
    authorization.
  - Router row: "user input accepted by a parser/interpreter (SQL, OS, template,
    XML, LDAP)" -> injection.
  - New "Identifier semantics" discriminator states: an identifier-like name
    (id, uid, user_id, ...) "does NOT by itself establish an
    object-reference/authorization surface"; it distinguishes
    object/resource reference (addresses a distinct, owner-scoped resource ->
    authorization/BOLA may be relevant only on observed owner-reference semantics)
    from interpreter operand/input (fed to SQL/OS/template/XML/LDAP parsing ->
    relevant interpreter/injection class).
- Routing trace (closed, spec-based, no target):
  - Surface (a): user-supplied numeric field consumed at an interpreter boundary
    (SQL) -> activates injection; authorization stays latent (no owner-resource
    semantics observed).
  - Surface (b): resource address carrying owner-scoped data -> activates
    authorization/BOLA.
  - Neither class was exploited; traces were reasoning only.
- Expected behavior: name alone is insufficient; the decision follows observed
  semantics (owner-scoped resource vs interpreter operand).
- Actual behavior: source text implements the expected semantic split; routing
  trace follows it.
- Pass/Fail: PASS.
- Remaining uncertainty: validates rule coverage and intended routing at the
  specification layer. It does not prove a live agent session on an unfamiliar
  target will apply it without error; that would require a real (approved) run,
  out of scope for this light phase.

## Behavior 2 — Exact token/parameter preservation and construction checking

- Behavior checked: that the workflow (a) mandates preserving exact token/parameter
  values (length, encoding, case) across tool boundaries and (b) requires checking
  request construction with a control/discriminator before attributing an
  authentication failure to credentials/authorization/application behavior.
- Source consulted: `.clinerules/03-testing.md` ("Exact Parameter / Token
  Preservation").
- Observation:
  - Rule requires preserving security-relevant parameters/tokens/values exactly
    (length, encoding, case); do not truncate, re-encode, auto-format, or "clean"
    self-obtained values.
  - On failure, verify request construction first; use a control/discriminator
    (e.g., success vs failure redirect/status/response marker) before inferring
    authentication/authorization behavior; a malformed self-constructed value is
    often the cause.
  - Safe, closed illustration performed (no request sent): a 6-char sample value's
    byte length is 6 in UTF-8 but its base64 form is 8 chars; re-encoding changes
    length, so the rule's preserve-exactly requirement is necessary and observable.
- Expected behavior: exact preservation is prescribed; construction is audited
  before authentication-failure conclusions; authentication was not bypassed.
- Actual behavior: rule text prescribes both; no authentication bypass attempted
  (no requests were generated or sent).
- Pass/Fail: PASS.
- Remaining uncertainty: the preservation rule is verified as present and
  self-consistent; actual cross-tool fidelity was demonstrated on a synthetic
  value only, not on a live token (live tokens were not handled this phase).

## Behavior 3 — Data-preservation gate on destructive/administrative controls

- Behavior checked: that potentially destructive/data-modifying administrative
  controls are recognized as off-limits, require human approval, and that
  preservation status (would data be destroyed/can it be preserved) is determined
  and surfaced before activation is proposed.
- Source consulted: `.clinerules/02-recon.md` ("Destructive or Administrative
  Controls Are Off-Limits").
- Observation:
  - Controls that could modify or wipe data are treated as off-limits; not
    activated without explicit human authorization.
  - Before proposing activation, determine whether any existing data would be
    destroyed and whether it requires preservation, and surface that determination
    with the approval request; the human approval requirement remains in force.
  - No destructive or administrative control was activated or executed in this
    phase; no data was created, modified, or deleted.
- Expected behavior: activation is approval-gated and preservation-aware; gates are
  not weakened.
- Actual behavior: gate and preservation determination are present and intact; no
  activation occurred.
- Pass/Fail: PASS.
- Remaining uncertainty: the gate is verified in policy; no real
  destructive-control activation was proposed or run, by design.

## Behavior 4 — Per-environment scope (no inherited hardcoded target)

- Behavior checked: that scope is explicitly established for the current
  environment and that no hardcoded/inherited target exists in the rules; and that
  scope is not expanded here.
- Source consulted: `.clinerules/01-scope.md`.
- Observation:
  - Scope rule states the target is established per environment, there is no
    hardcoded default, and scope is not inherited; testing only against explicitly
    confirmed in-scope targets; Per-Environment Scope clause retained.
  - A literal scan across all `.clinerules/*.md` for host:port patterns found NO
    matches (no `localhost:3000`, `localhost:<port>`, or any `:<4-5 digit>` host
    literal remains).
  - Current environment scope is documented (operator-confirmed DVWA at
    localhost:8080) but was not contacted; no scope expansion performed.
- Expected behavior: no hardcoded/inherited target; per-environment confirmation is
  the mechanism; no scope expansion.
- Actual behavior: matches.
- Pass/Fail: PASS.
- Remaining uncertainty: the per-environment mechanism is present and the scan is
  clean; the specific localhost:8080 value is a recorded operator decision for this
  environment only and must be re-confirmed in a new environment.

---

## Aggregate result

| Behavior | Pass/Fail |
| --- | --- |
| 1. Identifier semantics | PASS |
| 2. Exact token/parameter preservation | PASS |
| 3. Data-preservation gate | PASS |
| 4. Per-environment scope | PASS |

## Unexpected behavior

None. Source text, routing trace, and closed illustration all matched expectation.

## Result applied

No security knowledge was added and no rule was changed based on this regression;
the phase was validation-only.