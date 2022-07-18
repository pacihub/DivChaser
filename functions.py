import requests
from flask import redirect, render_template, request, session
from functools import wraps

# check if ticker is valid
def tickercheck(i):
    key = session["apitoken"]
    try:
        # API return value
        response = requests.get(f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={i}&apikey={key}")
    
    except requests.RequestException:
        return None
    
    try:
        # serialize the response and return as function output
        api_response = response.json()
        return {
            "symbol" : api_response["Symbol"],
            "name" : api_response["Name"],
            "sector" : api_response["Sector"],
            "industry" : api_response["Industry"],
            "marketcap" : api_response["MarketCapitalization"],
            "peratio" : api_response["PERatio"],
            "bookvalue" : api_response["BookValue"],
            "divpershare" : api_response["DividendPerShare"],
            "divyield" : api_response["DividendYield"],
            "divdate" : api_response["DividendDate"],
            "exdivdate" :api_response["ExDividendDate"],
            "beta" : float(api_response["Beta"]),
            "52wkhigh" : api_response["52WeekHigh"],
            "52wklow" : api_response["52WeekLow"],
            "exchange" : api_response["Exchange"],
 #           "payoutratio" : api_response["PayoutRatio"]
        }
    except (KeyError, TypeError, ValueError):
        return None   

    
def login_required(f):
   
    """ Decorate routes to require login.
        http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/  """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function    
    