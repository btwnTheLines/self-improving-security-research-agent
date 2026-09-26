# Module: injection

Interpreter/parser injection classes. Compact entries.

ID:INJ-SQLI
WHEN:[input fed to a persistence/query layer]
SURFACE:[sql-ish params, order/filter/id fields, ORM/query endpoints]
OBSERVE:[query string or body param; note type: str|int|uuid|json; framing via q/ and quotes/operators in errors]
HYPOTHESIS:[input concatenated into an SQL statement without parameterization]
TEST:[baseline request → same request with a neutral character (e.g. one quote) → compare response/error/timing/handling]
ADAPT:[by param type: integer/string/encoded/json; by DB: comments, concat, error-vs-blind; only escalate when baseline differs]
CONFIRM:[evidence of unparameterized interpolation (e.g. error referencing a clause, differing handling) with a non-destructive probe + control]
IMPACT:[data_read|data_write|auth_bypass|availability]
STOP:[use read-only minimal probes; no dump/pivot; no blind time-delay loops without approval]
TOOLS:[http(api|cli),burp,browser]
RELATED:[AUTHZ-FUNCTION,API-*,CONFIG-INFO]

ID:INJ-CMD
WHEN:[input reaches an OS command/exec surface]
SURFACE:[functions that run commands (ping/curl/path params), filenames passed to shell-able utilities]
HYPOTHESIS:[input concatenated into a shell command]
TEST:[neutral metacharactic probe (e.g. forced EOF/split) → compare behavior vs control]
ADAPT:[quoting, metachar set (;|&&||`$()), encoding, spaces/whitespace handling, shell vs exec]
CONFIRM:[observed command-parsing difference attributable to input, with control]
IMPACT:[remote_exec|data|availability]
STOP:[no actual command output harvest; minimal evidence only]
RELATED:[INJ-SQLI,API,CONFIG-INFO]

ID:INJ-TPL
WHEN:[input echoed/evaluated in a template context]
SURFACE:[email/template fields, markdown/wysiwyg, message bodies, any rendered text]
HYPOTHESIS:[server-side template/expression evaluated on user input]
TEST:[neutral template token probe vs control → differing evaluation output]
ADAPT:[by template engine detected from error/markup; braces/delimiters vary]
CONFIRM:[input-specific evaluation result, with control, non-destructive]
IMPACT:[data_read|rce_potential|info]
STOP:[no actual expression execution beyond minimal proof; client-side template is different class]
RELATED:[CLIENT-XSS,API]

ID:INJ-LDAP
WHEN:[input reaches an LDAP filter/query]
SURFACE:[directory lookup params, login/attribute filters]
HYPOTHESIS:[filter built by string concat]
TEST:[neutral filter metachar probe vs control]
CONFIRM:[filter-parse difference attributable to input]
IMPACT:[auth_bypass|data_read]
RELATED:[AUTHN-*,AUTHZ-*]

ID:INJ-XML
WHEN:[XML/parser input accepted]
SURFACE:[SOAP/XML endpoints, uploads parsed as XML, SSO/assertion handling]
HYPOTHESIS:[external entity/XXE or parser mis-config on attacker XML]
TEST:[external-entity probe referencing a controlled/non-network marker; attribute/DTD variant]
ADAPT:[entity expansion, external DTD, parameter entities, content-type]
CONFIRM:[parser resolves entity (effect) with control; prefer marker over outbound fetch]
IMPACT:[file_read|ssrf|availability]
STOP:[no external callout to third parties; local only; avoid billion-laughs (availability)]
RELATED:[INJ-SQLI,WEB-SSRF,FILES]

ID:INJ-OTHER
WHEN:[other interpreter/parser input: headers (email/Host), OS path joins, regex, eval-like]
SURFACE:[any input later interpreted]
HYPOTHESIS:[unsafe interpolation into another grammar]
TEST:[neutral grammar-discriminating probe vs control]
ADAPT:[grammar-specific; encoding; parser behavior]
CONFIRM:[differentiated interpretation attributable to input]
IMPACT:[varies]
RELATED:[WEB-*,API-*]