# Module: authorization

Access-control, object-level, function-level, and tenant-isolation classes.

> When object identifiers are exposed, consider whether authorization is
> enforced consistently for each object (general principle).

ID:AUTHZ-BOLA  (object-level / IDOR)
WHEN:[object identifiers exposed in URLs/paths/bodies]
SURFACE:[/resource/:id, ?id=, JSON refs, nested resources]
OBSERVE:[identifier form (int|uuid|slug|email), owner binding, current identity]
HYPOTHESIS:[object access not authorized for caller]
TEST:[baseline own object → controlled cross-object reference (your own second resource) within same account]
ADAPT:[id type, location (path/query/body), method, required session]
CONFIRM:[access/action on object you may not act on, with control]
IMPACT:[data_read|data_write|privilege]
STOP:[no real other-user objects without approval; use own/second-account control objects]
RELATED:[AUTHZ-HORIZ,AUTHZ-TENANT,API,GRAPHQL]

ID:AUTHZ-HORIZ
WHEN:[same-role users may act on one another's data]
SURFACE:[user-owned resources, user-id in requests]
HYPOTHESIS:[missing object ownership check (horizontal)]
TEST:[own object vs a second identifier you control, same role]
CONFIRM:[cross-user effect with control]
IMPACT:[data|action]
RELATED:[AUTHZ-BOLA,AUTHN-SESSION]

ID:AUTHZ-VERT
WHEN:[privileged functionality exists alongside lower-privilege]
SURFACE:[admin/management endpoints, role-bearing requests]
OBSERVE:[whether elevated actions require role; how role travels]
HYPOTHESIS:[vertical escalation via missing function-level or trustable role data]
TEST:[call privileged function with minimal-role session, minimal non-destructive probe with control]
ADAPT:[role field, header, token claim, direct endpoint]
CONFIRM:[elevated capability without privilege, controlled]
IMPACT:[privilege|data]
STOP:[no real privilege elevation against privileged accounts; approval required]
RELATED:[AUTHZ-FUNCTION,AUTHN-SESSION,API]

ID:AUTHZ-FUNCTION
WHEN:[some features are role/function-gated]
SURFACE:[menus hidden by role, gated routes, admin APIs]
HYPOTHESIS:[function-level auth missing (client-side gating only)]
TEST:[request gated function while unprivileged, control = authorized user]
CONFIRM:[response differs due to missing server gate]
IMPACT:[privilege]
RELATED:[AUTHZ-VERT,API,WEB]

ID:AUTHZ-OWNERSHIP
WHEN:[resources have implicit ownership]
SURFACE:[objects created/owned by caller]
HYPOTHESIS:[ownership not enforced on read/update/delete]
TEST:[own object lifecycle with a controlled second object]
CONFIRM:[write/delete on object not owned, with control]
IMPACT:[data|integrity]
RELATED:[AUTHZ-BOLA,AUTHZ-HORIZ]

ID:AUTHZ-TENANT
WHEN:[multi-tenant/multi-org isolation]
SURFACE:[org/tenant scoping params, shared resources]
HYPOTHESIS:[tenant isolation not enforced]
TEST:[cross-tenant reference (second tenant you control) vs own]
CONFIRM:[cross-tenant access/effect]
IMPACT:[data|privilege]
RELATED:[AUTHZ-BOLA,API,CLOUD-IAM]