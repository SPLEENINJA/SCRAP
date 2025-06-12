import os
from flask import Flask, request, send_file, render_template
from v2projet import run_selenium_scraper

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("front.html") 

@app.route("/launch", methods=["GET"])
def launch():
    args = request.args.to_dict()
    path = run_selenium_scraper(args)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
