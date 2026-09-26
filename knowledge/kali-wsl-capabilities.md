# Kali / WSL2 Capability Manifest & Integration

Environment snapshot (discovered, not assumed). Tool availability does **not**
imply authorization.

## Execution boundary

| Environment | Provides |
| --- | --- |
| Windows | Cline, VS Code, PowerShell, Docker, browser, Burp (declared; see note) |
| Kali/WSL2 | Linux CLI tooling, network/security utilities, scripting, enumeration, protocol tools |

- Invoke Linux tools from the authorized workspace via WSL.
- Windows paths and Linux paths are **not** interchangeable.
- Do not expose unrelated Windows filesystem areas; use the dedicated hacking
  workspace only.

| Side | Path |
| --- | --- |
| Windows | `C:\Users\curbr\OneDrive\Desktop\Code\ai\hacking` |
| WSL | `/mnt/c/Users/curbr/OneDrive/Desktop/Code/ai/hacking` |

## WSL discovery (2026-09-16)

`wsl.exe -l -v` ->
```
docker-desktop    Stopped   2
kali-linux        Running   2
```
- **kali-linux** is WSL2, running, minimal **Kali GNU/Linux Rolling**,
  kernel `6.6.87.2-microsoft-standard-WSL2`.
- **docker-desktop** is the WSL default but currently stopped; `wsl -e ...`
  without `-d` targets the default and is unreliable here. Always specify
  `-d kali-linux`.
- Working directory inside a fresh `wsl -d kali-linux` shell is the shared
  workspace (`/mnt/c/.../hacking`), so the boundary already aligns.

## Invocation from Windows

```
wsl.exe -d kali-linux -e bash -lc "<command>"
```

Confirmed working. No wrapper/installation is required for the agent to invoke
Kali. An optional convenience could be a thin local script alias, but it is not
necessary for this environment.

## Installed tool capability (verified)

Legend: AVAILABLE = `command -v` found it; NOT INSTALLED = not found; UNKNOWN =
not yet verified this pass.

| Capability | Tool | Status |
| --- | --- | --- |
| HTTP_ANALYSIS | curl, wget, python3(pip3), openssl, nc | AVAILABLE |
| SERVICE_DISCOVERY | nmap | AVAILABLE |
| CONTENT_DISCOVERY | ffuf | AVAILABLE |
| DATA_PROCESSING | jq, grep, sed, awk, sort, base64, strings, gzip, tar | AVAILABLE |
| SCRIPTING | python3 (3.13.12), bash | AVAILABLE |
| DNS/WHOIS | dig, host, whois | AVAILABLE |
| REMOTE/GIT | ssh, scp, ftp, git | AVAILABLE |
| INJECTION_TESTING | sqlmap | AVAILABLE |
| ONLINE_LOGIN/CREDENTIAL | hydra | AVAILABLE |
| HTTP/HTTPS_INTERCEPTION | mitmproxy, mitmdump, mitmweb | AVAILABLE |

Not installed in this Kali: `gobuster, wfuzz, dirb, nikto, dnsrecon, whatweb,
john, hashcat, ncat, exiftool, sqlite3, unzip, 7z, xxd, file`.

Tool versions were not fully enumerated on the original 2026-09-16 pass (only
presence). Do not state a version unless freshly verified. Burp availability on
Windows was previously **UNKNOWN**; verified on 2026-09-23 as installed but NOT
running, edition unverified, and local API not integrated - see the verified
update below.

## Verified update (2026-09-23) - tooling integration phase

Whole-distro capability re-verification was performed read-only (a probe script;
no target traffic, no scanning). Installs used `apt-get` as WSL root
(`wsl -d kali-linux -u root`) because the default user `curby` requires a
password for `sudo` (no NOPASSWD entry). The installed tools remain invokable by
Cline's normal path (default user).

AVAILABLE + VERIFIED (all `command -v` present):
`curl wget python3 jq nmap ffuf nc openssl git dig host whois ssh scp ftp
base64 strings gzip tar sqlmap hydra mitmproxy`

Fresh versions (2026-09-23): curl 8.20.0, wget 1.25.0, python3 3.13.12,
jq 1.8.1, nmap 7.99, ffuf 2.1.0-dev, openssl 3.6.2, git 2.53.0,
SSH (OpenSSH 10.3p1), base64 (coreutils 9.10), strings (binutils 2.46),
gzip 1.13, tar 1.35, sqlmap 1.10.8#stable, hydra 9.7, mitmproxy 12.2.3.

NEWLY INSTALLED (2026-09-23; previously NOT AVAILABLE):
- sqlmap 1.10.8 (`/usr/bin/sqlmap`; package `sqlmap 1.10.8-1`)
- hydra 9.7 (`/usr/bin/hydra`; package `hydra 9.7-1`, CLI only; no hydra-gtk, no
  Kali metapackages installed)
- mitmproxy 12.2.3 (package `mitmproxy 12.2.3-0kali4`; provides `/usr/bin/mitmproxy`,
  `/usr/bin/mitmdump`, `/usr/bin/mitmweb`; bundled via python3-mitmproxy-rs; runs on
  Python 3.14.7 / OpenSSL 3.6.2). INSTALLED + VERIFIED ONLY - NOT integrated into any
  security-testing workflow: no proxy config, no interception, no certificate setup.

Burp Suite on Windows (2026-09-23) - status categories:
- INSTALLED VERIFIED: `C:\Users\curbr\AppData\Local\Programs\BurpSuite`
  (`BurpSuite.exe`, `burpsuite.jar`, bundled `jre`, `burpbrowser`). install4j
  config: applicationName "Burp Suite", applicationVersion **2026.8**, media
  `burpsuite_windows-x64_v2026_8` (build 2026-08-20).
- RUNNING: **NO** - no Burp/java process; no Burp local API/proxy listener.
- EDITION/activation: **UNKNOWN** - the unified 2026.8 installer is
  binary-identical for Community vs Professional; Burp has never been launched
  here (empty UserConfig/WorkspaceConfig), so there is no license/sign-in state
  to inspect. Installing is not activation.
- Local API / machine-accessible interface: **UNKNOWN / NOT YET INTEGRATED** -
  Burp's programmatic REST API is a Professional feature and requires the app
  running with the API enabled plus an API key. Do not claim integration merely
  because it is installed.
- Integration notes (analysis only; NOT configured): Burp is a native Windows
  app, so Cline (Windows) would use its localhost REST API from the Windows
  side; WSL2/Kali is not the natural path to drive it and adds nothing here.
  Enabling the API requires launching Burp with the REST API and a token - a
  future, separately-approved step, not performed in this phase.

## Capability -> tool mapping (conceptual)

| Capability | Map to |
| --- | --- |
| HTTP_ANALYSIS | curl / wget / Python / Burp / browser |
| SERVICE_DISCOVERY | nmap (in-scope only) |
| CONTENT_DISCOVERY | ffuf (authorized, in-scope) |
| DATA_PROCESSING | jq / Python / standard Unix tools |
| PROXY/INTERCEPTION | Burp (Windows) |
| SCRIPTING | Python / Bash |

## Command safety (Kali)

Powerful capabilities carry additional care. Evaluate every command by:
target, scope, purpose, expected effect, authorization, passive-vs-active,
availability impact, and whether it touches another system.

Caution categories include: broad network scanning, service enumeration outside
explicit scope, credential attacks, brute force, exploitation, destructive
commands, high-rate fuzzing, and availability-affecting requests.

Running a command inside Kali is **not** authorization. The rules in
`.clinerules/` and the authorized scope still apply unchanged.

## Integration decision

- Cline can already invoke WSL commands directly (`wsl -d kali-linux -e ...`).
- Additional integration (a bespoke bridge/wrapper) is **not required** and was
  not added. Keeping Windows/Kali invocation plain and documented avoids
  broadening filesystem access or adding moving parts.