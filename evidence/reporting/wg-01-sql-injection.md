# WG-01 — SQL Injection: Unauthenticated Data Read (Confidentiality)

## 1. Title
SQL Injection — string concatenation into a query allows retrieval of internal records

## 2. Summary
A login-less query assignment endpoint concatenates user-supplied string input into
an SQL statement without parameterization. A boolean-always-true injection returned
the entire contents of the application's internal user table, including salary and
authentication-token columns that the caller should not have been able to view.

## 3. Confirmation status
**Confirmed vulnerability**

## 4. Affected component
`POST /WebGoat/SqlInjection/attack8` (assignment `SqlInjectionLesson8`), a database
query interface reached in an authenticated session. The normal (non-malicious)
query returns only records matching the submitted `name` + `auth_tan` filter; the
server-side statement is built by string concatenation of those two values.

## 5. Preconditions
- An authenticated session against the local target (`127.0.0.1:8080/WebGoat/`).
- No special role required; the caller is an ordinary user.

## 6. Steps to reproduce
1. Establish an authenticated session.
2. Send:
   `POST /WebGoat/SqlInjection/attack8`
   Body (form): `name=' OR '1'='1&auth_tan=' OR '1'='1`
3. Observe the response.

## 7. Expected behavior
If the control were correct, the query filter would be parameterized or otherwise
escaped, and the supplied values would match no record (or only the caller's
record), returning no internal data. The raw quotes would be treated as data, not
as SQL syntax.

## 8. Actual behavior
The response returned `lessonCompleted: true` with feedback:

> "You have succeeded! You successfully compromised the confidentiality of data by
> viewing internal information that you should not have access to."

and the `output` field contained the **entire** user table (all rows and columns,
including USERID, FIRST_NAME, LAST_NAME, DEPARTMENT, SALARY, AUTH_TAN) instead of
only matching records. The injected `' OR '1'='1` was interpreted as SQL.

## 9. Security impact
Confidentiality compromise: an unprivileged caller retrieved internal records
(employee names, departments, salaries, and authentication-token values) across the
whole table, not just their own. This is the data-read form of SQL injection and is
evidence of unsafe dynamic query construction.

## 10. Evidence / PoC
Raw artifact: `evidence/reporting/raw/wg_sqli_attack8.txt`

Request:
```
POST /WebGoat/SqlInjection/attack8 HTTP/1.1
Host: 127.0.0.1:8080
Content-Type: application/x-www-form-urlencoded
name=' OR '1'='1&auth_tan=' OR '1'='1
```
Response (abridged):
```
{"assignment":"SqlInjectionLesson8","attemptWasMade":true,
 "feedback":"...compromised the confidentiality of data by viewing internal
 information...","lessonCompleted":true,
 "output":"<table>...32147 Paulina Travers Accounting 46000 P45JSI...
  34477 Abraham Holman Development 50000 UU2ALK...
  37648 John Smith Marketing 64350 3SL99A...
  89762 Tobi Barnett Development 77000 TA9LL1...
  96134 Bob Franco Marketing 83700 LO9S2V...</table>"}
```
Control: the same endpoint with a literal value pair returned no such dump; the
injection differs only by the injected `' OR '1'='1` operands.

## 11. Remediation
Use parameterized queries / prepared statements (values bound, never concatenated)
for this and any other query built from user input. Apply least-privilege DB
accounts so the query layer cannot expose columns it should not.

## 12. Severity rationale
High-prevalence data-read SQL injection. Reliability is immediate and without
special preconditions; impact is direct confidentiality breach of internal records.
Severity is limited only by the fact that this is a controlled teaching-range client
session, not a production dataset.

## 13. Limitations / remaining uncertainty
- The full table was returned, establishing confidentiality impact directly.
- A related variant (`attack9`, salary-modification intent) also reflected the
  injection but was not further exercised; it is not claimed as a separate finding.
- No host, user, or external data was touched; all returned records are the
  application's own synthetic data.
