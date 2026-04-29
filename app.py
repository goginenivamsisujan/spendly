import sqlite3

from flask import Flask, render_template, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = "spendly-dev-secret"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("register.html")

    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm  = request.form.get("confirm_password", "")

    error = None
    if not name:
        error = "Full name is required."
    elif not email:
        error = "Email address is required."
    elif len(password) < 8:
        error = "Password must be at least 8 characters."
    elif password != confirm:
        error = "Passwords do not match."

    if error:
        return render_template("register.html", error=error, name=name, email=email)

    try:
        create_user(name, email, generate_password_hash(password))
    except sqlite3.IntegrityError:
        return render_template("register.html",
                               error="An account with that email already exists.",
                               name=name, email=email)

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html",
                               error="Invalid email or password.",
                               email=email)

    session.clear()
    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "January 2026",
    }
    stats = {
        "total_spent": "₹349.49",
        "transaction_count": 8,
        "top_category": "Bills",
    }
    transactions = [
        {"date": "Apr 21", "description": "Groceries",       "category": "Food",          "amount": "₹22.00"},
        {"date": "Apr 18", "description": "Miscellaneous",   "category": "Other",         "amount": "₹9.99"},
        {"date": "Apr 14", "description": "Clothing",        "category": "Shopping",      "amount": "₹80.00"},
        {"date": "Apr 10", "description": "Movie tickets",   "category": "Entertainment", "amount": "₹25.00"},
        {"date": "Apr 08", "description": "Pharmacy",        "category": "Health",        "amount": "₹35.00"},
        {"date": "Apr 05", "description": "Electricity bill","category": "Bills",         "amount": "₹120.00"},
        {"date": "Apr 03", "description": "Monthly bus pass","category": "Transport",     "amount": "₹45.00"},
        {"date": "Apr 01", "description": "Lunch at cafe",   "category": "Food",          "amount": "₹12.50"},
    ]
    categories = [
        {"name": "Bills",         "total": "₹120.00", "pct": 34},
        {"name": "Shopping",      "total": "₹80.00",  "pct": 23},
        {"name": "Transport",     "total": "₹45.00",  "pct": 13},
        {"name": "Health",        "total": "₹35.00",  "pct": 10},
        {"name": "Food",          "total": "₹34.50",  "pct": 10},
        {"name": "Entertainment", "total": "₹25.00",  "pct": 7},
        {"name": "Other",         "total": "₹9.99",   "pct": 3},
    ]
    return render_template("profile.html",
                           user=user, stats=stats,
                           transactions=transactions, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
