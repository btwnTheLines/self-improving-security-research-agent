# Knowledge Router / Index

Router: from **observed** surface characteristics, select the relevant class
module(s). Adaptive — do not assume a technology merely because a pattern is
common. Confirm applicability from evidence before using a module.

## Surface → Module routing

| Observed surface characteristic | Activate module(s) |
| --- | --- |
| auth/session flow, login, tokens, password reset, MFA | authentication |
| object identifiers in URLs/paths/bodies, owner references | authorization |
| user input accepted by a parser/interpreter (SQL, OS, template, XML, LDAP) | injection |
| HTML/JS/URL reflection of input, storage of attacker text | client |
| CSRF-relevant state-changing requests, link/redirect handling, outbound URL fetch | web |
| file upload/download, parse of uploaded content | files |
| structured/JSON interface, GraphQL, request schema | api |
| multi-step flows, order/state, values, idempotency | business-logic |
| headers, frameworks, debug/version exposure, secrets | configuration |
| network/service surface in scope, TLS/protocol behavior | protocol |
| SPA/client app, browser storage, WebSockets | modern-apps |
| cloud object storage, IAM, metadata, management interfaces | cloud |
| multiple of the above | activate the intersection; keep only evidence-supported classes |

Cross-cutting: any observed **owner-scoped object reference** also routes to
authorization — an identifier *name* alone does not (see "Identifier semantics"
below); any interpreter input also routes to injection; any auth flow also
routes to session/token concerns in authentication.

## Confirmed-finding routing (workflow stage)

A finding that reaches **confirmed** routes to two subsequent workflow stages,
not to further class modules: (1) **Verification Recipe Generation** — emit a
self-contained, human-executable recipe per
`knowledge/human/verification-recipe-template.md` and
`.clinerules/06-verification.md`; (2) **HUMAN MANUAL VERIFICATION** — a human
reproduces and validates the finding before any report. The recipe is an
instruction sheet, not proof; reports are never auto-submitted.

Identifier semantics: an identifier-like parameter name (id, uid, user_id, ...)
does NOT by itself establish an object-reference/authorization surface.
Distinguish: object/resource reference (addresses a distinct, owner-scoped
resource; responses may vary per reference) -> authorization/BOLA may be relevant;
interpreter operand/input (fed to SQL/OS/template/XML/LDAP parsing) -> route to the
relevant interpreter/injection class. Activate authorization only on observed
owner-reference semantics, not on the parameter name.

## Self-reported configuration is not evidence

Treat any application-reported identity, version, or claimed security/feature
level as unverified unless corroborated. Do not route or reason on it as fact;
flag it as unverified and corroborate it before relying on it. This
cross-references - it does not restate - the recon rule
`.clinerules/02-recon.md` "Distinguish Observed from Self-Reported Configuration"
(U-B), and applies it at the activation/reasoning step as well as at
characterization.

## Tool selection (least powerful tool that answers the question)

- Availability does not imply authorization.
- Choose by: observed surface, information required, scope, authorization, risk,
  efficiency, expected information gain, existing evidence.
- Order: start passive/read-only; escalate only with evidence the current
  question is not answered, and only within scope/approval.

| Capability | Typical tools |
| --- | --- |
| HTTP_ANALYSIS | curl, wget, Python, Burp, browser |
| SERVICE_DISCOVERY | nmap (in-scope only) |
| CONTENT_DISCOVERY | ffuf (authorized, in-scope) |
| DATA_PROCESSING | jq, grep/sed/awk, Python |
| PROXY/INTERCEPTION | Burp (Windows) |
| SCRIPTING | Python, Bash |

See `kali-wsl-capabilities.md` for what is actually installed.

## Module index

injection · client · authentication · authorization · web · files · api ·
business-logic · configuration · protocol · modern-apps · cloud

Machine entry format used in `machine/<module>.md`:
`ID · WHEN · SURFACE · OBSERVE · HYPOTHESIS · TEST · ADAPT · CONFIRM · IMPACT ·
STOP · TOOLS · RELATED`. Fields are omitted when they do not contribute.

## Boundaries

- This is the router, not a checklist. Do not force every class onto a target.
- Human readable deep description: `human/universal-security-testing-playbook.md`.