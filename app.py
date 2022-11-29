from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
from script.register import *
from script.predict import *
from script.login import *
app = Flask(__name__) 
app.secret_key = 'jbibuibubaskcnakvccwefre'


client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.qfakayr.mongodb.net/?retryWrites=true&w=majority")
db = client.test
db = client.get_database('total_records')
records = db.register

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predict")
def p():
    return predict()

@app.route('/login/', methods=['GET', 'POST'])
def l():
    return login(records)

@app.route('/register', methods=['GET', 'POST'])
def r():
    return register(records)
    
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("home.html")
    else:
        return render_template('home.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")



if __name__ == "__main__":
    app.run(debug=True)
