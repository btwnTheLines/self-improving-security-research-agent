# AI Security Research System — Structure Index

Authorized ethical-security-research workspace. This is a **structure/README index
only**; it describes the layout. It does not authorize any action — the
behavioral contract lives in `.clinerules/`.

## Directory map

| Path | Role | Human- or machine-oriented |
| --- | --- | --- |
| `.clinerules/` | Binding behavioral rules: behaviour, scope, recon, testing, validation, reporting, self-improvement. Always govern. | Both |
| `knowledge/` | Reusable security knowledge (decision support, never authority). | `human/` human-readable; `machine/` token-efficient entries |
| `evidence/` | Records from completed assessments (recon, testing, reporting, self-improvement) + their raw artifacts. | Both |
| `reports/` | Draft/internal bug-bounty reports (human review; no submission). | Human |
| `work/` | Scratch / working artifacts captured during assessments. | Data |
| `findings/`, `labs/`, `programs/` | Empty organizational placeholders (intentionally preserved). | n/a |

## How the agent behaves

`.clinerules/` defines behaviour end-to-end:

- `00-core.md` — role, operating principles, evidence standard, human control.
- `01-scope.md` — authorized target, scope boundaries, per-environment scope.
- `02-recon.md` — reconnaissance method; observed vs self-reported config.
- `03-testing.md` — testing authorization, approval gates, minimum testing.
- `04-validation.md` — verifying generated artifacts, guardrail preservation.
- `05-reporting.md` — reproducible evidence, class-level framing, report gate.
- `006-self-improvement.md` — learning loop, generalization, human approval.

## Security knowledge

`knowledge/index.md` routes observed surface characteristics to the relevant
`knowledge/machine/<module>.md` entries. `knowledge/human/` holds the
human-readable playbook and the bug-bounty report template
(`knowledge/human/bug-bounty-report-template.md`). Tool capabilities live in
`knowledge/kali-wsl-capabilities.md` (machine-specific snapshot).

## Tools / capabilities

Capability manifests and selection principles are documented in
`knowledge/index.md` (tool selection) and `knowledge/kali-wsl-capabilities.md`
(what is actually installed).

## How testing works

Testing rules: `.clinerules/03-testing.md`. Per-class testing guidance: the
relevant `knowledge/machine/<module>.md` entry. Read-only/minimal probes without
approval; consequential testing requires human approval.

## How evidence is stored

`evidence/` subfolders: `recon/` (attack-surface characterization), `testing/`
(per-test records), `reporting/` (per-finding reports + `raw/` request/response
artifacts), `self-improvement/` (learning-loop records & this cleanup report).
See `evidence/README.md`.

## How reports are generated

Per `.clinerules/05-reporting.md`, using the template at
`knowledge/human/bug-bounty-report-template.md`. Drafts live in `reports/`.

## How self-improvement works

Rule: `.clinerules/006-self-improvement.md`. Learning-loop records:
`evidence/self-improvement/`.

## Completed assessments vs reusable knowledge

- **Completed assessments (data/records):** `evidence/`, `reports/`, `work/`.
- **Reusable system knowledge (reference):** `knowledge/`.
```