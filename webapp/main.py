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

@app.route("/add_session", methods=["GET", "POST"])
def add_session():
    if request.method == "POST":
        title = request.form["title"]
        host = request.form["host"]
        new_session = Sessions(title=title, host=host)
        db.session.add(new_session)
        db.session.commit()
        id = new_session.id
        return redirect(url_for("add_session_status", id=id))
    else:
        return render_template("add_session.html")

@app.route("/add_session_status/<id>")
def add_session_status(id):
    query_sess = Sessions.query.get(id)
    if query_sess != None:
        return jsonify(query_sess.as_dict())
    else:
        return "id not found"

@app.route("/add_person", methods=["GET", "POST"])
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
    db.create_all()
    app.run(debug=True)