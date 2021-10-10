from flask import Flask, redirect, url_for, render_template, request


app = Flask(__name__)
words = open("./test_files/words.txt", "r").read().split()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/timefinder/", methods=['GET', 'POST'])
def timefinder():
    if request.method == "POST":
        link = request.form["link"]
        #search for link
        return redirect(url_for("link", lnk=link))
        
    else:
        return render_template("timefinder.html")

@app.route("/<lnk>")
def link(lnk):
    return render_template("time_display.html", link = lnk)

if __name__ == "__main__":
    app.run(debug=True)