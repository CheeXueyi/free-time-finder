from flask import Flask, redirect, url_for, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
app.secret_key = "major_software_project"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sessions.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    host = db.Column(db.String(50))
    dates = db.relationship("Date", cascade="all, delete-orphan", backref="session")
    people = db.relationship("Person", cascade="all, delete-orphan", backref="session")

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"))

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"))
    busy_times = db.relationship("Busy_time", cascade="all, delete-orphan", backref="person") 

class Busy_time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_session")
def add_session():
    #code to add new session
    return 0

@app.route("/add_person")
def add_person():    
    #code to add new person
    return 0 

@app.route("/find_session")
def find_session():
    #find and show session free times
    return 0 

@app.route("/timefinder/", methods=["GET", "POST"])
def timefinder():
    if request.method == "POST":
        link = request.form["link"]
        session["link"] = link
        
        #search for link
        return redirect(url_for("link"))
        
    else:
        return render_template("timefinder.html")

@app.route("/link")
def link():
    if "link" in session:
        link = session["link"]
        return render_template("time_display.html", link = link)
    else:
        return redirect(url_for("timefinder"))

@app.route("/json/<ses_id>")
def json(ses_id):
    #search session in database using ses_id
    print(ses_id)
    dict = {"greetings":"hi"}
    print(dict)
    json = jsonify(dict)
    return json

if __name__ == "__main__":
    app.run(debug=True)