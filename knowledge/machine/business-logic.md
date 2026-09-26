# Module: business-logic

Workflow, state, value, trust-boundary, concurrency, and abuse-of-function
classes. Applicability is highly application-specific: derive from observed
flow, never from a checklist.

ID:BUS-WORKFLOW
WHEN:[multi-step flows exist]
SURFACE:[onboarding, checkout, order, verification, authorization, invitations]
HYPOTHESIS:[step order/reuse manipulable (skip, reorder, mix steps)]
TEST:[legit complete own flow; then vary order/skip for own object with control]
ADAPT:[step token, state field, revisit]
CONFIRM:[out-of-order state accepted for own object]
IMPACT:[data|privilege|integrity]
RELATED:[AUTHN-STATE,BUS-STATE,API-MASS]

ID:BUS-STATE
WHEN:[objects have expected state transitions]
SURFACE:[orders, accounts, statuses, approvals]
HYPOTHESIS:[invalid/unauthorized state transition allowed]
TEST:[own object valid → invalid/forbidden transition, with control]
CONFIRM:[forbidden transition accepted]
IMPACT:[integrity|data|availability]
RELATED:[BUS-WORKFLOW,AUTHZ-OWNERSHIP]

ID:BUS-VALUE
WHEN:[numeric/value decisions client-driven]
SURFACE:[quantity, price, discount, amount, reward, points, limits]
HYPOTHESIS:[client-supplied value trusted (negative/zero/oversized/edited field)]
TEST:[benign boundary value on own transaction vs control]
ADAPT:[field, sign, precision, overflow, multi-value]
CONFIRM:[trusted or unbounded value yields unintended effect on own object]
IMPACT:[financial|data|integrity]
RELATED:[BUS-WORKFLOW,API-PARAM]

ID:BUS-TRUST
WHEN:[one component is trusted implicitly]
SURFACE:[server trusts client-computed totals, flags, discounts, prices]
HYPOTHESIS:[trust boundary violated]
TEST:[toggle a client-side trust marker (e.g. price/total/role flag) for own object with control]
ADAPT:[field, location, encoding]
CONFIRM:[server honors an input it should recompute]
IMPACT:[financial|privilege|integrity]
RELATED:[BUS-VALUE,API-MASS]

ID:BUS-RACE
WHEN:[concurrency-sensitive operations]
SURFACE:[balance/stock/coupon/promo redemption, enrollment]
HYPOTHESIS:[TOCTOU / race (double-spend, oversubscribe)]
TEST:[controlled concurrent benign attempts on own resource (low volume) with control]
ADAPT:[request timing, idempotency keys]
CONFIRM:[effect applied more than once / inconsistent state]
IMPACT:[financial|data|availability]
STOP:[low volume; own resource; no resource exhaustion]
RELATED:[BUS-VALUE,BUS-IDEMPOT,PROTOCOL]

ID:BUS-IDEMPOT
WHEN:[repeatable actions]
SURFACE:[payments, notifications, deductions, queue jobs]
HYPOTHESIS:[replay/idempotency issue (repeat a one-time action)]
TEST:[replay an own benign action with control]
ADAPT:[idempotency key, retry semantics]
CONFIRM:[side-effect duplicated]
IMPACT:[financial|spam|integrity]
RELATED:[BUS-RACE,BUS-WORKFLOW]

ID:BUS-ABUSE
WHEN:[intended function usable for unintended purpose/volume]
SURFACE:[free tiers, discounts, referral, export, notifications, search]
HYPOTHESIS:[abuse of intended functionality to gain undue benefit/exposure]
TEST:[benign excessive/alternate use of own account with control]
CONFIRM:[unauthorized benefit/exposure without breaking scope]
IMPACT:[financial|data|availability]
STOP:[no resource exhaustion; small scale]
RELATED:[BUS-VALUE,API-PARAM,CONFIG-INFO]