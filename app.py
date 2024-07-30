from flask import Flask, render_template, request, flash, abort, session, redirect
from cs50 import SQL
import datetime
import re
import secrets

# Configure app
app = Flask("__name__")
app.secret_key = secrets.token_hex(16)

# Configure database with cs50 library
db = SQL("sqlite:///waitlist.db")

@app.route("/", methods=["GET", "POST"])
def index():
    """Waitlist landing page"""
    if request.method == "GET":
        return render_template("index.html")

    # User reached this route via POST (by submitting a form)
    if not request.form.get("email") or not is_email(request.form.get("email")):
        return apology("The email address you provided is invalid."), 400
    # Check if email exist in the database
    if db.execute("SELECT id FROM waitlist WHERE email = ?;", request.form.get("email")):
        flash("The email address you provided already exists in our database", "danger")
        return redirect("/")

    # Save user email into a database
    db.execute("INSERT INTO waitlist (email, register_date) VALUES (?, ?);", request.form.get("email"), datetime.datetime.now())
    flash("Thank you for signing up for our waitlist! We're excited to have you join us soon. Stay tuned for updates!", "success")
    return redirect("/")

@app.route("/admin")
def admin_page():
    """Admin page"""
    if request.args.get("code") == "headstarter":
        email_count = db.execute("SELECT COUNT(*) AS count FROM waitlist;")[0]["count"]
        return f"<h1>Count:  {email_count} </h1>"
    else:
        return apology("You are unauthorized to access this page", code=401), 401

def is_email(email: str) -> bool:
    """Validate email"""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message))


application = app