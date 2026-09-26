# Module: protocol

Network/service, TLS, HTTP-behavior, and protocol trust-boundary classes.

> Authorized service enumeration only, and only when the network/service surface
> is explicitly in scope. Tool availability does not imply authorization.

ID:PROTO-ENUM
WHEN:[network/service discovery is explicitly in scope]
SURFACE:[in-scope host/ports/services]
HYPOTHESIS:[unexpected/in-scope service or exposure]
TEST:[passive/lightly-active enumeration limited to in-scope target; record only]
ADAPT:[port/version detection depth — keep minimal]
CONFIRM:[service identified on in-scope target]
IMPACT:[info|surface]
STOP:[no broad scans; no out-of-scope hosts; no banners beyond target]
TOOLS:[nmap(scope-limited)]
RELATED:[CONFIG-EXPOSED,SCOPE]

ID:PROTO-TLS
WHEN:[TLS/transport posture matters]
SURFACE:[https endpoints, headers, cipher suites]
HYPOTHESIS:[weak TLS/security configuration]
TEST:[observe TLS negotiation/settings for the target; record]
CONFIRM:[weak config confirmed from observation]
IMPACT:[integrity_exposure|info]
TOOLS:[openssl,nmap(script-limited)]
RELATED:[CONFIG-HEADERS]

ID:PROTO-HTTP
WHEN:[HTTP behavior across stack]
SURFACE:[redirect handling, status codes, host/routing, caching]
HYPOTHESIS:[HTTP-layer trust/behavior gap]
TEST:[observe and vary benign signals with control]
ADAPT:[host, method, headers, scheme]
CONFIRM:[behavioral gap attributable to HTTP handling]
IMPACT:[routing|info|availability]
RELATED:[WEB-REQMANIP,WEB-TRUST]

ID:PROTO-APPS
WHEN:[application-level protocols (WebSocket, gRPC, etc.) present]
SURFACE:[upgrade headers, websocket, protocol-specific framing]
HYPOTHESIS:[protocol trust-boundary issue]
TEST:[observe protocol handshake/state with control; benign variation on own session]
ADAPT:[protocol framing, auth in-band/out-band]
CONFIRM:[gap attributable to protocol handling]
IMPACT:[info|authz|availability]
RELATED:[MODERN-WS,API]

ID:PROTO-MGMT
WHEN:[management/admin services present]
SURFACE:[admin interfaces, management ports, debug consoles]
HYPOTHESIS:[unauthenticated/exposed management (off-limits to activate)]
TEST:[presence check only (U-D); record as off-limits]
CONFIRM:[surface exists]
IMPACT:[info|privilege_potential|availability]
STOP:[do not activate management/destructive controls]
RELATED:[CONFIG-DEBUG,CONFIG-EXPOSED,U-D]