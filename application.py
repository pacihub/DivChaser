from flask import Flask, render_template, request, jsonify, json, flash, redirect, session
from flask_session import Session
from cs50 import SQL
import requests

#for password hashing
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

#import functions
from functions import tickercheck, login_required

#configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response 

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#connect database
db = SQL("sqlite:///portfolio.db")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


#   /register
@app.route("/register", methods=["GET", "POST"])
def register():
        # check if username is entered and password fields match
        if request.method == 'POST':
            if not request.form.get("username"):
                return "must provide username"
            elif not request.form.get("password"):
                return "must provide password"
            elif not request.form.get("confirmation"):
                return "you must retype your password"
    
            if request.form.get("password") != request.form.get("confirmation"):
                return("passwords don't match")
    
            #check if username already exists
            check_if_exist = db.execute("SELECT * FROM userz WHERE username = :username",
                          username=request.form.get("username"))
                          
            if check_if_exist:
                return "existing username. Try logging in instead."
            else:
                db.execute("INSERT into userz (username, hash) VALUES (:username, :hash)",
                username = request.form.get("username"),
                hash = generate_password_hash(request.form.get("password")))
            return redirect("/login")
            
        else:
            return render_template("register.html")    
    
#   /login   
@app.route("/login", methods = ["GET", "POST"])
def login():
 
    #forgets any user_id
    session.clear()
    
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return "must provide username"

        # Ensure password was submitted
        elif not request.form.get("password"):
            return "must provide password"
        
        username_query = db.execute("SELECT * FROM userz WHERE username = :username",
                          username=request.form.get("username"))
#        print(username_query)

        # check if username exists                   
        if len(username_query) != 1:
            return "invalid username"
        
        #check if entered password is correct
        if not check_password_hash(username_query[0]["hash"], request.form.get("password")):
            return "wrong password"
        
        # Remember which user has logged in
        session["user_id"] = username_query[0]["id"]
        return redirect("/apiconnect")
    else:
        return render_template("login.html")

#   / enter API key and connect to AlphaVantage
@app.route("/apiconnect", methods=["GET", "POST"])  
@login_required

# Users must provide an API token
def apifn():
        if request.method == "POST":
            users_apitoken = request.form.get("api")
            session["apitoken"] = users_apitoken      # Store user's input in a session key, which is global
            return redirect('/')
        else:
            return render_template('apiconnect.html')

#   / home tab
@app.route("/")
@login_required
def homepage():
    return render_template("index.html")
    

@app.route("/explore", methods=["GET", "POST"])
@login_required
def search_stocks():
    if request.method == 'POST':
        
        #whatever the user entered in the front end casted to all UPPER case
        symbol = request.form.get("ticker").upper().strip()
        
        if not symbol:
            return "please enter a ticker"

        elif not tickercheck(symbol):
            return "not a valid ticker"
            
        # my function 'tickercheck' returns me a dict for XYZ stock for example per f-n definition
        # Storing the return dict from tickercheck in 'stockdata'
        stockdata = tickercheck(symbol)
        
        # I need to access stock data between routes, so I store it in Session dict which is global
        # and I can access those keys from different routes later
        session["ticker"] = stockdata["symbol"]
        session["name"] = stockdata["name"]
        session["beta"] = stockdata["beta"]
        session["sector"] = stockdata["sector"]
        session["divyield"] = stockdata["divyield"]
        session["industry"] = stockdata["industry"]
        session["divdate"] = stockdata["divdate"]
        session["exdivdate"] = stockdata["exdivdate"] 
#        session["payoutratio"] = stockdata["payoutratio"]
        session["divpershare"] = stockdata["divpershare"]
        
        print(stockdata)
        return render_template("stdata.html", stockdata = stockdata)
        
    else:
        return render_template("explore.html")
 

@app.route("/stdata", methods=["GET", "POST"])
def add_stock_to_portfolio():
        if request.method == 'POST':    
            
            #check if stock ticker is already in the database
            if db.execute("SELECT ticker FROM stockz WHERE ticker = :tickerz AND id = :id", 
            tickerz = session["ticker"],id = session["user_id"]):
                return "stock is already in portfolio"
            
            # otherwise it injects all stock data into db. \ is for new line continuation w/out breaking code
            # I access all these values from the global session variables
            else:
                db.execute("INSERT INTO stockz (id, stock_name, ticker, beta, sector, divyield, industry, dividend_date, \
                exdividend_date, divpershare) VALUES (:id, :stock_name, :ticker, :beta, :sector, :divyield, \
                :industry, :dividend_date, :exdividend_date, :divpershare)", id = session["user_id"], 
                stock_name = session["name"], ticker = session["ticker"],beta = session["beta"], 
                sector = session["sector"], divyield = session["divyield"], industry = session["industry"], dividend_date = session["divdate"],
                exdividend_date = session["exdivdate"], divpershare = session["divpershare"]) 
                      
                return redirect("/mystocks") 
                
                
@app.route("/newsearch", methods=["GET", "POST"]) 
def newsearch():
    return redirect('/explore')
    

#   /mystocks
@app.route("/mystocks", methods=["GET", "POST"])
@login_required
def mystocks():
#    if request.method == 'POST':
        #query a list of logged-in user's stocks.
        my_stocks = db.execute("SELECT *  FROM stockz WHERE id = :id ORDER BY divyield DESC", 
        id = session["user_id"])
        
        #query user's username to display on top of the html table
        current_user = db.execute("SELECT username FROM userz WHERE id = :id", id = session["user_id"])
#        print(my_stocks)
        return render_template("mystocks.html", my_stocks = my_stocks, user=current_user[0]["username"])

              
@app.route("/delstock", methods=["GET", "POST"])  
@login_required
def delstk():
    
    #delete stock from user's favorites upon their selection
    if request.method == "POST":
        del_element = request.form.get("delelement").upper()
        
        db.execute("DELETE FROM stockz WHERE ticker = :element AND id = :id",
        element = del_element,id = session["user_id"])
        return redirect("/mystocks")                    


@app.route("/contact", methods = ["GET","POST"])
def contact():
    
    if request.method == "GET":
        return render_template("contact.html")
    
    else:
        # grabs the info that user typed in fields and stores in variable
        feedback_name = request.form.get("name")
        feedback_email = request.form.get("email")
        feedback_message = request.form.get("message")
        
        # inject the information in the DB in contact_form table.
        db.execute("INSERT into contact_form (name, email, message) VALUES (:ime, :email, :message)",
            ime = feedback_name, email = feedback_email, message = feedback_message)
        return redirect('/')

#   /logout
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug = True)