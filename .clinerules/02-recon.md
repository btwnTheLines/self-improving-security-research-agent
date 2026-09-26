# Reconnaissance Rules

## Context Before Pattern-Mining

When mining client bundles, code, or other artifacts for endpoints, message
formats, or identifiers, first inspect a small raw sample of the target strings
to learn their actual syntax before writing search or extraction logic.

Base extraction on the observed format, not on guessed patterns.

## Characterize the Environment First

Before treating endpoints, paths, or payloads as given, observe the application's
architecture (server-rendered, SPA, API-only, or hybrid), its data/interface
paradigm (REST, GraphQL, RPC, forms, WebSocket, etc.), content types, and how
inputs travel. Derive the approach from these observations, not from a prior
application or assumed technology.

## Delimit the Surface by Authentication State

When an application is gated by authentication and no valid session is
available, characterize the reachable (pre-authentication) surface completely
and record authentication-gated areas as explicit unknowns, including why they
were not observable.

Do not log in, create accounts, register, or probe authentication/authorization
bypasses during reconnaissance. Note that functionality or endpoints whose
presence cannot be confirmed are unknowns, not established facts.

## Distinguish Observed from Self-Reported Configuration

Separate configuration or version information you observe directly (for
example, in responses, headers, or page content the application actually
produces) from information the application merely reports about itself.

Treat application-reported or otherwise unverified configuration as unverified
observations, flag them as such, and corroborate them before relying on them
as a basis for later testing. Do not treat a self-reported version, feature
toggle, or stated defense as ground truth.

## Optional Static-Asset Sampling

To determine whether an application is server-rendered or client-side, sampling
one small, representative static asset (for example, a small stylesheet or
script) is an optional technique.

Do not treat sampling as a mandatory step, and do not download large application
assets unless necessary. Confirm rendering behavior with page structure and
responses rather than a single asset alone.

## Destructive or Administrative Controls Are Off-Limits

During reconnaissance, note any discovered destructive or administrative
control that could modify or wipe data, and treat it as off-limits.

Do not activate such controls during reconnaissance unless explicitly
authorized by the human operator.

Before proposing activation of any potentially destructive or data-modifying
administrative control, determine whether any existing data would be destroyed
and whether it requires preservation, and surface that determination with the
approval request. The human approval requirement remains in force.
