import os

from decimal import Decimal
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from sql import *
from helpers import apology, login_required, lookup, usd



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL('complaints.db')
# Make sure API key is set
#if not os.environ.get("API_KEY"):
 #   raise RuntimeError("API_KEY not set")



@app.route("/view")
def view():
    complaints = db.execute("SELECT picture, tag, cds, dsc, score, valid, status transactions WHERE ___ GROUP BY _____")
    return render_template("index.html", complaints=complaints)



@app.route("/", methods=["GET", "POST"])
def buy():
    if request.method == "POST":
            db.execute("INSERT INTO complaints (picture, tag, cds, dsc, score, valid, status) VALUES(:user_id, :symbol, :cds, :dsc, :score, :valid, :status)",
            user_id=session["user_id"],
            dsc=request.form.get("dsc"),
            shares=shares,
            price=price_per_share)
            flash("Bought!")
            return redirect("/")
    else:
         return render_template("buy.html", symbolauto="", Cash=Cash)



@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")



@app.route("/history")
@login_required
def history():
    cash_user = db.execute("SELECT cash from users where id = :Id", Id=session["user_id"])
    cash_userlist = list(cash_user[0].values())
    Cash=round(Decimal(float(cash_userlist[0])),4)
    historystock = db.execute("SELECT symbol, shares, price_per_share, created_at FROM transactions WHERE user_id = :user_id ORDER BY created_at DESC", user_id=session["user_id"])
    return render_template("history.html", historystock=historystock, Cash=Cash)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
# Ensure username was submitted
    print ("reached1")
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provides username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                              username=request.form.get("username"))

        if len(rows) == 1:
            return apology("Sorry, the username already exists", 403)
        else:
            if request.form.get("password") != request.form.get("confirmation"):
                return apology("Sorry, the passwords don't match", 403)
            else:
                new_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :HASH)", username=request.form.get("username"), HASH=generate_password_hash(request.form.get("password")))
                rows = db.execute("SELECT * FROM users WHERE username = :username",
                                    username=request.form.get("username"))
                session["user_id"] = new_id
                return redirect("/")
    else:
        return render_template("register.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
