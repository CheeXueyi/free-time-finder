from argparse import REMAINDER
from flask import Flask, redirect, url_for, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
import datetime

app = Flask(__name__)
app.secret_key = "major_software_project"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sessions.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    dates = db.relationship("Date", cascade="all, delete-orphan", backref="event")
    people = db.relationship("Person", cascade="all, delete-orphan", backref="event")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))
    busy_dates = db.relationship("Busy_date", cascade="all, delete-orphan", backref="person") 

class Busy_date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date=db.Column(db.Date)
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
    #creates a new "Event" in database using inputted data and shows success page
    if request.method == "POST":
        title = request.form['title']
        new_event = Event(title=title)
        for i in request.form:
            if i[:-1] == "date_range_start":
                start = datetime.datetime.strptime(request.form[i], "%Y-%m-%d").date()
            elif i[:-1] == "date_range_end":
                end = datetime.datetime.strptime(request.form[i], "%Y-%m-%d").date()
                while start != end + datetime.timedelta(days=1):
                    new_date = Date(date=start, event=new_event)
                    db.session.add(new_date)
                    start += datetime.timedelta(days=1)
                db.session.commit()
        return render_template("make_event_status.html", id=new_event.id, status = "Success", title=new_event.title)
    else:
        return render_template("make_event.html")

@app.route("/find_event")
def find_event():
    #directs to event details page according to inputted event_id
    if request.args.get("event_id") != None:
        event_id = request.args.get("event_id")
        event = Event.query.filter_by(id=event_id).first()
        return render_template("event_page.html", event=event, n_people=len(event.people))
    else:
        return render_template("find_event.html")

@app.route("/add_new_participant", methods=["GET", "POST"])
def add_new_participant():
    #creates a new "Person" in an "Event" in data base along with their busy dates
    event_id = request.args.get("event_id")
    query_event = Event.query.filter_by(id=event_id).first()
    if request.method == "POST":
        new_name = request.form["name"]
        new_person = Person(name=new_name, event=query_event)
        db.session.add(new_person)
        for i in request.form:
            if i != "name":
                busy_date = datetime.datetime.strptime(i, "%Y-%m-%d").date()
                new_busy_date = Busy_date(date=busy_date, person=new_person)
                db.session.add(new_busy_date)
        db.session.commit()
        return render_template("add_new_participant_status.html", status="Success", person=new_person)
    else:
        return render_template("add_new_participant.html", event=query_event)

@app.route("/edit_participant", methods=["GET", "POST"])
def edit_participant():
    person_id = request.args.get("person_id")
    query_person = Person.query.filter_by(id=person_id).first()
    query_event = query_person.event
    if request.method == "POST":
        db.session.delete(query_person)
        new_name = request.form["name"]
        new_person = Person(name=new_name, event=query_event)
        db.session.add(new_person)
        for i in request.form:
            if i != "name":
                busy_date = datetime.datetime.strptime(i, "%Y-%m-%d").date()
                new_busy_date = Busy_date(date=busy_date, person=new_person)
                db.session.add(new_busy_date)
        db.session.commit()
        return render_template("edit_participant_status.html", status="Success", person=new_person)
    else:
        person_busy_dates = []
        for i in query_person.busy_dates:
            person_busy_dates.append(i.date)
        return render_template("edit_participant.html", person=query_person, person_busy_dates=person_busy_dates)

@app.route("/delete_person")
def delete_person():
    person_id = request.args["person_id"]
    query_person = Person.query.filter_by(id=person_id).first()
    name = query_person.name
    event = query_person.event
    db.session.delete(query_person)
    db.session.commit()
    return render_template("delete_person_status.html", status="Success", event = event, person_name=name)
    

@app.route("/find_best_dates")
def find_best_date():
    if "id" not in request.args: return "Error <a href='/'>go back to home page</a>"
    event_id = request.args["id"]
    return render_template("find_best_dates.html", event_id=event_id)
    
@app.route("/json")
def json_req():
    if "id" not in request.args: return "Error <a href='/'>go back to home page</a>"
    id=request.args["id"]
    event = Event.query.get(int(id))
    if event != None:
        res = event.as_dict()
        
        #get event dates
        res["dates"] = []
        for i in event.dates:
            res["dates"].append(i.date)
        
        #get event people and their busy dates
        res["people"] = []
        for i in event.people:
            busy_dates = []
            for busy_date in i.busy_dates:
                busy_dates.append(busy_date.date)
            name = i.name
            person = {
                "name":name,
                "busy_dates":busy_dates
            }
            res["people"].append(person)
        
        #return event dict
        res["status"] = 1
        return jsonify(res)
    else:
        return jsonify({"status":0})

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
    query_sess = Event.query.get(id)
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

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    