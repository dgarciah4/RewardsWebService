import os
import requests
import sqlite3
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from datetime import datetime


####### * Initialization of the database and its location

basedir = os.path.abspath(os.path.dirname(__file__))

## Initialization of FLASK environment
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
## Ensures multiple threads are being used instead of a single thread
conn = sqlite3.connect('data.sqlite',check_same_thread=False)

print ("****Opened database successfully****")
print ("****Accounting Views****")

cursor = conn.cursor()

## Display data tables on points for accounting purposes
## Pritns in terminal the transaction table properly sorted by timestamp
def transactionData():
    print('\nData in user table (Transactions):')
    data=cursor.execute('''SELECT * FROM user''')
    timeSorting = "SELECT * FROM user ORDER BY timestamp"
    cursor.execute(timeSorting)
    conn.commit()
    for row in data:
        print(row)
transactionData()

## Displays Total Points in a Seperate Table
def totalPoints():
    print('\nData in amounts table (Total Points):')
    data=cursor.execute('''SELECT * FROM amounts''')
    for row in data:
        print(row)
totalPoints()

## Prints out total balances by payer
def balance():
    print("\nBalance Sorted by Payer:")
    data = cursor.execute('''SELECT payer,
                            SUM(points) AS points
                            FROM user
                            GROUP BY payer''')
    for row in data:
        print(row)
balance()


##########################################################################################
## Class models for setup and reference purposes

# Class Model of the user table containing the data for each payer transaction
class User(db.Model):
    __tablename__="user"

    timestamp   = db.Column(db.Text, primary_key=True)
    points      = db.Column(db.Integer)
    payer       = db.Column(db.Text)

    def __init__(self,timestamp,points,payer):
        self.timestamp   = timestamp
        self.points      = points
        self.payer       = payer

# Simple Model used to setup the amounts table containing the total amount of points
class Point(db.Model):
    __tablename__="amounts"

    id      = db.Column(db.Integer, primary_key=True)
    points  = db.Column(db.Integer)

    def __init__(self,id,points):
        self.id     = id
        self.points = points
###########################################################################################


# Query fetching the sum of points for all payers in user table
def fetch_sumPoints():
    cursor.execute('''SELECT SUM(points) FROM user''')
    fetch = cursor.fetchall()[0][0]
    return fetch

# Query fetching the sum of points in the amounts table
def fetch_sumPoints2():
    cursor.execute('''SELECT SUM(points) FROM amounts''')
    fetch = cursor.fetchall()[0][0]
    return fetch

# Simple query used to create a sample table
def create_tables():
    cursor.execute('''INSERT INTO amounts(id, points)
                    VALUES(1, 1700)''')
    conn.commit()
#create_tables()

# Query Command that assists in resetting the total amount of points
# before any amounts were spent
def resetPoints():
    fetching = fetch_sumPoints()
    strFetching = str(fetching)
    setPoints = " UPDATE amounts SET points = " + strFetching + " WHERE id = 1"
    cursor.execute(setPoints)
    conn.commit()


#############################################################################################
######## PAGE ROUTES AND REDIRECTS ############

## route for home page
@app.route('/')
def home():
    return render_template('home.html')

## route to points page that displays the table of all transactions from payer
@app.route('/points', methods= ['POST', 'GET'])
def points():
    all_points = User.query.all()
    return render_template('points.html',all_points = all_points)
cursor.execute("SELECT * FROM user ORDER BY timestamp")

## route to payout page allowing to create payers and setup amounts to payout in points in a form
## redirects to points page afterwards to add to transactions list
@app.route('/payout',methods= ['POST','GET'])
def payout():
    # retrieves info from each user input and appropiately adds to database
    if request.method == 'POST':
        data        = request.form
        timestamp   = data["timestamp"]
        points      = data["points"]
        payer       = data["payer"]
        new_data    = User(timestamp, points, payer)
        db.session.add(new_data)
        db.session.commit()                 ## commits changes to database
        all_points = User.query.all()       
        return render_template('points.html', all_points=all_points)

    return render_template('payout.html')


## Page focused on Spending Points
## User is able to see their current amount of points they have
## Amounts spent is appropiatly to the accounts table
## Amount spent is also equally chosen from oldest payer transaction
@app.route('/spend', methods= ['POST','GET'])
def spend():
    fetching2 = fetch_sumPoints2()
    balance()
    transactionData()
    totalPoints()
    total = fetching2
    totalAmount = total
    if request.method == 'POST':
        data        = request.form
        spent       = data["points"]
        if spent == '':
            return render_template('spend.html', totalAmount=totalAmount)
        totalAmount = totalAmount - int(spent)
        strTA = str(totalAmount)
        # Updates amounts table with the new amount after spending
        amountsUpdate = "UPDATE amounts SET points = " + strTA + " WHERE id = 1"
        if totalAmount < 0:
            totalAmount = 0
            print("Total amount of Points:" + str(totalAmount))
            return render_template('spend.html', totalAmount=totalAmount)
        
        cursor.execute(amountsUpdate)
    conn.commit()
    print("Total amount of Points:" + str(totalAmount))
    return render_template('spend.html', totalAmount = totalAmount)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
