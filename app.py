from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime

app = Flask(__name__)

with open("config.json", "rb") as confile:
    config = json.load(confile)

if config["local_env"] == True:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ledger.db'
    app.config['SECURITY_KEY'] = '379db29fe33c2812e94897d01726b771755ce5893472ca6b0c9fe020e3047226a2e3'
elif config["loacl_env"] == False:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI")
    app.config['SECURITY_KEY'] = os.environ.get("SECURITY_KEY")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Ledger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    trade = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    totalPrice = db.Column(db.Integer, nullable=False)
    dateAdded = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.name} - {self.category} - {self.trade}"


@app.route("/", methods=['GET', 'POST'])
def home():
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
        dateAdded = datetime.now().strftime("%d-%m-%y, %I:%M:%S %p")

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
        "index.html",
        silverItems = silverItems,
        goldItems = goldItems,
        sold = sold,
        bought = bought,
        allTrade = allTrade
    )

@app.route("/delete/<int:id>")
def delete(id):
    delLedger = Ledger.query.filter_by(id=id).first()
    db.session.delete(delLedger)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
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
        dateAdded = datetime.now().strftime("%d-%m-%y, %I:%M:%S %p")

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
        return redirect("/")

    goldItems = config["goldSubcategory"]
    silverItems = config["silverSubcategory"]
    
    # Get element from database and send it to template
    item = Ledger.query.filter_by(id=id).first()
    print(item.category)
    
    return render_template(
        "update.html",
        id = id,
        item = item,
        goldItems = goldItems,
        silverItems = silverItems
    )

if __name__ == '__main__':
    app.run(debug = config["local_env"], port=5000)