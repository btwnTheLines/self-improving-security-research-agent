# Module: api

API classes: REST, GraphQL, excessive data exposure, mass assignment / property
binding, authorization on APIs, method handling, parameter manipulation,
schema/input validation.

ID:API-BOLA  (see AUTHZ-BOLA for details)
WHEN:[object refs in API requests]
RELATED:[AUTHZ-BOLA,AUTHZ-HORIZ,AUTHZ-TENANT]

ID:API-EXPOSE
WHEN:[API returns objects to clients]
SURFACE:[list/detail responses, schemas]
HYPOTHESIS:[excessive data exposure (internal fields / over-collection returned)]
TEST:[observe response fields vs what the feature requires; control = authorized call]
ADAPT:[field selection, relation expansion, serialization]
CONFIRM:[internal/excess fields observable to normal caller]
IMPACT:[data_leak|cred]
RELATED:[API-SCHEMA,CONFIG-INFO,GRAPHQL]

ID:API-MASS
WHEN:[create/update accepts object/properties]
SURFACE:[POST/PUT/PATCH object endpoints, registration]
HYPOTHESIS:[mass assignment / property binding (client-supplied fields bound to server objects)]
TEST:[for own object, benign extra field echo vs control; observe persisted property]
ADAPT:[field name, nesting, json vs form, graphql args]
CONFIRM:[a property you should not set via API is persisted, with control]
IMPACT:[privilege|data]
STOP:[own object only; do not change a real privileged field without approval]
RELATED:[API-BOLA,AUTHZ-VERT,GRAPHQL]

ID:API-METHOD
WHEN:[HTTP method semantics]
SURFACE:[same resource under different methods]
HYPOTHESIS:[method mishandling (unauth GET/PUT, override bypass)]
TEST:[method/override variation on an authorized resource, with control]
ADAPT:[HEAD/OPTIONS, X-HTTP-Method-Override, CORS preflight]
CONFIRM:[behavioral difference attributable to method handling]
IMPACT:[bypass|info]
RELATED:[WEB-REQMANIP,WEB-CSRF]

ID:API-PARAM
WHEN:[parameters drive behavior]
SURFACE:[ids, sort/order, pagination, filters, mass params]
HYPOTHESIS:[parameter manipulation (types, ranges, negatives, arrays, duplicates) weakens checks]
TEST:[benign boundary/type variation on own resource vs control]
ADAPT:[type, sign, size, array, encoding]
CONFIRM:[enforcement gap attributable to param handling]
IMPACT:[data|availability|authz]
STOP:[no resource-exhausting values]
RELATED:[API-BOLA,BUS-*]

ID:API-SCHEMA
WHEN:[input validation on API fields]
HYPOTHESIS:[weak schema/input validation (type, length, charset)]
TEST:[benign out-of-contract value vs control]
CONFIRM:[improper value accepted/processed]
IMPACT:[data|availability|injection_carrier]
RELATED:[API-PARAM,INJ-*]

ID:GRAPHQL  (when GraphQL observed)
SURFACE:[single /graphql endpoint, introspection, batching]
HYPOTHESIS:[introspection enabled; field/object authz gaps; alias/alias bypass; resource abuse]
TEST:[confirm observed schema first (introspection) → benign field access with control]
ADAPT:[introspection query, field selection, aliases, batch, variables]
CONFIRM:[unauthorized field/object / info or alias/allowlist effect]
IMPACT:[data_leak|availability]
STOP:[no introspection-heavy fuzz; no batch DoS]
RELATED:[API-*,AUTHZ-BOLA,MODERN-*]