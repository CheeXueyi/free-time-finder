from flask import Flask, redirect, url_for, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "MajorSoftwareProject"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/timefinder/", methods=['GET', 'POST'])
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