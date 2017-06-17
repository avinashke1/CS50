from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    tempdata = db.execute("SELECT shares, symbol FROM portfolio WHERE id = :id",id=session["user_id"])
    TotalCash = 0
    for temp in tempdata:
        symbol = temp["symbol"]
        shares = temp["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        TotalCash += total
        db.execute("UPDATE portfolio SET price=:price, \total=:total WHERE id=:id AND symbol=:symbol",price=usd(stock["price"]),total=usd(total), id=session["user_id"], symbol=symbol)
    
    NewCash = db.execute("SELECT cash FROM users \WHERE id=:id", id=session["user_id"])
    
    TotalCash += NewCash[0]["cash"]
    

    NewProfile = db.execute("SELECT * from portfolio WHERE id=:id", id=session["user_id"])
                                    
    return render_template("index.html", stocks=NewProfile,cash=usd(NewCash[0]["cash"]), total= usd(TotalCash) )

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    if request.method == "GET":
        return render_template("buy.html")
    else:
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol")
        
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive integer")
        except:
            return apology("Shares must be positive integer")
      
        Money = db.execute("SELECT cash FROM users WHERE id = :id",id=session["user_id"])
        
        if not Money or float(Money[0]["cash"]) < stock["price"] * shares:
            return apology("Not enough money")
        
        db.execute("INSERT INTO histories (symbol, shares, price, id) VALUES(:symbol, :shares, :price, :id)",symbol=stock["symbol"], shares=shares,price=usd(stock["price"]), id=session["user_id"])
                 
        db.execute("UPDATE users SET cash = cash - :purchase WHERE id = :id",id=session["user_id"],purchase=stock["price"] * float(shares))
                        
        user_shares = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol=:symbol",id=session["user_id"], symbol=stock["symbol"])
                           
        if not user_shares:
            db.execute("INSERT INTO portfolio (name, shares, price, total, symbol, id) VALUES(:name, :shares, :price, :total, :symbol, :id)",name=stock["name"], shares=shares, price=usd(stock["price"]),total=usd(shares * stock["price"]),symbol=stock["symbol"], id=session["user_id"])
                        
        else:
            TotalShare = user_shares[0]["shares"] + shares
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol",shares=TotalShare, id=session["user_id"],symbol=stock["symbol"])
        
        return redirect(url_for("index"))
        

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    Cache = db.execute("SELECT * from histories WHERE id=:id", id=session["user_id"])
    
    return render_template("history.html", Cache=Cache)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("Must provide username")

        elif not request.form.get("password"):
            return apology("Must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = :username",username=request.form.get("username"))

        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        session["user_id"] = rows[0]["id"]

        return redirect(url_for("index"))

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    session.clear()

    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    if request.method == "POST":
        rows = lookup(request.form.get("symbol"))
        
        if not rows:
            return apology("Invalid Symbol")
            
        return render_template("quoted.html", stock=rows)
    
    else:
        return render_template("quote.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    if request.method == "POST":
        
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")
            
        # ensure password was submitted    
        elif not request.form.get("password"):
            return apology("Must provide password")
        
        # ensure password and verified password is the same
        elif request.form.get("password") != request.form.get("passwordagain"):
            return apology("password doesn't match")
        
        # insert the new user into users, storing the hash of the user's password
        result = db.execute("INSERT INTO users (username, hash)VALUES(:username, :hash)",username=request.form.get("username"),hash=pwd_context.encrypt(request.form.get("password")))
                 
        if not result:
            return apology("Username already exist")
        session["user_id"] = result
        return redirect(url_for("index"))
    
    else:
        return render_template("register.html")                

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "GET":
        return render_template("sell.html")
    else:
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid Symbol")

        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive integer")
        except:
            return apology("Shares must be positive integer")

        user_shares = db.execute("SELECT shares FROM portfolio WHERE id = :id AND symbol=:symbol",id=session["user_id"], symbol=stock["symbol"])

        if not user_shares or int(user_shares[0]["shares"]) < shares:
            return apology("Not enough shares")

        db.execute("INSERT INTO histories (symbol, shares, price, id)VALUES(:symbol, :shares, :price, :id)",symbol=stock["symbol"], shares=-shares,price=usd(stock["price"]), id=session["user_id"])
          
        db.execute("UPDATE users SET cash = cash + :purchase WHERE id = :id",id=session["user_id"],purchase=stock["price"] * float(shares))

        shares_total = user_shares[0]["shares"] - shares

        if shares_total == 0:
            db.execute("DELETE FROM portfolio WHERE id=:id AND symbol=:symbol",id=session["user_id"],symbol=stock["symbol"])

        else:
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id AND symbol=:symbol",shares=shares_total, id=session["user_id"],symbol=stock["symbol"])

        return redirect(url_for("index"))
        
@app.route("/loan", methods=["GET", "POST"])
@login_required
def loan():
    """Get a loan."""
    
    if request.method == "POST":

        try:
            loan = int(request.form.get("loan"))
            if loan < 0:
                return apology("Loan must be positive amount")
            elif loan > 1000:
                return apology("Cannot loan more than $1,000 at once")
        except:
            return apology("Loan must be positive integer")
            
        db.execute("UPDATE users SET cash = cash + :loan WHERE id = :id",loan=loan, id=session["user_id"])

        return apology("Loan is successful", "No need to pay me back")
    
    else:
        return render_template("loan.html")
