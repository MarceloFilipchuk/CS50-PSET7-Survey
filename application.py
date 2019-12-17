import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# export API_KEY=pk_48460f9070584002b41b3b81491109c4

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Redirects from the index directly to the form
@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")

# Shows the form
@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")

# Stores the data from the form in a .csv file called survey.csv for later process
@app.route("/form", methods=["POST"])
def post_form():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    lvlofeducation = request.form.get("lvlofeducation")
    gender = request.form.get("gender")
    if not firstname or not lastname or not lvlofeducation or not gender:
        return render_template("error.html", message="You have to fill all the requested forms!")
    else:
        with open("survey.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(((firstname), (lastname), (lvlofeducation), (gender)))
        return redirect("/sheet")

# Creates a table with the data stored in the survey.csv file
@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        data = list(reader)
    return render_template("sheet.html", data=data)
