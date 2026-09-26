# Module: cloud

Cloud/platform classes: IAM, object storage, metadata/service exposure,
management interfaces, platform trust boundaries.

ID:CLOUD-IAM
WHEN:[cloud identity/permission model]
SURFACE:[cloud roles, scopes, tokens, policies, service accounts]
HYPOTHESIS:[over-privileged/inconsistent authorization at platform layer]
TEST:[observe authorization for own identity/resources; controlled variation with control]
ADAPT:[scope, role, token audience]
CONFIRM:[unauthorized platform action available to lower-privilege caller]
IMPACT:[privilege|data]
RELATED:[AUTHZ-VERT,AUTHN-SESSION]

ID:CLOUD-STORAGE
WHEN:[object storage buckets/files]
SURFACE:[bucket/object URLs, storage permissions]
HYPOTHESIS:[misconfigured storage (public/writable)]
TEST:[observe access controls on in-scope objects; read-only access check with control]
ADAPT:[object reference, listing permission]
CONFIRM:[object readable/writable without authorization]
IMPACT:[data_leak|data_write]
STOP:[no writes without approval; read-only presence]
RELATED:[FILES-DOWNLOAD,CLOUD-IAM]

ID:CLOUD-META
WHEN:[metadata/service where platform leaks internal info]
SURFACE:[metadata endpoints, error unions, cloud identity services]
HYPOTHESIS:[metadata/service exposure reachable]
TEST:[observe whether a metadata/service surface is reachable in-scope; minimal read-only with control]
ADAPT:[n/a]
CONFIRM:[in-scope metadata/service exposure]
IMPACT:[info|credential_potential]
STOP:[no metadata abuse; no credential harvesting; record only]
RELATED:[WEB-SSRF,CONFIG-SECRETS]

ID:CLOUD-MGMT
WHEN:[management/interfaces control plane]
SURFACE:[admin consoles, APIs, control-plane endpoints]
HYPOTHESIS:[management interface exposed/unauthorized (off-limits to activate)]
TEST:[presence check only (U-D)]
CONFIRM:[surface exists]
IMPACT:[privilege_potential|availability]
STOP:[no activation; record as off-limits]
RELATED:[CONFIG-DEBUG,PROTO-MGMT,U-D]

ID:CLOUD-TRUST
WHEN:[platform trust boundaries]
SURFACE:[cross-service calls, OAuth/broker, service identities]
HYPOTHESIS:[trust boundary violated between platform components]
TEST:[observe authorization between in-scope components; controlled variation]
ADAPT:[audience, impersonation, delegation]
CONFIRM:[cross-boundary access attributable to input]
IMPACT:[privilege|data]
RELATED:[CLOUD-IAM,AUTHN-STATE]