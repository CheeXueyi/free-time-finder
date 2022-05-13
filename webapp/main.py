from argparse import REMAINDER
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

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

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

#everything under functions start here

@app.route("/functions", methods=["GET"])
def functions():
    return render_template("functions.html")

@app.route("/make_event", methods = ["GET", "POST"])
def make_event():
    if request.method == "POST":
        #take details of event to make new event code here
        title=request.form['title']
        host=request.form['host']
        for i in request.form:
            print(i, request.form[i], type(request.form[i]))
        return "good"
    else:
        return render_template("make_event.html")

#tutorial starts here

@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")

#about us starts here

@app.route("/about")
def about():
    return render_template("about.html")


#--------------------------------------------------------------
#------------------------TESTING-------------------------------
#--------------------------------------------------------------
@app.route("/add_session", methods=["GET", "POST"])
def add_session():
    if request.method == "POST":
        title = request.form["title"]
        host = request.form["host"]
        test = request.form["test"]
        print(test)
        '''
        new_session = Sessions(title=title, host=host)
        db.session.add(new_session)
        db.session.commit()
        id = new_session.id
        return render_template("add_session_success.html", id=id)
        '''
    else:
        return render_template("add_session.html")

@app.route("/add_session_status/<id>")
def add_session_status(id):
    query_sess = Sessions.query.get(id)
    if query_sess != None:
        query_sess = query_sess.as_dict()
        title = query_sess["title"]
        return render_template("add_session_status.html", id=id, status="success", title=title)
    else:
        return "id not found"

@app.route("/add_person", methods=["GET", "POST"])
def add_person():    
    #code to add new person
    return "coming soon" 

@app.route("/find_session")
def find_session():
    #find and show session free times
    return render_template("timequery.html")

@app.route("/json/<id>")
def json_req(id):
    query_sess = Sessions.query.get(int(id))
    if query_sess != None:
        query_sess = query_sess.as_dict()
        query_sess["status"] = 1
        return jsonify(query_sess)
    else:
        return jsonify({"status":0})

@app.route("/timequery")
def timequery():
    return render_template("timequery.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    