from flask import Flask, request, redirect, session
from flask.templating import render_template
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime

app = Flask(__name__)

with open("config.json", "rb") as confile:
    config = json.load(confile)

if config["local_env"] == True:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ledger.db'
    app.config['SECRET_KEY'] = '379db29fe33c2812e94897d01726b771755ce5893472ca6b0c9fe020e3047226a2e3'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ledger class for maintaining records of sales and purchase of jewelery
class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    trade = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.FLOAT, nullable=False)
    rate = db.Column(db.FLOAT, nullable=False)
    totalPrice = db.Column(db.FLOAT, nullable=False)
    dateAdded = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.name} - {self.category} - {self.trade}"

# Class gold for daily incoming and outgoing gold
class Gold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    inOut = db.Column(db.String(15), nullable=False)
    weight = db.Column(db.FLOAT, nullable=False)
    dateAdded = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.jewel_id} - {self.name} - {self.weight}"

# Class cash for daily incoming and outgoing cash
class Cash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    inOut = db.Column(db.String(15), nullable=False)
    price = db.Column(db.FLOAT, nullable=False)
    dateAdded = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.jewel_id} - {self.name} - {self.price}"

# Routing Starts here
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    getResponseDict = json.loads(response.data)
    response.content_type = "application/json"
    return render_template("error.html", response=getResponseDict)

@app.route('/Login', methods=['GET', 'POST'])
def login():
    if 'user' in session and session['user'] in config['User_name']:
        return redirect("/")

    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if username == config['User_name'] and userpass == config['User_pass']:
            # set session variable
            session['user'] = username
            return redirect("/")

        else:
            wrongkw = "*Invalid Input!!"
            return render_template("login.html", wrongkw=wrongkw)
        
    else:
        return render_template("login.html")

@app.route('/Logout')
def Logout():
    if 'user' in session and session['user'] == config['User_name']:
        session.pop('user')
        return redirect("/Login")
    else:
        return redirect("/Login")


@app.route("/", methods=['GET', 'POST'])
def home():
    if 'user' in session and session['user'] == config["User_name"]:
        # Query Data from database
        goldIn = Gold.query.filter_by(inOut = "In").all()
        goldOut = Gold.query.filter_by(inOut = "Out").all()
        cashIn = Cash.query.filter_by(inOut = "In").all()
        cashOut = Cash.query.filter_by(inOut = "Out").all()

        # Data for balance sheet
        DATA = {
            "Gold In": 0,
            "Gold Out": 0,
            "Cash In": 0,
            "Cash Out": 0,
            "Gold Balance": 0,
            "Cash Balance": 0
        }

        # Fill DATA using for loops
        for i in goldIn:
            DATA["Gold In"] += i.weight

        for i in goldOut:
            DATA["Gold Out"] += i.weight

        for i in cashIn:
            DATA["Cash In"] += i.price

        for i in cashOut:
            DATA["Cash Out"] += i.price

        # Show Balance by subtractig items
        DATA["Gold Balance"] = DATA["Gold In"] - DATA["Gold Out"]
        DATA["Cash Balance"] = DATA["Cash In"] - DATA["Cash Out"]

        return render_template(
            "index.html",
            goldIn = goldIn,
            goldOut = goldOut,
            cashIn =cashIn,
            cashOut = cashOut,
            DATA = DATA
        )
    
    else:
        return redirect("/Login")

@app.route("/Gold", methods=['GET', 'POST'])
def addGold():
    if 'user' in session and session['user'] == config["User_name"]:
        if request.method == 'POST':
            # Get data from form
            name = request.form.get("name").title()
            inOut = request.form.get("inOut")
            weight = request.form.get("weight")
            dateAdded = datetime.now().strftime("%d-%m-%y")

            # Add data to database
            gold = Gold(
                name = name,
                inOut = inOut,
                weight = weight,
                dateAdded = dateAdded
            )

            # Add it to db
            db.session.add(gold)
            db.session.commit()

        return redirect("/")
    else:
        return redirect("/Login")

@app.route("/Cash", methods=['GET', 'POST'])
def addCash():
    if 'user' in session and session['user'] == config["User_name"]:
        if request.method == 'POST':
            # Get data from form
            name = request.form.get("name").title()
            inOut = request.form.get("inOut")
            price = request.form.get("cost")
            dateAdded = datetime.now().strftime("%d-%m-%y")

            # Add data to database
            cash = Cash(
                name = name,
                inOut = inOut,
                price = price,
                dateAdded = dateAdded
            )

            # Add it to db
            db.session.add(cash)
            db.session.commit()

        return redirect("/")
    else:
        return redirect("/Login")
        

@app.route("/Ledger", methods=['GET', 'POST'])
def ledger_home():
    if 'user' in session and session['user'] == config["User_name"]:
        if request.method == 'POST':
            name = request.form.get("name").title()
            category = request.form.get("category")

            # Get values according to gold
            if category == "Gold":
                trade = request.form.get("buySellGold")
                subcategory = request.form.get("goldSubCategory").capitalize()
                weight = request.form.get("goldWeight")
                rate = request.form.get("goldRate")

            # Get values according to silver
            elif category == "Silver":
                trade = request.form.get("buySellSilver")
                subcategory = request.form.get("silverSubCategory").capitalize()
                weight = request.form.get("silverWeight")
                rate = request.form.get("silverRate")

            # Get values according to grocerie
            elif category == "Grocery":
                trade = request.form.get("buySellGrocerie")
                subcategory = request.form.get("SubCatGrocerie").capitalize()
                weight = request.form.get("grocQuantity")
                rate = request.form.get("grocRate")

            totalPrice = float(weight)*float(rate)
            dateAdded = datetime.now().strftime("%d-%m-%y")

            ledger = Ledger(
                name = name,
                category = category,
                subcategory = subcategory,
                trade = trade,
                weight = weight,
                rate = rate,
                totalPrice = totalPrice,
                dateAdded = dateAdded
                )
            db.session.add(ledger)
            db.session.commit()

        goldItems = config["goldSubcategory"]
        silverItems = config["silverSubcategory"]

        # From DataBase
        sold = Ledger.query.filter_by(trade="Sold").all()
        bought = Ledger.query.filter_by(trade="Buy").all()
        allTrade = Ledger.query.all()

        return render_template(
            "ledger.html",
            silverItems = silverItems,
            goldItems = goldItems,
            sold = sold,
            bought = bought,
            allTrade = allTrade
        )
    else:
        return redirect("/Login")

@app.route("/Ledger/delete/<int:id>")
def ledger_delete(id):
    if 'user' in session and session['user'] == config["User_name"]:
        delLedger = Ledger.query.filter_by(id=id).first()
        db.session.delete(delLedger)
        db.session.commit()
        return redirect("/Ledger")
    else:
        return redirect("/Login")

@app.route("/Gold/delete/<int:id>")
def delGold(id):
    if 'user' in session and session['user'] == config["User_name"]:
        delGold = Gold.query.filter_by(id=id).first()
        db.session.delete(delGold)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/Login")

@app.route("/Cash/delete/<int:id>")
def delCash(id):
    if 'user' in session and session['user'] == config["User_name"]:
        delCash = Cash.query.filter_by(id=id).first()
        db.session.delete(delCash)
        db.session.commit()
        return redirect("/")
    else:
        return redirect("/Login")

@app.route("/Ledger/update/<int:id>", methods=['GET', 'POST'])
def ledger_update(id):
    if 'user' in session and session['user'] == config["User_name"]:
        if request.method == 'POST':
            name = request.form.get("name").title()
            category = request.form.get("category")

            # Get values according to gold
            if category == "Gold":
                trade = request.form.get("buySellGold")
                subcategory = request.form.get("goldSubCategory").capitalize()
                weight = request.form.get("goldWeight")
                rate = request.form.get("goldRate")

            # Get values according to silver
            elif category == "Silver":
                trade = request.form.get("buySellSilver")
                subcategory = request.form.get("silverSubCategory").capitalize()
                weight = request.form.get("silverWeight")
                rate = request.form.get("silverRate")

            # Get values according to grocerie
            elif category == "Grocery":
                trade = request.form.get("buySellGrocerie")
                subcategory = request.form.get("SubCatGrocerie").capitalize()
                weight = request.form.get("grocQuantity")
                rate = request.form.get("grocRate")

            totalPrice = float(weight)*float(rate)
            # dateAdded = datetime.now().strftime("%d-%m-%y")

            # Get th particular item by id
            ledger = Ledger.query.filter_by(id=id).first()

            # Change according to form
            ledger.name = name
            ledger.category = category
            ledger.subcategory = subcategory
            ledger.trade = trade
            ledger.weight = weight
            ledger.rate = rate
            ledger.totalPrice = totalPrice

            # Change it from database
            db.session.add(ledger)
            db.session.commit()

            # Redirects to home
            return redirect("/Ledger")

        goldItems = config["goldSubcategory"]
        silverItems = config["silverSubcategory"]
        
        # Get element from database and send it to template
        item = Ledger.query.filter_by(id=id).first()
        
        return render_template(
            "update_Ledger.html",
            id = id,
            item = item,
            goldItems = goldItems,
            silverItems = silverItems
        )
    else:
        return redirect("/Login")

@app.route("/Gold/update/<int:id>", methods=['GET', 'POST'])
def gold_update(id):
    if 'user' in session and session['user'] == config["User_name"]:
        inpQuan = "Weight" # For geting data from form dynamically

        if request.method == 'POST':
            # Get data from form
            name = request.form.get("name").title()
            inOut = request.form.get("inOut")
            weight = request.form.get(inpQuan)

            # Query data from form
            upGold = Gold.query.filter_by(id = id).first()

            # Update the data
            upGold.name = name
            upGold.inOut  = inOut
            upGold.weight = weight

            # Commit it to database
            db.session.add(upGold)
            db.session.commit()

            return redirect("/")

        # Send data from database into form
        gold = Gold.query.filter_by(id = id).first()
        inpQuanVal = float(gold.weight) # Convert the weight into float object and send it into form

        return render_template(
            "update_Cash_Gold.html",
            category = "Gold",
            id = id,
            inpQuan = inpQuan,
            inpQuanVal =inpQuanVal,
            item = gold
            )
    else:
        return redirect("/Login")

@app.route("/Cash/update/<int:id>", methods=['GET', 'POST'])
def cash_update(id):
    if 'user' in session and session['user'] == config["User_name"]:
        inpQuan = "Amount" # For geting data from form dynamically

        if request.method == 'POST':
            # Get data from form
            name = request.form.get("name").title()
            inOut = request.form.get("inOut")
            price = request.form.get(inpQuan)

            # Query data from form
            upCash = Gold.query.filter_by(id = id).first()

            # Update the data
            upCash.name = name
            upCash.inOut  = inOut
            upCash.weight = price

            # Commit it to database
            db.session.add(upCash)
            db.session.commit()

            return redirect("/")

        # Send data from database into form
        cash = Cash.query.filter_by(id = id).first()
        inpQuanVal = float(cash.price) # Convert the price into float object and send it into form

        return render_template(
            "update_Cash_Gold.html",
            category = "Cash",
            id = id,
            inpQuan = inpQuan,
            inpQuanVal = inpQuanVal,
            item = cash
            )
    else:
        return redirect("/Login")

# Register Service Worker
@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

if __name__ == '__main__':
    app.run(debug = config["local_env"], port=5000)