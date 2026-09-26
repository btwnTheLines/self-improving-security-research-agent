# Universal Security Testing Playbook (Human-Readable)

A plain-language companion to the machine knowledge layer. It explains *how the
agent thinks and operates* so an operator can review, steer, and audit the
workflow. It is **not** an exhaustive security textbook and it never authorizes
an action — the behavioral contract is `.clinerules/`.

Reading map:
- Reasoning model → §1
- Taxonomy → §2
- Testing & stopping principles → §3
- Test-input (payload) generation → §4
- Confirmation → §5
- Tool selection & Kali → §6
- Limitations → §7
- Self-improvement → §8

---

## 1. Reasoning model

The agent moves through distinct, explicitly-labelled phases:

```
scope → characterize → surface → hypothesis → test → validate → evidence
→ verification-recipe → human-verification → report → learn
```

Each phase respects the rules in `.clinerules/`:
- Scope is established per environment; nothing is assumed authorized.
- The application is characterized from observed behavior, not from prior
  applications (P1). Pre-auth surface is fully mapped; authenticated-only areas
  become explicit **unknowns** (U-A). Self-reported configuration is flagged as
  unverified (U-B).
- Every finding keeps the **observation / hypothesis / evidence / confirmed**
  distinction. A tool result or an unexpected response is never, by itself,
  a vulnerability.
- Every **confirmed** finding is followed by a **Verification Recipe** (see §5)
  that a human manually verifies before any report is produced. The recipe is an
  instruction sheet, not proof, and reports are never auto-submitted.

## 2. Taxonomy

Security classes are stored in `knowledge/machine/<module>.md` and routed from
`knowledge/index.md`. The taxonomy organizes thinking; it is **not a checklist**
imposed on every target. Applicability is decided from observed evidence.

Modules:
injection · client · authentication · authorization · web · files · api ·
business-logic · configuration · protocol · modern-apps · cloud

## 3. Testing & stopping principles

- **Minimum necessary testing**: use the smallest test that can resolve the
  question; STOP when sufficient evidence exists.
- **Least impact**: prefer read-only and minimal non-destructive tests.
- **Human approval gate**: consequential actions (auth bypass, authorization
  bypass, privilege escalation, another user's data, destructive actions, data
  modification, credential attacks, availability impact, exploit execution,
  uncertain safety) require human approval first. The knowledge layer cannot
  bypass this.
- **Stop conditions**: on scope escalation (new host/domain/application), stop
  and ask; on sufficient evidence, stop; do not maximize exploitation.
- **Destructive/admin controls** discovered during recon are off-limits unless
  explicitly authorized (U-D).

## 4. Test-input (payload) generation

The agent **generates** test inputs; it does not cycle a payload dictionary.

General process:

```
observed input → context → parser/interpreter → transformation/encoding
→ baseline → minimal discriminating test → response → interpretation
→ adaptation → confirmation → minimum-impact proof
```

Principles:
- Start from the observed input and the surrounding context (location, type,
  content type, encoding, parser behavior).
- Use a **baseline** and a **control** so a negative is informative.
- Adapt only when evidence shows the current test is insufficient; do not
  escalate complexity without cause.
- The model's internal security knowledge supplies plausible probes for the
  observed grammar; verification comes from the response, not from the probe
  succeeding.

## 5. Confirmation

A vulnerability is not confirmed by a payload or tool output alone. The agent
must validate the claimed security impact:
- hypothesis, test, request/input, response/observation, interpretation,
  confidence, remaining uncertainty.
- Pair probes with controls; confirm the *effect* is real and attributable.
- The human operator makes the final validity determination.

### Verification recipe and the human gate

Once a finding is **confirmed**, the agent generates a **Verification Recipe** —
a self-contained, human-executable instruction sheet (per
`knowledge/human/verification-recipe-template.md` and `.clinerules/06-verification.md`)
covering: finding/class, endpoint, preconditions, exact reproduction steps, the
minimal test input, a benign control, expected vulnerable vs safe behavior,
evidence to capture, safety limits/stop conditions, cleanup, and reporting notes.

- The recipe is an instruction sheet for a human; it is **not proof** and never
  changes a finding's status.
- A human must **manually verify** the finding against the recipe before any
  report is produced or submitted.
- Reports are **never** submitted automatically.
- Raw request/response evidence is preserved separately (in `evidence/reporting/raw/`)
  and referenced, not duplicated.
- Recipes are reproducible from the recipe and raw evidence alone, without access
  to this system's internal working session.

## 6. Tool selection & Kali integration

- Selection principle: use the **least powerful tool that can answer the
  current question**. Tool availability does not imply authorization.
- Tools are chosen by surface, information required, scope, authorization,
  risk, efficiency, expected information gain, and existing evidence.
- Kali (WSL2) is an execution/tooling layer. The playbook describes
  **capabilities conceptually** (`HTTP_ANALYSIS`, `SERVICE_DISCOVERY`,
  `CONTENT_DISCOVERY`, `DATA_PROCESSING`, `PROXY/INTERCEPTION`, `SCRIPTING`);
  the router (`knowledge/index.md`) and the capability manifest
  (`knowledge/kali-wsl-capabilities.md`) map capability → installed tool.
- The playbook never says "always use Kali." It says: choose the appropriate
  capability, then the appropriate tool for the in-scope, authorized question.
- Burp is a Windows-side capability, selected when interception/replay/
  comparative analysis is useful — still subject to the same scope and approval
  rules.

## 7. Limitations

- The knowledge layer is decision support, not authority. It does not expand
  scope and cannot authorize.
- The taxonomy routes; evidence decides. Do not force classes onto a target.
- Capability manifests are machine-specific snapshots; tools must be discovered,
  not assumed.
- Machine entries are compressed for token efficiency; they assume the model's
  underlying security knowledge and are not a substitute for care or evidence.

## 8. Self-improvement

The learning loop improves both behavior/workflow and security knowledge:

```
observe → problem/success → general lesson → proposed change → human approval
→ update → regression test → cross-environment test
```

- Do not turn a target-specific endpoint or payload into a rule.
- Prefer generalized classes: "when this class of boundary exists, consider…",
  not "always test this exact endpoint".
- Rules and knowledge changes require human approval and must preserve the
  safety, scope, approval, evidence, and stopping guardrails.