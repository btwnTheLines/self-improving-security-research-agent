# Module: web

Request/web classes: CSRF, SSRF, redirects, path handling, request manipulation,
HTTP trust-boundary issues.

ID:WEB-CSRF
WHEN:[state-changing request via browser cookies]
SURFACE:[POST/state-changing endpoints authenticated by cookie]
OBSERVE:[anti-CSRF tokens present? origin/referer checks? SameSite?]
HYPOTHESIS:[state change possible without a user-unaware valid proof]
TEST:[submit state-changing request without the token/origin marker, with control (valid request)]
ADAPT:[token presence/derivation, origin/referer, JSON/plain, SameSite context]
CONFIRM:[effect applied without anti-CSRF control, with control]
IMPACT:[data_write|integrity|availability_of_account]
STOP:[no destructive/large effect; minimal state delta; no real user]
RELATED:[AUTHN-SESSION,WEB-REQMANIP,CONFIG-HEADERS]

ID:WEB-SSRF
WHEN:[server fetches a client-controlled URL]
SURFACE:[url/file fields, webhooks, import/external resolvers, image fetch]
HYPOTHESIS:[server-side request to attacker-selected target]
TEST:[control target = a benign, in-scope marker (localhost/own) vs a neutral control]
ADAPT:[scheme, host, redirect handling, DNS, URL parse quirks, encoding]
CONFIRM:[server reaches in-scope marker (response/time/effect), with control]
IMPACT:[internal_access|data|pivot]
STOP:[no external/internal network pivot beyond minimal marker; no metadata abuse without approval]
RELATED:[API,FILES,CLOUD-META,PROTOCOL]

ID:WEB-REDIRECT
WHEN:[URL/local input drives a redirect]
SURFACE:[?next=/url params, login-success redirect, open links]
HYPOTHESIS:[open redirect (attacker-controlled destination)]
TEST:[benign controlled destination as param vs control]
ADAPT:[relative/absolute/scheme-relative, protocol-relative, encoded]
CONFIRM:[redirect to attacker-chosen in-scope destination, with control]
IMPACT:[phishing|oAuth_token_leak_context]
STOP:[no external redirects out of scope]
RELATED:[CLIENT-CONTEXT,WEB-REQMANIP]

ID:WEB-PATHTRAV
WHEN:[input used to build a file/resource path]
SURFACE:[file params, download/export paths, ?file=, template path selectors]
HYPOTHESIS:[path traversal / arbitrary file read]
TEST:[neutral traversal step on a controlled path vs control; observe normalization]
ADAPT:[../ variants, encoding, OS separators, absolute paths]
CONFIRM:[retrieval of a file that should not be path-selectable, with control]
IMPACT:[data_read|rce_potential]
STOP:[read only; minimal files; no system files beyond proof]
RELATED:[FILES-PATH,INJ-OTHER,API]

ID:WEB-REQMANIP
WHEN:[server trusts method/headers/bodies inconsistently]
SURFACE:[HTTP method handling, Host/Origin/X-Forwarded-*, duplicate headers, param parsing]
HYPOTHESIS:[security relevant to method/header/param trust boundary]
TEST:[method/header variation with control, minimal]
ADAPT:[method override, header duplicates, param bombs, parsing discrepancies]
CONFIRM:[enforcement gap attributable to manipulation]
IMPACT:[bypass_authz|routing|availability]
STOP:[no availability-impacting fuzz; small variations only]
RELATED:[AUTHN-SESSION,WEB-CSRF,API]

ID:WEB-TRUST
WHEN:[one HTTP component trusts another]
SURFACE:[proxy→backend, host-based routing, origin checks, caching]
HYPOTHESIS:[trust boundary violated (cache poisoning, host routing, origin spoof)]
TEST:[observe how trust signals affect response, with control]
ADAPT:[host/origin/cache-key manipulation]
CONFIRM:[misrouting/poison behavior attributable to input]
IMPACT:[data_exposure|defacement|availability]
STOP:[no caches of real users poisoned]
RELATED:[WEB-REQMANIP,CONFIG-*]