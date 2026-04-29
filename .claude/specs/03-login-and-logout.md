# Spec: Login and Logout

## Overview
This step implements session-based login and logout — the second half of Spendly's authentication system. A registered user submits their email and password; the server looks up the user, verifies the password with werkzeug, and stores the user's `id` in the Flask session on success. The logout route clears the session and redirects to the landing page. Together with Step 2, this completes the full auth cycle and gates access to future logged-in routes.

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, working `/register` route)

## Routes
- `GET /login` — renders the login form — public
- `POST /login` — verifies credentials, sets session, redirects to `/profile` on success — public
- `GET /logout` — clears session, redirects to `/` — logged-in (but safe to call even if not logged in)

## Database changes
No new tables or columns. Read-only query against the existing `users` table:
```sql
SELECT id, password_hash FROM users WHERE email = ?
```

## Templates
- **Modify:** `templates/login.html`
  - Fix action to use `url_for('login')`
  - Repopulate `email` field on failed login (`value="{{ email or '' }}"`)
  - The `{% if error %}` block is already present — no change needed there
- **Modify:** `templates/base.html`
  - Update nav links to show "Sign out" (linking to `/logout`) when `session.user_id` is set, and "Sign in" / "Get started" when it is not

## Files to change
- `app.py` — add `POST` to `/login`; implement `/logout`; add `secret_key`; add `session` to flask imports; add `check_password_hash` to werkzeug imports; add `get_user_by_email` to db imports
- `database/db.py` — add `get_user_by_email(email)` helper
- `templates/login.html` — fix form action; repopulate email on error
- `templates/base.html` — conditional nav links based on session

## Files to create
None.

## New dependencies
No new pip packages. Use:
- `flask.session` (already available in Flask)
- `werkzeug.security.check_password_hash` (already installed)

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — no f-strings in SQL
- Password verified with `werkzeug.security.check_password_hash` — never compare plaintext
- `app.secret_key` must be set before sessions work — use a hardcoded dev key for now (e.g. `"spendly-dev-secret"`)
- Store only `user_id` (integer) in the session — never store name, email, or password hash
- Logout must call `session.clear()` — do not manually delete individual keys
- On failed login: show a generic error ("Invalid email or password.") — do not reveal which field was wrong
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic (`get_user_by_email`) in `database/db.py`, not inline in the route

## Definition of done
- [ ] `GET /login` renders the form
- [ ] Correct credentials → session contains `user_id`, redirects to `/profile`
- [ ] Wrong password → inline error "Invalid email or password.", email field repopulated
- [ ] Unknown email → same generic error (no user-enumeration)
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] After logout, `session` contains no `user_id`
- [ ] Nav shows "Sign out" link when logged in, "Sign in" / "Get started" when logged out
- [ ] App starts without errors
