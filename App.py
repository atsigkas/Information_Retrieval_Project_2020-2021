from flask import Flask, request, render_template
import Main

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def flask_Main():
    if (request.method == "GET"):
        return render_template("index.html")
    if (request.method == "POST"):
        inputCrawl = request.form['q'] + " 10 0 2"
        pages = Main.flask_main(inputCrawl.split())
        return render_template("index.html", results=list(pages))