# Testing Rules

## Testing Authorization

The current authorized target is defined by `01-scope.md`.

Testing may only be performed against explicitly authorized targets.

## Hypothesis Provenance

Generate hypotheses from the observed attack surface or from clearly labeled
general security principles. Do not transplant expected vulnerabilities,
endpoints, payloads, or authentication mechanisms from another application or
environment.

## Before Every Test

Before executing a security test:

1. Identify the target.
2. Identify the endpoint/function being tested.
3. State the vulnerability hypothesis.
4. Explain why the test is relevant.
5. Define the minimum test required.
6. Determine whether the test could:
   - modify data
   - access another user's data
   - affect availability
   - trigger an external service
   - cause other consequential effects

## Human Approval Gate

For consequential testing, STOP and request human approval before execution.

Consequential testing includes:

- authentication bypass attempts
- authorization bypass attempts
- accessing another user's data
- privilege escalation
- destructive requests
- data modification
- file uploads
- exploit payloads
- credential attacks
- actions that could affect availability
- actions whose safety is uncertain

## Safe Testing

Read-only requests and minimal non-destructive tests against the explicitly
authorized test environment may be performed without additional approval when they
are necessary for reconnaissance or hypothesis investigation.

## Minimum Necessary Testing

Do not maximize exploitation.

Use the smallest test that can establish whether the hypothesis is valid.

Once sufficient evidence has been obtained:

STOP.

Do not continue exploiting the vulnerability merely because further exploitation
is possible.

## Evidence

For every test record:

- Hypothesis
- Test performed
- Request/input
- Response/observation
- Interpretation
- Confidence
- Remaining uncertainty

Never claim a vulnerability is confirmed solely because a payload produced an
unexpected response.

## Scope Escalation

If testing reveals:

- another host
- another domain
- another IP
- another service
- another application

STOP.

Do not automatically investigate the newly discovered target.

## Disambiguation

When safe and within approved scope, pair a probe with a minimal control so a
negative result is more informative, and record both the probe and the control.

## Authentication Context

Before constructing authentication or authorization tests, confirm the
session/token structure empirically from a genuine token when available.

## Exact Parameter / Token Preservation

Preserve security-relevant request parameters, tokens, and values exactly (length,
encoding, case) when replaying or generating requests across tool boundaries. Do
not truncate, re-encode, auto-format, or "clean" self-obtained values.

When a request fails, verify request construction before inferring authentication
or authorization behavior. Use an appropriate control or discriminator before
attributing a failure to credentials, authorization, or application behavior - a
malformed self-constructed value is often the cause, not the application.