# DivChaser
Web App for tracking stock dividends

#Project Title: DivChaser

    DivChaser is a dynamic web application that lets you
    track certain financial data about stocks.

#Project goal:
    To help newbie investors educate themselves about the world of dividends and see how
    different companies pay them to their shareholders.

#Technologies:
     - Python 3.7.9
     - SQLite3
     - Java Script
     - Bootstrap v5.0.0
     - HTML and Jinja

#Functionalities:
     - Connectivity to real financial data via API.
     - Allows users to enter and use their own API keys.
     - Dynamically generated content. Generate financial data (mostly data about dividends) for screening
       about companies per users' choice.
     - Ability to save a list of user's favorite stocks and their dividend data in one place.
     - Ability to dynamically modify this list by removing stocks or adding new stocks to it.
     - Authentication. Ability to register and log in different users.
     - Remembers every user's progress via cookies. Every user has their own profile.


#Overview:
    The web application uses API to connect the user to financial data provider.
    After having registered and logged in, users must obtain their own API keys form the data provider and
    enter the key into the webpage to be able to browse freshly generated financial data.

    On a separate screen the user can search for stock tickers. Via the API the company's financial data
    is fetched from the data provider and is populated on the screen.
    Then the user has the option to 'add' this stock and its financial data to his list of favorite stocks
    or move on. User has the ability to modify this list by deleting and adding new stocks to it.


#Example:
    Bob is new to investing and is curious about dividends. He wants to browse some companies and see
    how they pay dividends.
    He registers on DivChaser, then logs in, enters his API key and he is all set to
    browse stocks. Bob searches for company XYZ. Financial data, such as XYZ's dividend yield,
    payout ratio, earnings per share, etc. populates on the screen. Bob decides to add XYZ stock to his
    favorites. Stock's name and dividend data are saved in a list.
    Bob can later log in and see his list of his favorite stocks, that he could modify by
    adding new stocks to it or removing stocks from it.



