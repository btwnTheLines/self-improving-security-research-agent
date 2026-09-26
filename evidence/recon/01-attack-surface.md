# Reconnaissance — Attack Surface Map

Target: `http://localhost:3000` (local OWASP Juice Shop, Docker)
Date: 2026-09-14
Scope: **Recon/attack-surface mapping only. No exploitation performed.**
All probes below were read-only GET/HEAD requests or static analysis of the
client bundle downloaded to the local temp dir.

## Reconnaissance performed

1. Confirmed app is running: `GET /` -> HTTP 200, Angular 2 SPA.
2. Observed response headers:
   - `Access-Control-Allow-Origin: *`
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: SAMEORIGIN`
   - `Feature-Policy: payment 'self'`
   - `X-Recruiting: /#/jobs`
3. Fetched `robots.txt` -> `Disallow: /ftp` (hint of an FTP service).
4. Downloaded `main.js` (~1.2 MB) to local temp and statically extracted
   client routes and REST/API endpoint literals (template literals).
5. Confirmed read-only probes:
   - `GET /api/Products` -> 200, full product objects (price, deluxePrice, timestamps)
   - `GET /rest/products/search?q=apple` -> 200, JSON results
   - `GET /rest/user/whoami` -> 200, `{"user":{}}` when unauthenticated

## Client-side routes (SPA functional areas)

- Catalog/shop: `search`, `basket`, `order-summary`, `payment/:entity`,
  `order-completion/:id`, `delivery-method`, `address/*`, `saved-payment-methods`
- Auth/account: `login`, `register`, `forgot-password`, `change-password`,
  `two-factor-authentication`, `2fa/enter`, `last-login-ip`, `data-export`,
  `privacy-security`, `deluxe-membership`, `wallet`, `wallet-web3`
- Communication: `contact`, `chatbot`, `conversation/:id`, `complain`,
  `photo-wall`, `privacy-policy`
- Admin/ops: `administration`, `accounting`, `score-board`, `recycle`,
  `bee-haven`, `juicy-nft`, `web3-sandbox`, `hacking-instructor`,
  `coding-challenge/:challengeKey`
- Civ: `about`, `track-result`, `track-result/new`, `403`, `**`

## REST/API endpoints (from client bundle)

- `/api/Users`, `/api/Products`, `/api/Feedbacks`, `/api/Recycles`,
  `/api/Complaints`, `/api/Deliverys`, `/api/Quantitys`, `/api/BasketItems`,
  `/api/Cards`, `/api/Addresss`, `/api/Challenges`, `/api/Hints`,
  `/api/SecurityQuestions`, `/api/SecurityAnswers`
- `/rest/user/login`, `/rest/user/whoami`, `/rest/user/change-password`,
  `/rest/user/reset-password`, `/rest/user/security-question`,
  `/rest/user/authentication-details/`, `/rest/user` (reg.)
- `/rest/products/search`, `/rest/products`, `/rest/basket/`,
  `/rest/track-order`, `/rest/order-history`, `/rest/deluxe-membership`,
  `/rest/wallet/balance`, `/rest/country-mapping`, `/rest/languages`
- `/rest/2fa/setup|status|verify|disable`
- `/rest/captcha`, `/rest/image-captcha/`, `/rest/chat`,
  `/rest/repeat-notification`, `/rest/admin`, `/rest/memories`,
  `/rest/saveLoginIp`, `/rest/web3`
- `/rest/continue-code`, `/rest/continue-code/apply/`,
  `/rest/continue-code-findIt`, `/rest/continue-code-fixIt` (+ `/apply/`)

## Authentication & authorization mechanisms (observed)

- Login response returns a JWT (`token`) stored in `localStorage['token']`.
- Requests send `Authorization: Bearer <token>`.
- `GET /rest/user/whoami` decodes the JWT server-side; returns `{"user":{}}`
  when no/untrusted token present.
- 2FA state machine (`/rest/2fa/*`) and `totp_tmp_token` in localStorage.
- Role model (admin vs user) implied by authorization checks on admin routes
  (`administration`, `accounting`, `/rest/admin`).

## Input points identified

- HTTP query params: `q` (product search), `page`/sort likely on lists.
- JSON bodies: all `/api/*` and `/rest/*` mutations (login, register, feedback,
  complaints, reviews, addresses, cards, basket, orders, continue-code apply).
- URL path params: `/api/Challenges/:id`, `/rest/basket/:id`,
  `/rest/user/authentication-details/:id`, route params (`/address/edit/:id`).
- File upload endpoints implied by bundle (`/file-upload`, image-captcha).
- Client-side directive/`<routerLink>` navigation (SPA).