# WebGoat — Observed Lesson Assignment-Endpoint Map (Authenticated, Read-Only)

- Date: 2026-09-26
- Method: benign `GET /WebGoat/<Lesson>.lesson` for each lesson named in the
  observed menu catalog; assignment endpoints parsed from `form.attack-form`
  elements (`action`, `method`, parameter `name`s). Raw per-lesson artifact
  files under `evidence/reporting/raw/webgoat_read_<Lesson>.lesson`.
- **No form was submitted, no data mutated.** These are OBSERVED endpoint
  definitions only; behavior/validation of each is an UNTESTED unknown.
- Destructive/admin controls (e.g. `service/restartlesson.mvc`) are excluded
  and off-limits.

### WebWolfIntroduction.lesson
- `/WebGoat/WebWolf/landing` POST — params: (none)

### HttpBasics.lesson
- `/WebGoat/HttpBasics/attack1` POST — params: person, SUBMIT
- `/WebGoat/HttpBasics/externalcheck` POST — params: code
- `/WebGoat/HttpBasics/attack2` POST — params: magic_num, answer, magic_answer, SUBMIT
- `/WebGoat/HttpBasics/quiz` POST — params: Quiz_solutions

### HttpProxies.lesson
- `/WebGoat/HttpProxies/intercept-request` POST — params: changeMe
- `/WebGoat/HttpProxies/intercept-request` POST — params: changeMe

### ChromeDevTools.lesson
- `/WebGoat/ChromeDevTools/dummy` POST — params: successMessage, submitMessage
- `/WebGoat/ChromeDevTools/network` POST — params: networkNum, SUBMIT
- `/WebGoat/ChromeDevTools/network` POST — params: number, Submit, network_num

### CIA.lesson
- `/WebGoat/cia/quiz` POST — params: Quiz_solutions

### LessonTemplate.lesson
- `/WebGoat/lesson-template/sample-attack` POST — params: param1, param2, submit

### OpenRedirect.lesson
- `/WebGoat/OpenRedirect/task1` POST — params: url
- `/WebGoat/OpenRedirect/task2` POST — params: url
- `/WebGoat/OpenRedirect/task3` POST — params: target, token
- `/WebGoat/OpenRedirect/task4` POST — params: target
- `/WebGoat/OpenRedirect/quiz` POST — params: Quiz_solutions
- `/WebGoat/OpenRedirect/mitigation` POST — params: url
- `/WebGoat/OpenRedirect/safe` GET — params: destId

### HijackSession.lesson
- `/WebGoat/HijackSession/login` POST — params: username, password

### IDOR.lesson
- `/WebGoat/IDOR/login` POST — params: username, password, submit
- `/WebGoat/IDOR/profile` GET — params: View Profile
- `/WebGoat/IDOR/diff-attributes` POST — params: attributes, Submit Diffs
- `/WebGoat/IDOR/profile/alt-path` POST — params: url, submit
- `/WebGoat/IDOR/profile/{userId}` GET — params: View Profile
- `/WebGoat/IDOR/profile/{userId}` GET — params: View Profile

### MissingFunctionAC.lesson
- `/WebGoat/access-control/hidden-menu` POST — params: hiddenMenu1, hiddenMenu2, submit
- `/WebGoat/access-control/user-hash` POST — params: userHash, submit
- `/WebGoat/access-control/user-hash-fix` POST — params: userHash, submit

### SpoofCookie.lesson
- `/WebGoat/SpoofCookie/login` POST — params: username, password

### Cryptography.lesson
- `/WebGoat/crypto/encoding/basic-auth` POST — params: answer_user, answer_pwd, SUBMIT
- `/WebGoat/crypto/encoding/xor` POST — params: answer_pwd1, SUBMIT
- `/WebGoat/crypto/hashing` POST — params: answer_pwd1, answer_pwd2, SUBMIT
- `/WebGoat/crypto/signing/verify` POST — params: modulus, signature, SUBMIT
- `/WebGoat/crypto/secure/defaults` POST — params: secretText, secretFileName, SUBMIT

### SqlInjection.lesson
- `/WebGoat/SqlInjection/attack2` POST — params: query
- `/WebGoat/SqlInjection/attack3` POST — params: query
- `/WebGoat/SqlInjection/attack4` POST — params: query
- `/WebGoat/SqlInjection/attack5` POST — params: query
- `/WebGoat/SqlInjection/assignment5a` POST — params: account, operator, injection, Get Account Info
- `/WebGoat/SqlInjection/assignment5b` POST — params: login_count, userid, Get Account Info
- `/WebGoat/SqlInjection/attack8` POST — params: name, auth_tan
- `/WebGoat/SqlInjection/attack9` POST — params: name, auth_tan
- `/WebGoat/SqlInjection/attack10` POST — params: action_string

### SqlInjectionAdvanced.lesson
- `/WebGoat/SqlInjectionAdvanced/attack6a` POST — params: userid_6a, Get Account Info
- `/WebGoat/SqlInjectionAdvanced/attack6b` POST — params: userid_6b, Check Dave's Password:
- `/WebGoat/SqlInjectionAdvanced/login` POST — params: username_login, password_login, remember, login-submit
- `/WebGoat/SqlInjectionAdvanced/register` PUT — params: username_reg, email_reg, password_reg, confirm_password_reg, register-submit
- `/WebGoat/SqlInjectionAdvanced/quiz` POST — params: Quiz_solutions

### SqlInjectionMitigations.lesson
- `/WebGoat/SqlInjectionMitigations/attack10a` POST — params: field1, field2, field3, field4, field5, field6, field7
- `/WebGoat/SqlInjectionMitigations/attack10b` POST — params: editor
- `/WebGoat/SqlOnlyInputValidation/attack` POST — params: userid_sql_only_input_validation, Get Account Info
- `/WebGoat/SqlOnlyInputValidationOnKeywords/attack` POST — params: userid_sql_only_input_validation_on_keywords, Get Account Info
- `/WebGoat/SqlInjectionMitigations/attack12a` POST — params: (none)
- `/WebGoat/SqlInjectionMitigations/attack12a` POST — params: ip

### CrossSiteScripting.lesson
- `/WebGoat/CrossSiteScripting/attack1` POST — params: checkboxAttack1, answer
- `/WebGoat/CrossSiteScripting/attack5a` GET — params: QTY1, QTY2, QTY3, QTY4, field1, field2, SUBMIT
- `/WebGoat/CrossSiteScripting/attack6a` POST — params: DOMTestRoute, SubmitTestRoute
- `/WebGoat/CrossSiteScripting/dom-follow-up` POST — params: successMessage, submitMessage
- `/WebGoat/CrossSiteScripting/quiz` POST — params: Quiz_solutions

### CrossSiteScriptingStored.lesson
- `/WebGoat/CrossSiteScriptingStored/stored-xss-follow-up` POST — params: successMessage, submitMessage

### CrossSiteScriptingMitigation.lesson
- `/WebGoat/CrossSiteScripting/attack3` POST — params: editor
- `/WebGoat/CrossSiteScripting/attack4` POST — params: editor2

### PathTraversal.lesson
- `/WebGoat/PathTraversal/profile-upload` POST — params: uploadedFile, fullName, email, password
- `/WebGoat/PathTraversal/profile-upload-fix` POST — params: uploadedFile, fullName, email, password
- `/WebGoat/PathTraversal/profile-upload-remove-user-input` POST — params: uploadedFile, fullName, email, password
- `/WebGoat/PathTraversal/random` POST — params: secret
- `/WebGoat/PathTraversal/zip-slip` POST — params: uploadedFile, fullName, email, password

### CSRF.lesson
- `/WebGoat/csrf/basic-get-flag` POST — params: csrf, submit
- `/WebGoat/csrf/confirm-flag-1` POST — params: confirmFlagVal, submit
- `/WebGoat/csrf/review` POST — params: reviewText, stars, validateReq, submit
- `/WebGoat/csrf/feedback/message` POST — params: name, email, subject, message
- `/WebGoat/csrf/feedback` POST — params: confirmFlagVal, submit
- `/WebGoat/csrf/login` POST — params: submit

### SecurityMisconfiguration.lesson
- `/WebGoat/SecurityMisconfiguration/task1` POST — params: username, password
- `/WebGoat/SecurityMisconfiguration/task2` POST — params: token
- `/WebGoat/SecurityMisconfiguration/task3` POST — params: apiKey
- `/WebGoat/SecurityMisconfiguration/task4` POST — params: envEnabled, healthDetails, defaultUser, defaultPassword

### XXE.lesson
- `/WebGoat/xxe/simple` POST — params: (none)
- `/WebGoat/xxe/content-type` POST — params: (none)
- `/WebGoat/xxe/blind` POST — params: (none)

### VulnerableComponents.lesson
- `/WebGoat/VulnerableComponents/attack1` POST — params: payload, SUBMIT

### AuthBypass.lesson
- `/WebGoat/auth-bypass/verify-account` POST — params: secQuestion0, secQuestion1, jsEnabled, verifyMethod, userId, submit
- `/WebGoat/auth-bypass/verify-account` POST — params: newPassword, newPasswordConfirm, userId, submit

### InsecureLogin.lesson
- `/WebGoat/InsecureLogin/task` POST — params: (none)
- `/WebGoat/InsecureLogin/task` POST — params: username, password

### JWT.lesson
- `/WebGoat/JWT/decode` POST — params: jwt-encode-user
- `/WebGoat/JWT/votings` POST — params: (none)
- `/WebGoat/JWT/quiz` POST — params: Quiz_solutions
- `/WebGoat/JWT/secret` POST — params: token
- `/WebGoat/JWT/refresh/checkout` POST — params: (none)
- `/WebGoat/JWT/jku/delete?token=eyJ0eXAiOiJKV1QiLCJqa3UiOiJodHRwOi8vMTI3LjAuMC4xOjgwODAvV2ViR29hdC9pbWFnZXMvandrcy5qc29uIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJXZWJHb2F0IFRva2VuIEJ1aWxkZXIiLCJpYXQiOjE3NzczODQ4NjEsImV4cCI6MjIxOTIzNDQ2MSwiYXVkIjoid2ViZ29hdC5vcmciLCJzdWIiOiJqZXJyeUB3ZWJnb2F0LmNvbSIsInVzZXJuYW1lIjoiSmVycnkiLCJFbWFpbCI6ImplcnJ5QHdlYmdvYXQuY29tIiwiUm9sZSI6WyJDYXQiXX0.P6x2mSeN58GVRs6zz3OESnIwqdA9WND1pnBtix8c760j3_V4TPuQylfKA7TIQ7CN8dtTF0hY_5T-toa8VagkHvy27fYBDNK_XTwRjjoQu1U279e7ILuPvj53lkTOL5vtTYl5FGo4yRGXObPHdOka3tFXTO3296XAqUXiNSmLHCKO_rZiNX8zJJssVyUkGXA7cgGKZn_a77kndxsUukGGaZggqm2kBZng2SQbz3-6Lkrav6QU2GTwKXjuRLt852KuCSqpQYSyPoBWn3IuvgolrtUbb_BCsWX5tSKdXPp3Ffe592wDf_j92THukeKhC88Mu4_0KdwkMMovzCeH7YGXOw` POST — params: (none)
- `/WebGoat/JWT/kid/delete?token=eyJ0eXAiOiJKV1QiLCJraWQiOiJ3ZWJnb2F0X2tleSIsImFsZyI6IkhTMjU2In0.ewogICJpc3MiOiAiV2ViR29hdCBUb2tlbiBCdWlsZGVyIiwKICAiaWF0IjogMTUyNDIxMDkwNCwKICAiZXhwIjogMTYxODkwNTMwNCwKICAiYXVkIjogIndlYmdvYXQub3JnIiwKICAic3ViIjogImplcnJ5QHdlYmdvYXQuY29tIiwKICAidXNlcm5hbWUiOiAiSmVycnkiLAogICJFbWFpbCI6ICJqZXJyeUB3ZWJnb2F0LmNvbSIsCiAgIlJvbGUiOiBbCiAgICAiQ2F0IgogIF0KfQ.CgZ27DzgVW8gzc0n6izOU638uUCi6UhiOJKYzoEZGE8` POST — params: (none)

### PasswordReset.lesson
- `/WebGoat/PasswordReset/simple-mail` POST — params: email, password
- `/WebGoat/PasswordReset/simple-mail/reset` POST — params: emailReset
- `/WebGoat/PasswordReset/questions` POST — params: username, securityQuestion
- `/WebGoat/PasswordReset/SecurityQuestions` POST — params: question, Check Question
- `/WebGoat/PasswordReset/reset/login` POST — params: email, password
- `/WebGoat/PasswordReset/ForgotPassword/create-password-reset-link` POST — params: email

### SecurePasswords.lesson
- `/WebGoat/SecurePasswords/assignment` POST — params: password

### InsecureDeserialization.lesson
- `/WebGoat/InsecureDeserialization/task` POST — params: token

### LogSpoofing.lesson
- `/WebGoat/LogSpoofing/log-spoofing` POST — params: username, password
- `/WebGoat/LogSpoofing/log-bleeding` POST — params: username, password

### SSRF.lesson
- `/WebGoat/SSRF/task1` POST — params: url, Steal the Cheese
- `/WebGoat/SSRF/task2` POST — params: url, try this

### BypassRestrictions.lesson
- `/WebGoat/BypassRestrictions/FieldRestrictions` POST — params: select, radio, radio, checkbox, shortInput, readOnlyInput
- `/WebGoat/BypassRestrictions/frontendValidation` POST — params: field1, field2, field3, field4, field5, field6, field7, error

### ClientSideFiltering.lesson
- `/WebGoat/clientSideFiltering/attack1` POST — params: userID, UserSelect, answer, SUBMIT
- `/WebGoat/clientSideFiltering/getItForFree` POST — params: checkoutCode

### HtmlTampering.lesson
- `/WebGoat/HtmlTampering/task` POST — params: QTY, Total

### ChallengeIntro.lesson
- (no `attack-form` assignment endpoints in this page)

### Challenge1.lesson
- `/WebGoat/challenge/1` POST — params: (none)
- `/WebGoat/challenge/flag/1` POST — params: flag

### Challenge5.lesson
- `/WebGoat/challenge/5` POST — params: username_login, password_login, remember, login-submit
- `/WebGoat/challenge/flag/5` POST — params: flag

### Challenge7.lesson
- `/WebGoat/challenge/7` POST — params: email, recover-submit, token
- `/WebGoat/challenge/flag/7` POST — params: flag

### Challenge8.lesson
- `/WebGoat/challenge/flag/8` POST — params: flag

### WebGoatIntroduction.lesson (captured separately)
- `POST /WebGoat/WebGoat/mail` — params: uniqueCode
- `POST /WebGoat/WebGoat/mail/send` — params: email
