# Module: configuration

Configuration, exposure, disclosure, and hardening classes.

> Distinguish directly observed configuration from application/self-reported
> configuration (`.clinerules/02-recon.md` U-B). Corroborate before relying on it.

ID:CONFIG-HEADERS
WHEN:[HTTP responses carry security posture]
SURFACE:[all responses]
OBSERVE:[CSP, X-Frame-Options, HSTS, X-Content-Type-Options, Referrer-Policy, cookie flags, Server banner]
HYPOTHESIS:[missing/weak security headers/settings]
TEST:[observe headers across surfaces (dynamic + static); note framing affect on other classes]
ADAPT:[n/a — observation]
CONFIRM:[record; assess as context/impact modifier, not standalone vuln without effect]
IMPACT:[context|volume]
RELATED:[CLIENT-*,AUTHN-SESSION,WEB-CSRF]

ID:CONFIG-INFO
WHEN:[internal details surfaced]
SURFACE:[debug pages, stack traces, error details, version endpoints, verbose errors, self-reported config]
HYPOTHESIS:[information disclosure aiding further attacks]
TEST:[observe error/version/debug output; compare verbose vs normal for same request with control]
ADAPT:[verbosity trigger, URL paths, headers]
CONFIRM:[specific internal info (paths, versions, schema, config) disclosed that should not be]
IMPACT:[info|attack_lubricant]
STOP:[no exploit of disclosed detail in recon; record only]
RELATED:[AUTHN-ENUM,API-EXPOSE,CONFIG-DEBUG]

ID:CONFIG-DEBUG
WHEN:[debug/administration surfaces]
SURFACE:[debug endpoints, console, actuator/env paths, dev functions]
HYPOTHESIS:[debug/administration exposed to unauthorized/low-privilege]
TEST:[note presence; do not activate destructive/admin controls (U-D). A read-only presence check with control]
CONFIRM:[surfaces reachable that should be internal]
IMPACT:[info|privilege_potential|availability]
STOP:[do not activate destructive/debug-mutating controls during recon]
RELATED:[CONFIG-INFO,AUTHZ-FUNCTION,U-D]

ID:CONFIG-SECRETS
WHEN:[credentials/tokens/keys exposed]
SURFACE:[responses, JS, storage, config, logs, version control, error output]
HYPOTHESIS:[secrets exposure]
TEST:[observe storage/response for secret material; do not exfiltrate or use them]
ADAPT:[n/a]
CONFIRM:[usable secret artifact observable to low-privilege caller]
IMPACT:[account|infra]
STOP:[never test or use discovered secrets; record and report only]
RELATED:[CONFIG-INFO,API-EXPOSE,MODERN-STORAGE]

ID:CONFIG-EXPOSED
WHEN:[resources reachable that should not be]
SURFACE:[backup files, git metadata, .git, staging, source map, internal paths]
HYPOTHESIS:[exposed resource disclosure]
TEST:[observe presence; minimal read-only probe with control]
CONFIRM:[sensitive resource reachable]
IMPACT:[info|code|data]
RELATED:[CONFIG-INFO,WEB-PATHTRAV]

ID:CONFIG-FEATURES
WHEN:[unnecessary features/services present]
SURFACE:[extra endpoints, default pages, sample data, admin panels]
HYPOTHESIS:[unnecessary feature/service expands attack surface]
TEST:[observe and record; assess in-scope effect]
ADAPT:[n/a]
CONFIRM:[elevated/unnecessary surface reachable in scope]
IMPACT:[info|surface_expansion]
RELATED:[CONFIG-EXPOSED,PROTOCOL]