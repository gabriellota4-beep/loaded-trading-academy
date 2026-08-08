# Testing

## Automated tests

Command:

```bash
python manage.py test
```

| Area | Test coverage | Expected result |
|---|---|---|
| Registration | Valid username, unique email, strong password | Account created and learner redirected to profile |
| Catalogue | Public list and detail requests | Published course information is visible |
| Course management | Regular user requests staff route | Access is denied by redirect |
| Reviews | Paid learner submits review | One review is stored |
| Review authorization | Non-owner submits review | Review is not stored |
| Lesson authorization | Non-owner opens lesson URL | Redirected to public course page |
| Lesson authorization | Paid learner opens lesson URL | Protected lesson renders |
| Checkout authentication | Anonymous user posts checkout | Redirected to login |
| Stripe configuration | Secret key missing | No abandoned pending order remains |
| Return-page security | Pending order success URL receives arbitrary session ID | Order remains pending |
| Webhook fulfilment | Verified paid event matches order and session | Order becomes paid and intent ID is stored |
| Webhook protection | Event session does not match order | Order remains pending |
| Learner dashboard | Profile has a paid order | Owned course appears in My Learning |

Additional command:

```bash
python manage.py check
```

Expected: no system-check issues.

## Manual functional testing

| Feature | Steps | Expected result | Status |
|---|---|---|---|
| Navigation | Open every header/footer link on desktop | Correct page opens; no broken links | Pass locally |
| Mobile menu | Resize below 700px and select Menu | Menu opens, closes, and reports expanded state | Pass locally |
| Search | Search using part of a course title/summary | Matching courses display | Pass locally |
| Empty search | Search for an unknown phrase | Helpful empty result displays | Pass locally |
| Registration | Submit missing/invalid fields | Inline Django validation displays | Pass locally |
| Authentication | Log in and log out | Navigation and protected access update | Pass locally |
| Profile | Change experience, display name, and market | Saved values remain after redirect | Pass locally |
| Course CRUD | As staff create, edit, unpublish, and delete a test course | UI and database immediately reflect changes | Pass locally |
| CRUD authorization | Repeat staff routes as normal user | Access is denied | Pass locally |
| Unpublished course | Open its known public URL | 404 returned | Pass locally |
| Checkout | Purchase using Stripe test card | Stripe-hosted page returns to processing/success view | Requires deployed Stripe test keys |
| Webhook | Complete a Stripe test payment | Order becomes paid and lesson appears | Requires deployed webhook |
| Duplicate purchase | Attempt checkout for an owned course | User is informed and no new order is created | Pass locally |
| Lesson privacy | Copy lesson URL into logged-out/private browser | Login/access protection prevents content exposure | Pass locally |
| Review create/update | Save twice on the same owned course | Existing review updates; duplicate is not created | Pass locally |
| Admin | Open `/admin/` as superuser | Models can be managed | Pass locally |
| Error handling | Request an unknown URL | Standard 404 response displays | Pass locally |

## Responsive testing

Layouts should be checked at minimum at these widths:

- 320px mobile
- 375px mobile
- 768px tablet
- 1024px laptop
- 1440px desktop

The course grid uses `auto-fit` and the navigation switches to the JavaScript toggle at 700px. Forms use full-width controls to avoid horizontal overflow.

## Browser testing

Final deployed checks must be recorded for current versions of:

- Google Chrome
- Microsoft Edge
- Mozilla Firefox
- Safari or iOS Safari when available

## Validation

Before submission, validate rendered pages with:

- W3C HTML Validator
- W3C CSS Validator
- Chrome Lighthouse for accessibility, best practices, SEO, and performance
- Python style check (`python -m flake8` if installed)

Any third-party warnings caused by generated Stripe or Django markup should be distinguished from project-authored code.

## Security tests

- Secret files and `.env` are ignored by Git.
- Payment state cannot be changed through the success page.
- Stripe signatures are verified before event processing.
- Order number and unique Checkout Session must both match.
- CSRF protection remains active for user forms; only the signed Stripe webhook is exempt.
- Staff-only mutations use server-side authorization.
- Paid lesson access is evaluated server-side for every request.
- Production mode enables HTTPS redirect, HSTS, and secure cookies.

## Bugs found and resolved

| Bug | Cause | Resolution |
|---|---|---|
| Return page could mark an order paid | Browser-provided Checkout Session was retrieved after redirect | Removed fulfilment from the return page; added signed webhook fulfilment |
| Any logged-in learner could review any course | Review route checked login but not ownership | Reused paid-access authorization before saving reviews |
| No private learning destination | Initial course model only stored public description | Added protected lesson content and My Learning dashboard |
| Registration did not collect email | Default Django form omits email | Added required, normalized, unique email form field |
| Missing Stripe key left potential incomplete state | Order was created before configuration check | Pending order is deleted and user receives a clear message |

## Final deployment retest

The following remain to be completed against the live URL immediately after deployment:

- real PostgreSQL migration;
- Stripe test checkout and webhook delivery;
- live responsive/browser matrix;
- live Lighthouse results;
- deployed link and screenshots in `README.md`.
