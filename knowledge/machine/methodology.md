# Module: methodology (cross-cutting)

Distilled, genuinely generalizable research methodology extracted from the case
studies (`knowledge/case-studies/01..05-*-analysis.md`). This entry is
**cross-cutting**: consult it alongside whatever class module the router
activates, not instead of it. It consolidates methodology that recurred across
five independent vulnerability classes, so each principle below is corroborated
by multiple engagements.

> Decision support only. It never authorizes an action. Applicability is derived
> from observed evidence, within the authorized scope, and within `.clinerules/`.
> These principles are class-level and technology-agnostic; the concrete
> payloads, hosts, endpoints, CVEs, and property names from the case studies are
> **not** general knowledge (see "Case-specific details" below).

---

## Reusable research principles

These recur across CS1–CS5. Each is a reasoning/behavior principle, not an
endpoint-specific technique.

- **Trust-boundary reasoning, not payload lists.** Locate chained components
  (proxy→backend, CDN→origin, cache→app) and ask what each *believes* about
  framing, origin, identity, and state, then test where they disagree. Do not
  clone payloads; derive hypotheses from the observed multi-tier architecture.
  (CS1 framing parity; CS2 "keyed ≠ safe" cache transforms; CS5 proxy-vs-backend
  framing.)
- **Every ambiguity probe is a differential with a paired control.** Design a
  benign/in-sync control input (present/absent, in-key/out-key, matched/non-matching)
  so a negative result is informative ("not vulnerable" vs "not triggered").
  Choose an observable response difference (status split, HIT/MISS, timing,
  reflected-vs-absent) as ground truth. (all five.)
- **Confirm behavior before assigning an impact class.** Buggy input is not a
  vulnerability; characterize what the server actually *does* with a value
  (fetches / renders / parses / reflects / honors) before claiming SSRF, XSS,
  injection, or RCE. (CS3 fetch-vs-render-vs-parse; CS4 confirm a property is
  read; CS5 primitive ≠ impact.)
- **Self-reported config, docs, and "patched" advisories are unverified.**
  Corroborate from observed responses before relying on them; a documentation
  change is not a fix and must be re-tested. (CS2 vendor docs wrong, docs-only
  fix; CS3 spec capability is a hypothesis to verify; aligns with `02-recon`.)
- **Separate primitive detection (safe) from impact confirmation (higher risk)
  and stage by collateral.** Detect cheaply and reversibly first; only escalate
  to the riskier demonstration after the safe stage passes. Never let a probe
  affect others' sessions/state or exceed minimum necessity. (CS1 Detect→Confirm→Explore;
  CS2 non-destructive to real visitors; CS4 destructive vs non-destructive.)
- **Chain an otherwise-benign gadget to demonstrate credible impact.** A raw
  primitive (single desync, one request DoS, a stray fetch) is not impact;
  compose it with an echo/redirect/cache/state bug that upgrades it to a
  concrete, observable consequence. (CS1, CS2, CS5; CS3 smallest forcing action.)
- **Treat a confirmed primitive without an impact path as an open problem, not
  a dead end.** Enumerate the remaining capabilities you control (bytes, shape,
  delivery) and find a universal mechanism that converts the primitive into
  impact. (CS5 universal reflector + cache-as-delivery.)
- **Pivot on constraint discovery, not on frustration.** Each blocked avenue
  names the concrete mechanism that unlocks the next capability; escalate along
  the ladder released by each discovery. (CS5 constraint ladder; CS4
  safety/reversibility drives pivots; CS3 mechanism-driven pivots.)
- **Enumerate, don't guess.** Form hypotheses over the full plausible space the
  target presents (framing combinations, normalization transforms, spec-mandated
  endpoints, globally-read option properties, shaping primitives) rather than
  transplanting expected payloads. (CS1, CS2, CS3, CS4.)
- **Audit your tooling.** Use tools that do not silently normalize/mangle the
  input being tested, and beware oracle false positives (e.g. a 404 conflation,
  a WAF scraping an OAST host). (CS1 auto-corrected Content-Length; CS3 Intruder
  404 conflation; CS4 WAF false-positive.)
- **Reach cross-user impact through shared server state when connections are
  isolated.** When per-request connections prevent direct delivery to others,
  a shared cache/state is a natural delivery channel — but treat any action that
  could persist attacker-controlled content for other users as high-collateral
  and human-approved. (CS2, CS5.)

## Reusable technical knowledge (class-level patterns)

Technology-agnostic test-construction patterns observed repeatedly:

- **Resolver/forcing oracle:** for a parameter that is fetched/read only at a
  later step (stored/second-order), choose the *smallest* flow action that forces
  its resolution (complete an authorization, hit a token/read-back endpoint),
  and confirm server-side handling with an out-of-band callback.
- **Out-of-band (OAST) callback** as an asynchronous success signal when no
  synchronous response difference is available; keep the callback host inside the
  authorized scope; obfuscate the host to survive hostname-scraping intermediaries.
- **Boolean oracle with an explicit negative control:** when a response splits
  into two distinguishable outcomes (200 vs 404, matched vs non-matched), a
  non-matching control input makes each response interpretable (enumeration,
  char-by-char extraction).
- **Message-framing differential (proxy vs backend)** as the desync oracle:
  confirm disagreement on message boundaries (Content-Length/Transfer-Encoding,
  response concatenation) with a benign in-sync pair as baseline.
- **Cache oracle:** pick a reflection + a HIT/MISS discloser; probe every change
  as a two-request differential decided by the HIT signal; examine the
  transformations applied to keyed components, not only keyless ones; pierce a
  masking cache with busters/alternate-path encodings before abandoning a
  static-looking surface.
- **Universal reflector:** when no application reflection endpoint exists, check
  for a protocol-native echo (TRACE) that reflects user-controlled bytes, which
  can materialize a payload needing no app-level reflector.
- **Execution precondition check:** a stored/crafted response is only impactful
  as XSS if served under an active content-type (e.g. text/html); verify the
  effective content-type before claiming execution impact.
- **Reversibility and containment:** prefer probes that can be toggled off and
  carry self-controlled/isolated identifiers and canaries so proofs cannot reach
  genuine users; never automate destructive deletion (PURGE) or state mutation.

## Case-specific details — NOT general knowledge

These provenances are recorded in the per-case analyses and must not be
transplanted or reasoned on as fact for another target:

- Hosts/domains and their role mappings; exact endpoint paths; parameter names
  and canaries used as controls.
- Vendor/version/date-specific behaviors and their CVE/tracker identifiers
  (behaviors changed under patching and can be wrong in vendor docs).
- Exact byte-formatted request/response samples and Content-Length/path values
  (worked illustrations on one target, not transferable payloads).
- Framework/module-specific property names and code snippets (surface on that
  stack, not guaranteed elsewhere).
- The claim that any vendor "always" behaves a certain way.

If the agent would carry these forward, it risks (a) presuming behavior that has
changed or was never true of the target under test, (b) transplanting
hosts/endpoints/payloads onto an unrelated authorized target (scope violation),
and (c) treating example exploits as a checklist instead of deriving hypotheses
from the observed target. The generalizable value is the *reasoning* in the two
sections above; the artifacts are illustrations only.

## Redundant lessons (consolidation signal)

The same principle appearing across multiple independent classes raises
confidence it generalizes:

- Differential-with-control: **all five** (CS1, CS2, CS3, CS4, CS5).
- Behavior-before-characterization / self-reported-not-evidence: **CS2, CS3,
  CS4, CS5**.
- Stage-by-collateral / separate detection from impact: **CS1, CS2, CS4, CS5**.
- Trust-boundary reasoning: **CS1, CS2, CS5**.
- Chain-a-benign-gadget-for-impact: **CS1, CS2, CS3, CS5**.
- Enumerate-don't-guess hypothesis formation: **CS1, CS2, CS3, CS4**.
- Pivot-on-constraint-discovery: **CS1, CS3, CS4, CS5**.
- Universal reflector / cache-as-cross-user-delivery: **CS2, CS5**.

## Safety and approval (shared, non-negotiable)

Every class studied here has a high-collateral variant that affects other users
or persistent server state (desync vs live traffic; cache poisoning; token
leakage via cross-domain flows; SSRF callbacks; process-crashing prototype
pollution; persisting attacker-controlled responses). The **methodology**
generalizes; the **side effects do not**. Before invoking any of these on a live
authorized target, confirm the stop/cleanup boundaries and keep the test minimal
and reversible; gate any test that could poison a cache, leak a credential, hit
an out-of-scope/internal host, crash or persistently modify state, or persist
attacker-controlled content for other users behind the human-approval step (per
`.clinerules/03-testing.md`).

## Sources

Distilled from `knowledge/case-studies/01-http-desync--analysis.md`,
`02-web-cache-entanglement--analysis.md`, `03-hidden-oauth--analysis.md`,
`04-server-side-prototype-pollution--analysis.md`,
`05-trace-desync--analysis.md`. Each analysis separates **[LESSON]** (this
entry), **[TARGET]** (excluded), and **[FACT/INTERP/UNCERTAIN]** for provenance.

RELATED := all class modules in `knowledge/machine/` (+ `index.md` router)

