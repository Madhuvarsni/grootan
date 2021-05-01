from flask import Flask, render_template, request, flash, url_for, redirect
import json
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = '20a167a4cf75c2a6ed44bd5f'


@app.route('/login')
@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["_password"]
        if username == "root" and password == "approot":
            return redirect(url_for("homepage"))
        flash("Invalid Credentials. Try again", "danger")
    return render_template("login.html")


@app.route('/home', methods=["GET", "POST"])
def homepage():
    with open(os.path.dirname(os.path.realpath("api.json")+"\\api.json")) as f:
        data = json.load(f)
    return render_template('home.html', dictionary=data)


@app.route('/profile/<id_no>')
def profile(id_no):
    with open(os.path.dirname(os.path.realpath("api.json")+"\\api.json")) as f:
        data = json.load(f)
    if int(id_no) > len(data):
        return redirect(url_for("profile", id_no=1))
    profile_data = data[int(id_no)-1]
    return render_template("profile.html", dictionary=profile_data)


@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        with open(os.path.dirname(os.path.realpath("api.json")+"\\api.json")) as f:
            data = json.load(f)
        new_user = {
            "id": len(data)+1,
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "age": request.form["age"],
            "dob": request.form["dob"],
            "more": {
                "address_line1": request.form["address_line1"],
                "address_line2": request.form["address_line2"],
                "phone": request.form["phone"],
            },
        }
        data.append(new_user)
        with open(os.path.dirname(os.path.realpath("api.json")+"\\api.json"), 'w') as file:
            file.seek(0)
            file.write(json.dumps(data))
            file.truncate()
        return redirect(url_for("homepage"))
    return render_template("register.html")


if __name__ == "__main__":
    app.run()
