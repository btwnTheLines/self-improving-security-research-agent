# Report 01 — SQL Injection in a user-ID lookup

## Summary
A numeric user-ID parameter is concatenated into an SQL statement without parameterization, allowing an attacker to alter the SQL query and read arbitrary database content.

## Confirmation status
**Confirmed vulnerability** (with read-only, non-destructive proof).

## Affected component
Authenticated "SQL Injection" exercise, user-ID lookup (`/vulnerabilities/sqli/`), GET parameter `id`.

## Preconditions
Authenticated session (any role). Security level: low (the level in effect).

## Steps to reproduce
1. `GET /vulnerabilities/sqli/?id=1&Submit=Submit` → baseline row.
2. `GET /vulnerabilities/sqli/?id=1'&Submit=Submit` → SQL syntax error names the injected quote.
3. `GET /vulnerabilities/sqli/?id=1' UNION SELECT user(),database()-- -&Submit=Submit` → returns DB user and database name.

## Expected behavior
The `id` value should be bound/parameterized so a quote or UNION cannot alter the query, and a non-integer should be rejected or safe.

## Actual behavior
- Baseline returned `ID: 1 / First name: admin / Surname: admin`.
- Single quote triggered: `You have an error in your SQL syntax ... near ''1''' at line 1` (unparameterized interpolation).
- UNION proof returned `First name: app@localhost / Surname: dvwa`, reading DB identity/metadata.

## Security impact
Data read of the database (read-only demonstrated; write/exfiltration not exercised). Impact supported: unauthorized read access to database contents.

## Evidence / PoC
Exact responses (raw: `evidence/reporting/raw/sqli_base.txt`, `sqli_quote.txt`, `sqli_union.txt`):
- `id=1'` → `<pre>...SQL syntax...near ''1''' at line 1</pre>`
- `id=1' UNION SELECT user(),database()-- -` → `<pre>...First name: app@localhost<br />Surname: dvwa</pre>`
Baseline control (`id=1`) returned only the normal row, so the differences are attributable to the injected input.

## Remediation
Use parameterized queries/bound parameters for all user input reaching a persistence layer; validate input types; apply least-privilege DB accounts.

## Severity rationale
Preconditions are moderate (authenticated), impact is data read with demonstrated arbitrary-SQL; reported Medium. Full write/exfiltration and error-based disclosure not exercised.

## Limitations / remaining uncertainty
Read/metadata proof only; no attempt to read user records or write. The blind (cookie/user-agent) injection surface is the same underlying class and was not separately exercised.