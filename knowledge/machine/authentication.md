# Module: authentication

Credential, session, token, recovery, MFA, and authentication-state classes.

> Confirm session/token structure from a genuine token before constructing
> auth tests (`.clinerules/03-testing.md` Authentication Context).

ID:AUTHN-LOGIC
WHEN:[login/verification compares credentials]
SURFACE:[login, API token check, OTP verify]
OBSERVE:[how identity and proof are transmitted; session issued how]
HYPOTHESIS:[verification logic flawed (e.g. any-match, type-confusion on identity/proof)]
TEST:[benign malformed/type-varying input vs control within one account]
ADAPT:[field type, multiplicity, encoding]
CONFIRM:[identity established without correct proof, controlled and reversible]
IMPACT:[authn_bypass]
STOP:[no real-account credential attacks; no guessing privileged creds]
RELATED:[AUTHN-SESSION,AUTHZ-*]

ID:AUTHN-CRED
WHEN:[credential storage/transport]
SURFACE:[login/submit/changepass/registration endpoints]
HYPOTHESIS:[credentials mishandled (plaintext store, no rate limit, exposed in logs/response)]
TEST:[observe transport (HTTPS), response content, error differences for existence]; [rate-limit/account-enum differ signals]
ADAPT:[case sensitivity, format, user enumeration signals]
CONFIRM:[evidence of weak transport/storage/response handling with control]
IMPACT:[cred|account_takeover]
STOP:[no brute force; single sign-in difference only]
RELATED:[PROTO-TLS,AUTHN-SESSION,AUTHN-ENUM]

ID:AUTHN-SESSION
WHEN:[state is carried via cookie/token]
SURFACE:[session cookie, bearer/JWT, claims]
OBSERVE:[cookie flags; token format(JWT? claims? exp?); server decode behavior]
HYPOTHESIS:[session predictable, not invalidated, or client-trustable]
TEST:[session fixation/rotation on login/logout; token manipulation vs baseline]
ADAPT:[algorithm/alg field, expiry, claim semantics — after genuine token observed]
CONFIRM:[state accepted that should not be (within one account), with control]
IMPACT:[impersonation|account_takeover]
STOP:[no cross-user; one-account only; no alg downgrade blind guess]
RELATED:[AUTHN-LOGIC,MODERN-STORAGE,API]

ID:AUTHN-RESET
WHEN:[password recovery/reset]
SURFACE:[forgot/reset links, tokens, security questions]
HYPOTHESIS:[reset flow predictable or bypassable (guessable token, user-controlled account field, no auth on step)]
TEST:[enumerate reset-flow steps via benign markers for own account]
ADAPT:[token construction, step order, account reference]
CONFIRM:[flow accepts a controlled non-proof for own account]
IMPACT:[account_takeover]
RELATED:[AUTHN-SESSION,AUTHZ-*]

ID:AUTHN-MFA
WHEN:[MFA/2FA present]
SURFACE:[2FA setup/verify/disable, TOTP]
HYPOTHESIS:[MFA bypassable (step skip, stale state, backup/recovery reuse, verify-any)]
TEST:[for own account, benign path/state variations with control]
ADAPT:[step ordering, state tokens, known codes vs guesses]
CONFIRM:[MFA gate passed without valid second factor, own account]
IMPACT:[authn_bypass]
STOP:[no real MFA replay against live codes if it risks someone else]
RELATED:[AUTHN-SESSION,MODERN-*]

ID:AUTHN-STATE
WHEN:[multi-step or stateful auth]
SURFACE:[state tokens, one-time flows, OAuth-ish transitions]
HYPOTHESIS:[state confusion (replay, reorder, token mix)]
TEST:[legit close to the state machine; reorder/stale for own session]
CONFIRM:[state consumed out of sequence, own flow]
IMPACT:[authn_bypass]
RELATED:[AUTHN-SESSION,BUS-*]

ID:AUTHN-ENUM
WHEN:[account existence observable]
SURFACE:[login/register/reset responses]
HYPOTHESIS:[user enumeration via differing responses/timing]
TEST:[two fabricated variants vs control]
CONFIRM:[consistent differential signal]
IMPACT:[info]
RELATED:[AUTHN-CRED,CONFIG-INFO]