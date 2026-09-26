# Module: client

Client-side / output-encoding classes.

ID:CLIENT-RXSS
WHEN:[input reflected into an HTML/JS response]
SURFACE:[query/body params echoed in body or headers; error/redirect echoes]
OBSERVE:[location of reflection: element content|attribute|script|url; encoding applied]
HYPOTHESIS:[reflection not context-safely encoded → markup/script injection]
TEST:[neutral probe char vs control reflected identically? → context-specific breakout probe]
ADAPT:[by context: element/attr/js/url; quote/angle/bracket set; URL-encoding; browser vs server]
CONFIRM:[warning-only marker that breaks out of context and would render, with control; no stored or privilege effect]
IMPACT:[session|data|token]
STOP:[browser-only; prefer benign marker; no cookie theft; capture real-use]
TOOLS:[browser,burp,http]
RELATED:[CLIENT-SXSS,CLIENT-DOM,CONFIG-HEADERS]

ID:CLIENT-SXSS
WHEN:[attacker-controlled text stored and later rendered to others]
SURFACE:[comments/feedback/name/display fields persisted]
OBSERVE:[is output HTML-encoded? which pages render it]
HYPOTHESIS:[stored content rendered without context-safe encoding]
TEST:[store a benign differential marker; observe rendering to a second session/context]
ADAPT:[element/attr/js context]
CONFIRM:[marker renders differently with/without encoding; control; affect on other user is the impact baseline]
IMPACT:[other_user_session|data]
STOP:[do not use real third parties; no persistent malicious content; mark tested artifact clearly if created]
RELATED:[CLIENT-RXSS,AUTHZ-*,BUS-*]

ID:CLIENT-DOM
WHEN:[client-side JS handles input via sinks]
SURFACE:[SPA; hash/query params; localStorage; URL-fragment-driven behavior]
HYPOTHESIS:[unsafe DOM sink (eval/innerHTML/write/doc.write/location) with attacker-controlled source]
TEST:[sink-reachable benign marker via the client route; compare controlled variation]
ADAPT:[source (hash, query, storage), sink, gating]
CONFIRM:[observed sink behavior attributable to source, with control]
IMPACT:[session|data]
RELATED:[CLIENT-RXSS,MODERN-*]

ID:CLIENT-CONTEXT
WHEN:[input lands in attribute, script, or URL context]
SURFACE:[any reflected/stored value in markup]
OBSERVE:[quoting and encoding around the value]
HYPOTHESIS:[context-unsafe output]
TEST:[context-discriminating marker vs control]
ADAPT:[attr(quote/event-handler), script(string/block), url(javascript:/data:)]
CONFIRM:[rendering difference attributable to input]
IMPACT:[session|data]
RELATED:[CLIENT-RXSS,CLIENT-DOM,WEB-OPENREDIRECT]