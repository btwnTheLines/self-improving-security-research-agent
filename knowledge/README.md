# Universal Security Knowledge Layer

An optional knowledge layer for the authorized ethical-security research
workflow. It **activates, structures, and routes** the model's existing
security knowledge; it does not teach security from first principles.

## Relationship to `.clinerules`

- `.clinerules/` are the **binding behavioral rules** (scope, safety, approval,
  evidence, stopping, human control). They always govern.
- This `knowledge/` layer is **decision support only**. It never authorizes an
  action.

> A technique being present here does NOT authorize its execution. Applicability
> is derived from observed evidence, within the authorized scope, and within the
> rules in `.clinerules/`.

## Layout

- `index.md` — compact knowledge **router**: observed surface characteristics →
  relevant modules, plus tool-selection principles.
- `machine/` — token-efficient, model-oriented class entries (compact notation).
  Load only modules relevant to the observed attack surface.
- `human/universal-security-testing-playbook.md` — human-readable playbook
  (reasoning model, taxonomy, testing/confirmation/tool-selection principles,
  Kali integration, limitations, self-improvement).
- `kali-wsl-capabilities.md` — environment-specific capability manifest,
  Windows/WSL boundary, and concrete WSL2 invocation. It is deliberately scoped
  to this machine and is only about **tools**, not vulnerability reasoning.

## How to use (token-efficient)

1. Establish scope and characterize the environment (per `.clinerules`).
2. From **observed** surface characteristics, consult `index.md` to select the
   relevant module(s). Do not load all modules.
3. Use module entries to structure observation → hypothesis → test → confirm.
4. Choose tools via `index.md` (tool selection) and `kali-wsl-capabilities.md`
   (what is actually available). Least-powerful tool that answers the question.
5. Treat a positive finding as a hypothesis until validated per `.clinerules`.

## Guardrails (non-negotiable)

- Knowledge never expands scope, never bypasses approval, never licenses
  destructive or out-of-scope action.
- Applicability is always determined from observed evidence, not from the
  taxonomy.
- The taxonomy is not a checklist to force onto every target.