# Module: modern-apps

Modern app classes: SPA/client-side, browser storage, JavaScript security,
WebSockets, event-driven interfaces.

ID:MODERN-CLIENT
WHEN:[client-side app (SPA)]
SURFACE:[client bundle, client routes, JS-rendered pages]
OBSERVE:[is it server-rendered or client-side? (sample one small asset; U-C); bundle size]
HYPOTHESIS:[client-side handling widens surface (routes/endpoints/sinks discoverable in JS)]
TEST:[observe client structure from small assets/page sources (no unnecessary large downloads)]
ADAPT:[n/a — recon of client is observation]
CONFIRM:[client-revealed environments/endpoints/claims recorded as observable surface]
IMPACT:[surface]
RELATED:[MODERN-STORAGE,CLIENT-DOM,API-*]

ID:MODERN-STORAGE
WHEN:[browser storage used]
SURFACE:[localStorage/sessionStorage/cookies, bearer tokens, cached data]
HYPOTHESIS:[sensitive data in browser storage / XSS-exfiltratable / cookie/token handling weak]
TEST:[observe what is stored and how (scope: own session); correlate with XSS/token handling]
ADAPT:[n/a]
CONFIRM:[sensitive artifact stored/transactionable insecurely (own session)]
IMPACT:[session|data]
RELATED:[AUTHN-SESSION,MODERN-JS,CONFIG-SECRETS]

ID:MODERN-JS
WHEN:[JS governs security-sensitive logic]
SURFACE:[client-side enforcement, JS secrets, source maps, dynamic sinks]
HYPOTHESIS:[client-side-only gating or JS-disclosed secrets/claims]
TEST:[observe whether enforcement duplicates server-side; note JS claims]
ADAPT:[n/a]
CONFIRM:[client-gating only / JS-exposed secret/claim]
IMPACT:[privilege|info]
RELATED:[AUTHZ-FUNCTION,MODERN-CLIENT,CONFIG-SECRETS]

ID:MODERN-WS
WHEN:[WebSocket channel present]
SURFACE:[ws/wss endpoints, upgrade handshake, messages]
HYPOTHESIS:[authz/session/message-validation gap over WebSocket]
TEST:[validated own-session messages; observe handshake auth; benign cross-context variation with control]
ADAPT:[message framing, origin/handshake checks, session reuse]
CONFIRM:[gap attributable to WS handling]
IMPACT:[info|authz|availability]
STOP:[no message flood]
RELATED:[AUTHN-SESSION,AUTHZ-*,PROTO-APPS]

ID:MODERN-EVENT
WHEN:[event-driven interfaces (SSE, webhooks, queues, streaming)]
SURFACE:[server-sent events, callback URLs, message subscribers]
HYPOTHESIS:[event trust boundary (authz on subscribe; callback injection/SSRF)]
TEST:[own-subscription control; callback target = benign in-scope marker]
ADAPT:[source filtering, authorization on channel]
CONFIRM:[unauthorized subscribe/callback effect, with control]
IMPACT:[data|info|avail]
RELATED:[WEB-SSRF,AUTHZ-*,PROTO-APPS]