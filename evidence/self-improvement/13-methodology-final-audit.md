# Final Methodology Audit — 13-methodology-final-audit

Date: 2026-09-30
Phase type: read-only audit. No rule, knowledge, index, case-study, workflow, or
evidence modification. The ONLY file changed by this phase is this audit record.

## 1. Scope of audit

Verify that `knowledge/machine/methodology.md` (the cross-cutting,
case-study-distilled methodology module created from the five case-study
syntheses) fits cleanly into the existing security-testing agent system, across
six dimensions: duplication, conflicts, over-engineering, generalization
quality, routing, and architecture simplification. Audit only — findings are
reported; no changes are made. Any simplification opportunities are recorded for
future, human-approved action and are NOT applied here.

## 2. Files inspected

- `knowledge/machine/methodology.md` (new, under audit)
- `knowledge/index.md` (router) and `knowledge/machine/index.md` (module index)
- All twelve class modules in `knowledge/machine/`: api, authentication,
  authorization, business-logic, client, cloud, configuration, files,
  injection, modern-apps, protocol, web
- All `.clinerules/*.md`: 00-core, 006-self-improvement, 01-scope, 02-recon,
  03-testing, 04-validation, 05-reporting, 06-verification
- Prior audit/self-improvement artifacts (for format): 12-cycle4-light-routing-regression,
  13-documentation-structure-cleanup
- Case-study analyses selectively, only to resolve the provenance of two
  questionable lessons: the "universal reflector (TRACE)" pattern and the
  "never automate destructive deletion (PURGE)" guidance (CS5 and CS2).

## 3. Duplication findings

Each methodology lesson was compared against `.clinerules/`, `knowledge/index.md`,
the module index, and the class modules.

1. **Differential-with-control** (methodology principle #2)
   Substantially duplicates `.clinerules/03-testing.md` "Disambiguation" (pair a
   probe with a minimal control) and is already encoded in every class module's
   `TEST` field ("...with control"). Three independent homes for the same rule.
   Classification: **unnecessary duplication** — reduce to a cross-reference to
   `03-testing.md` (the observed-response-difference nuance can live as a one-line
   rationale). **Confirmed.**

2. **Self-reported config / docs / "patched" advisories are unverified**
   (principle #4) Duplicates `.clinerules/02-recon.md` (U-B "Distinguish Observed
   from Self-Reported Configuration") AND the dedicated
   `knowledge/index.md` "Self-reported configuration is not evidence" section (which
   itself cross-references U-B). This is a third framing of the same rule, and the
   principle even acknowledges it "aligns with 02-recon". Classification:
   **unnecessary duplication** — collapse to a pointer to `02-recon.md` (or drop from the
   module; the router already enforces it). **Confirmed.**

3. **Confirm behavior before assigning an impact class** (principle #3)
   Restates `.clinerules/00-core.md` Evidence Standard and `03-testing.md` Evidence
   ("Never claim a vulnerability is confirmed solely because a payload produced an
   unexpected response"). Same intent. Classification: **harmless reinforcement**
   (a rhetorical restatement; adds no behavior). **Confirmed.**

4. **Enumerate, don't guess** (principle #9)
   Overlaps `.clinerules/03-testing.md` "Hypothesis Provenance" (derive hypotheses
   from observed surface, do not transplant expected vulns) and `02-recon.md`
   "Characterize the Environment First" / "Context Before Pattern-Mining".
   Classification: **harmless reinforcement** (near-duplicate of Hypothesis
   Provenance). **Confirmed.**

5. **Separate primitive detection from impact confirmation / stage by collateral**
   (principle #5) Overlaps `03-testing.md` "Human Approval Gate" and "Minimum
   Necessary Testing" and `02-recon.md` off-limits controls, but adds a genuinely
   novel "staging" framing (collateral-phase ordering) not stated elsewhere.
   Classification: **harmless reinforcement** (novel nuance; consistent, not
   redundant). **Confirmed.**

6. **Reversibility and containment** (technical pattern)
   Overlaps `02-recon.md` (off-limits controls) and `03-testing.md` (minimum
   necessary, non-destructive). The specific "never automate destructive deletion
   (PURGE)" guidance is well-grounded — CS2 explicitly notes PURGE is "not suitable
   for automation due to the race and threat to other users". Classification:
   **harmless reinforcement** (adds the canary/identifier-isolation nuance). **Confirmed.**

7. **Audit your tooling** (principle #10)
   Overlaps `knowledge/index.md` "Tool selection" and `03-testing.md` "Exact
   Parameter / Token Preservation", but adds the oracle-false-positive nuance not
   cleanly stated elsewhere. Classification: **harmless reinforcement**. **Confirmed.**

8. **Trust-boundary reasoning** (principle #1)
   Generalizes WEB-TRUST / BUS-TRUST / CLOUD-TRUST / PROTO-HTTP. It is a
   cross-cutting lens over existing class modules, not a per-class restatement.
   This is the intended (non-redundant) function. Classification: **harmless
   reinforcement** / no real duplication. **Confirmed.**

9. **Chain-an-benign-gadget, primitive-as-open-problem, pivot-on-constraint,
   cross-user-via-shared-state** (principles #6,7,8,11) and the resolver/forcing
   oracle, OAST callback, boolean oracle, framing-differential, cache-oracle,
   universal-reflector, execution-precondition patterns are genuinely new — no
   equivalent exists in `.clinerules/` or the class modules.
   Classification: **no duplication**. **Confirmed.**

## 4. Conflict findings

No direct contradictions with scope, authorization, human approval, evidence
standards, stopping conditions, tool selection, hypothesis formation, or testing
behavior were found.

1. **Scope / authorization** — The module repeatedly bounds itself ("Decision
   support only. It never authorizes an action"; applicability "within the
   authorized scope"). The OAST guidance ("keep the callback host inside the
   authorized scope") is consistent with `01-scope.md` (no external callouts) and
   with WEB-SSRF (in-scope marker). No conflict. **Confirmed.**
2. **Human approval** — The "Safety and approval" section explicitly gates
   cache-poisoning, credential-leak, out-of-scope/internal, crash, persistent-state,
   and persistence-of-attacker-content tests behind `03-testing.md` human approval.
   This matches (does not weaken) the Human Approval Gate. **Confirmed.**
3. **Evidence standards** — "Confirm behavior before impact class" and the
   "confirmed vs impact" distinction match `00-core.md` and `03-testing.md`
   evidence rules. No weakening. **Confirmed.**
4. **Stopping / minimum necessity** — Staging-by-collateral and reversibility
   guidance align with Minimum Necessary Testing and 02-recon off-limits; the
   module does not encourage fuller exploitation. **Confirmed.**
5. **Hypothesis formation / testing behavior** — "Enumerate, don't guess" and
   "derive hypotheses from the observed multi-tier architecture" agree with
   `03-testing.md` Hypothesis Provenance. **Confirmed.**
6. **Apparent-risk item checked** — Principle #11 ("shared server state is a
   natural delivery channel") could superficially appear to encourage cache use,
   but it is paired in the same module with an explicit approval gate and with
   WEB-TRUST's `STOP: no caches of real users poisoned`. No conflict. **Confirmed.**
7. **Precedence** — The module explicitly defers to `.clinerules/` and states it is
   not a license; there is no precedence ambiguity. It adds no rule whose purpose
   is to override an existing rule (per `006-self-improvement.md`). **Confirmed.**

Overall conflict finding: **no substantive conflicts.** **Confirmed.**



## 5. Over-engineering findings

1. **"Redundant lessons (consolidation signal)" section** is review/provenance
   metadata with no runtime decision value. Every principle above it already cites
   the supporting cases in its own parenthetical, and the module's "Sources"
   section repeats the provenance. Showing which case supports which lesson teaches
   the agent nothing operational; it is a synthesis-quality record, not guidance.
   Classification: **over-engineering for a runtime knowledge module** — remove, or
   move this content into the audit/review record (as this file does). **Confirmed.**
2. **"Sources" section with provenance tags** is low-runtime-value review metadata;
   a runtime module needs only a one-line pointer to the case-study directory.
   Classification: **mild over-engineering**, trimmable. **Likely.**
3. **"Case-specific details — NOT general knowledge" section** is a justified
   guardrail (prevents payload/host/CVE transplant), but it largely repeats
   `02-recon.md` / `03-testing.md` Hypothesis Provenance and `006-self-improvement.md`
   generalization. Keep as a light reminder; do not let it grow. Not over-engineered
   on its own. **Likely** (mild redundancy, acceptable).
4. **Replication risk** — If this "consolidation counts + provenance" pattern is
   copied into every future synthesis module, accumulation would become
   over-engineering. Recommend containing this pattern to review records, not
   runtime modules. **Confirmed** (forward-looking).

Net: the principle/pattern content is appropriately scoped (11 + 8 entries, terse);
the over-engineering is confined to the meta/provenance sections. **Confirmed.**

## 6. Generalization findings

1. **Well-generalized (Confirmed):** differential-with-control; trust-boundary
   reasoning; behavior-before-impact; self-reported-not-evidence; staging-by-
   collateral; chain-a-benign-gadget; enumerate-don't-guess; pivot-on-constraint;
   audit-tooling (principle); resolver/forcing oracle; OAST callback; boolean
   oracle with control; framing differential; reversible/contained testing. These
   are technology-agnostic reasoning/test-construction principles.
2. **Universal reflector (TRACE)** — the *principle* (look for a universal echo
   when no app-level reflector exists) generalizes (**Confirmed**). The concrete
   TRACE mechanism is one HTTP-specific instance (**Confirmed** origin: CS5,
   PortSwigger, 2024). TRACE is frequently disabled and not guaranteed to exist;
   the module itself marks it as an example. Hold it as illustrative, not an
   assumed-available gadget. **Likely** overall.
3. **Primitive-without-impact-as-open-problem** — sound principle but supported
   primarily by a single case (CS5: universal reflector + cache-as-delivery).
   Multi-case corroboration is lacking, so generalization confidence should be
   kept **provisional** pending re-validation on another class. **Uncertain**
   (funding strength), principle itself reasonable.
4. **Cache oracle** — derived mainly from CS2 (web-cache entanglement). The oracle
   concept generalizes to any caching/intermediary layer, so the class-tie is mild
   and acceptable. **Likely.**
5. **Execution-precondition (content-type for execution)** — generalizable to any
   output/execution context; the "XSS under text/html" example is class-illustrative
   but not restrictive. **Confirmed.**
6. **No case-specific leakage** — the module does not carry forward hosts, exact
   endpoints, parameter names, CVEs, or vendor claims; it explicitly excludes them
   and uses only vulnerability-class and protocol terms (desync, TRACE, PURGE,
   HIT/MISS, CT/TE). One borderline item: the literal method name "PURGE" appears,
   but it is used to illustrate "destructive deletion," not as a payload. **Confirmed.**

## 7. Routing findings

1. `knowledge/index.md` positions methodology as cross-cutting, consulted alongside
   an activated class module, and explicitly "decision support, not a license." This
   matches the module's own header. **Confirmed.**
2. `knowledge/machine/index.md` lists the 12 class modules, then names methodology
   separately as cross-cutting ("consult alongside any activated class module, not
   instead of it"). Consistent with the router; no circularity. **Confirmed.**
3. Minor redundancy: `knowledge/index.md` references methodology in TWO places —
   the cross-cutting paragraph (lines ~28-32) and the "Module index" (~86-88). Not
   confusing, but a single canonical cross-reference would be cleaner. **Likely**
   (cosmetic).
4. No routing activation is duplicated or delegated to methodology; the class
   modules remain the primary routing targets. **Confirmed.**

## 8. Simplification opportunities

Reported only — NOT applied in this audit.

1. **Remove or relocate the "Redundant lessons (consolidation signal)" section**
   from `methodology.md` to the review record; it is provenance metadata, not
   agent guidance. (Over-engineering finding #1.) **Confirmed.**
2. **Collapse principle #4 (self-reported config)** to a pointer to `02-recon.md`
   U-B and the existing `knowledge/index.md` section; it is a third restatement.
   **Confirmed.**
3. **Collapse principle #2 (differential-with-control)** to a pointer to
   `03-testing.md` Disambiguation, keeping only the response-observation rationale.
   **Confirmed.**
4. **Consolidate the two methodology references** in `knowledge/index.md` into one
   canonical placement. **Likely.**

5. **Trim the "Sources"/provenance section** to a one-line pointer to
   `knowledge/case-studies/`. **Likely.**
6. **No class-module merges/archival** — the twelve class modules are unchanged and
   methodology is genuinely additive (it fills the previously-absent cross-cutting
   layer). No top-level architectural consolidation is warranted. **Confirmed.**

## 9. Required fixes

None. All duplication/over-engineering findings in sections 3, 5, and 8 are
optimization items (cross-referencing and trimming), not correctness or safety
defects. The module:
- does not weaken scope, approval, evidence, stopping, or non-destructive rules;
- introduces no contradiction with `.clinerules/` or any class module;
- routes correctly and is genuinely additive.

No required fix is outstanding. If optimization is desired, it must be performed
as a separate, human-approved maintenance pass (never automatically), consistent
with `006-self-improvement.md`. **Confirmed.**

## 10. No-change findings

- This audit changed only `evidence/self-improvement/13-methodology-final-audit.md`
  (this file). No `.clinerules/`, `knowledge/`, case-study, or existing-evidence
  file was modified. Verified via `git status` (below). **Confirmed.**
- No rule or knowledge change is required by this audit. **Confirmed.**
- The module's provisional lessons (TRACE illustration; single-case
  primitive-as-open-problem) are advisory, not unsafe, and need no urgent action. **Confirmed.**

## 11. Final assessment

`knowledge/machine/methodology.md` fits cleanly into the existing system. It is
safe, consistent with every guardrail, correctly and non-circularly routed, and
fills a genuine cross-cutting gap. The audit surfaced only minor duplication of
already-enforced rules (self-reported config, differential-with-control), one
meta/provenance section of marginal runtime value, and two lessons whose
generalization confidence should stay provisional — none of which affects
correctness or safety. No required fixes; no further building is needed.

NO CHANGES REQUIRED — STOP BUILDING.
