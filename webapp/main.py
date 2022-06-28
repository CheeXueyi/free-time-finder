from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.exceptions import HTTPException



#-----------------------------------------------------#
#----------Web app configuration starts here----------#
#-----------------------------------------------------#
app = Flask(__name__)
app.secret_key = "major_software_project"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#---------------------------------------------------#
#----------Web app configuration ends here----------#
#---------------------------------------------------#



#----------------------------------------------#
#----------Database models start here----------#
#----------------------------------------------#
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
#--------------------------------------------#
#----------Database models end here----------#
#--------------------------------------------#



#---------------------------------------#
#----------Routing starts here----------#
#---------------------------------------#
#home page
@app.route("/") 
def home():
    return render_template("index.html")


#-----functions start-----#
#main functions page
@app.route("/functions", methods=["GET"]) 
def functions():
    return render_template("functions.html")


#make new event page
@app.route("/make_event", methods = ["GET", "POST"]) 
def make_event():
    #when web form is submitted, creates event according to form details
    if request.method == "POST": 
        title = request.form['title']
        new_event = Event(title=title)
        
        #adds all dates starting from starting date to ending date to event in database
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
    
    #when make new event page is accessed, show make event page
    else: 
        return render_template("make_event.html")


#find event page
@app.route("/find_event")
def find_event():
    #if event_id query was set in address, show event page
    if request.args.get("event_id") != None: 
        event_id = request.args.get("event_id")
        event = Event.query.filter_by(id=event_id).first()
        return render_template("event_page.html", event=event, n_people=len(event.people))

    #if event_id query was not set in address, show find event page
    else: 
        return render_template("find_event.html")


#add new participant page
@app.route("/add_new_participant", methods=["GET", "POST"])
def add_new_participant():
    event_id = request.args.get("event_id")
    query_event = Event.query.filter_by(id=event_id).first()

    #when webform is submitted, create new participant according to form details
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
    
    #when webform is not submitted, shows add new participant page 
    else: 
        return render_template("add_new_participant.html", event=query_event)


#edit participant page
@app.route("/edit_participant", methods=["GET", "POST"])
def edit_participant():
    person_id = request.args.get("person_id")
    query_person = Person.query.filter_by(id=person_id).first()
    query_event = query_person.event

    #when webform is submitted, delete original participant and create new participant with new details from form 
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
    
    #when webform is not submitted, show edit participant page with participant's details 
    else:
        person_busy_dates = []
        for i in query_person.busy_dates:
            person_busy_dates.append(i.date)
        return render_template("edit_participant.html", person=query_person, person_busy_dates=person_busy_dates)


#delete person activator, deletes specified participant when accessed
@app.route("/delete_person")
def delete_person():
    person_id = request.args["person_id"]
    query_person = Person.query.filter_by(id=person_id).first()
    name = query_person.name
    event = query_person.event
    db.session.delete(query_person)
    db.session.commit()
    return render_template("delete_person_status.html", status="Success", event = event, person_name=name)
    

#find best date page
@app.route("/find_best_dates")
def find_best_date():
    if "id" not in request.args: return "Error <a href='/'>go back to home page</a>"
    event_id = request.args["id"]
    return render_template("find_best_dates.html", event_id=event_id)
    

#JSON request directory, returns event details in JSON format
@app.route("/json")
def json_req():
    if "id" not in request.args: return "Error <a href='/'>go back to home page</a>"
    id=request.args["id"]
    event = Event.query.get(int(id))

    #if event with specified id exists
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

    #if event with specified id does not exist
    else:
        return jsonify({"status":0})
#-----functions end-----#


#tutorial page
@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")


#about us page
@app.route("/about")
def about():
    return render_template("about.html")


#error handling
@app.errorhandler(Exception)
def handle_exception(error):
    # pass through HTTP errors
    if isinstance(error, HTTPException):
        return error

    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html", error=error)


#loading database on first website visit after restarts
@app.before_first_request
def create_tables():
    db.create_all()
#------------------------------------#
#----------Routing end here----------#
#------------------------------------#



#only for testing, app is run in configuration file in webhosting site
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
    