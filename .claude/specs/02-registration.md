# Spec: Registration

## Overview
This step implements user registration — the first half of Spendly's authentication system. A visitor can submit their name, email, and password through a form. The server validates the input, hashes the password, inserts the new user into the `users` table, and redirects to the login page on success. Duplicate email addresses are rejected with a clear inline error. This step converts the existing `GET /register` stub into a fully working route pair.

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()` must exist)

## Routes
- `GET /register` — renders the registration form — public
- `POST /register` — processes form submission, inserts user, redirects to `/login` on success — public

## Database changes
No new tables or columns. Uses the existing `users` table:
- `name` (TEXT NOT NULL)
- `email` (TEXT UNIQUE NOT NULL)
- `password_hash` (TEXT NOT NULL)

A duplicate email will trigger a UNIQUE constraint violation — catch it and show an inline error.

## Templates
- **Modify:** `templates/register.html`
  - Add `<form method="POST" action="{{ url_for('register') }}">` with fields: `name`, `email`, `password`, `confirm_password`
  - Display inline error messages (from flashed messages or a passed `error` variable)
  - All field values must be re-populated on validation failure (except passwords)
  - Link to `/login` for users who already have an account

## Files to change
- `app.py` — convert `GET /register` to a two-method route; add POST handler logic
- `templates/register.html` — add form, error display, and field repopulation
- `database/db.py` — add `create_user(name, email, password_hash)` helper

## Files to create
None.

## New dependencies
No new dependencies. Use:
- `werkzeug.security.generate_password_hash` (already installed)
- `flask.request`, `flask.redirect`, `flask.url_for`, `flask.flash` (already available)

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — no f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before any DB insert
- Plaintext passwords must never be stored or logged
- Validate server-side: name non-empty, valid email format, password ≥ 8 chars, passwords match
- On duplicate email: catch `sqlite3.IntegrityError`, show "An account with that email already exists."
- On success: `redirect(url_for('login'))` — do not render the register template
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- DB logic (the INSERT) goes in `database/db.py`, not inline in the route

## Definition of done
- [ ] `GET /register` renders the registration form with name, email, password, confirm password fields
- [ ] Submitting valid data creates a new row in `users` with a hashed password
- [ ] Successful registration redirects to `/login`
- [ ] Submitting a duplicate email shows an inline error and does not create a duplicate row
- [ ] Submitting mismatched passwords shows an inline error
- [ ] Submitting a password shorter than 8 characters shows an inline error
- [ ] Form fields (name, email) are repopulated after a validation error
- [ ] Password fields are cleared after a validation error
- [ ] No plaintext password appears in the database (`password_hash` starts with `pbkdf2:` or `scrypt:`)
- [ ] App starts without errors
