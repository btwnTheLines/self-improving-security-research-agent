# Report 02 — Command Injection in an IP-input field

## Summary
An IP-address field is concatenated into an OS command string, allowing attacker-controlled command execution on the server.

## Confirmation status
**Confirmed vulnerability** (minimal, benign, non-destructive proof).

## Affected component
Authenticated "Command Injection" exercise (`/vulnerabilities/exec/`), POST field `ip`.

## Preconditions
Authenticated session. Security level: low (in effect).

## Steps to reproduce
1. `POST ip=127.0.0.1` → baseline `ping` output.
2. `POST ip=127.0.0.1 && echo CMDINJ-CONFIRMED` → command separator appended; both run.

## Expected behavior
The value should be validated as an IP/host and passed to the command safely (or the command construct should not concatenate user input).

## Actual behavior
The injected `&&` followed by `echo` executed: the response contained the ping output **and** the line `CMDINJ-CONFIRMED`, proving the injected command ran in the server's shell.

## Security impact
Arbitrary OS command execution on the server (demonstrated with an `echo`, non-destructive). Full remote-code impact is inferred from the same mechanism but was not exercised.

## Evidence / PoC
Baseline (`ip=127.0.0.1`) → ping only. Proof (`ip=127.0.0.1 && echo CMDINJ-CONFIRMED`) → ping output followed by `CMDINJ-CONFIRMED` (raw: `evidence/reporting/raw/exec_base.txt`, `exec_proof.txt`). The difference is attributable to the injected command.

## Remediation
Do not build shell command strings from user input; validate the input strictly (e.g., IP format) and prefer APIs that do not invoke a shell; apply least privilege and disable unused OS features.

## Severity rationale
Command execution is high impact; evidence is a benign echo, not a destructive/full RCE demonstration. Reported High with the note that impact was demonstrated non-destructively.

## Limitations / remaining uncertainty
Only a benign `echo` was executed to establish the class; reverse-shell, file effect, or privileged execution were not attempted. This was a minimal non-destructive proof.