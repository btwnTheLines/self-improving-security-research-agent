# Evidence Index

This folder holds records and raw artifacts from completed security assessments.
It is organized so evidence is easy to locate and to distinguish from reusable
system knowledge (which lives in `knowledge/`).

## Subfolders

| Path | Role |
| --- | --- |
| `recon/` | Attack-surface characterization and recon method applied per target. |
| `testing/` | Per-test records (hypothesis, request/response inputs, interpretation). |
| `reporting/` | Per-finding bug-bounty-style reports, plus `raw/` request/response artifacts backing them. |
| `self-improvement/` | Learning-loop records (reviews, approved improvements, regressions, and this cleanup report). |

## Reporting evidence convention

`evidence/reporting/<NN>-<finding>.md` reports reference exact artifacts under
`evidence/reporting/raw/`. Those raw files are the preserved request/response
evidence and must not be treated as disposable.