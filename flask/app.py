from flask import Flask, render_template, request
import json

app = Flask(__name__)
filename = "ldap.json"
dataform = []

@app.route('/', methods=["GET", "POST"])
def render():
    if request.method == "POST":
        identifiant = request.form.get("identifiant")
        prenom = request.form.get("prenom")
        password = request.form.get("password")
        email = request.form.get("email")
        organisation = request.form.get("organisation")
        if request.form.get("connectFtp"):
            connectFtp = "connectFtp"
        if request.form.get("sendFileFtp"):
            sendFileFtp = "sendFileFtp"
        if request.form.get("sendMail"):
            sendMail = "sendMail"
        if request.form.get("readMail"):
            readMail = "readMail"

        with open(filename, 'r') as f:
            dataform = json.load(f)

        dataform.append({
            "identifiant": identifiant,
            "prenom": prenom,
            "password": passwordn,
            "email": email,
            "organisation": organisation,
            "connectFtp": connectFtp,
            "sendFileFtp": sendFileFtp,
            "sendMail": sendMail,
            "readMail": readMail
        })


        with open(filename, 'w') as f:
            json.dump(dataform, f, indent = 4, separators=(",",": "))
        print(dataform)


    return render_template("index.html")
