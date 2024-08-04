from flask import Flask, render_template, session, redirect, request, url_for, flash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from functools import wraps
import random

load_dotenv()

uri = os.getenv("MONGO_URI_STRING")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Accounts"]
userinfo = db["Users"]
logindb = db["Login"]
app = Flask(__name__)

app.secret_key= "3405gorfejiu84tgfnje2i30rf9joed23rifu90ehoirj49getb8fvu7yd8h3ut4oig9tebifv8dwc7ey80h3ut4og5itu9b0evfdc"
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in") or not session.get("username"):
            flash("You need to be logged in to access this page.")
            return redirect(url_for("login"))
        user = logindb.find_one({"username": session.get("username")})
        if not user:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def onboard_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = logindb.find_one({"username": session.get("username")})
        if not user:
            return redirect(url_for("login"))
        if user["onboarded"] == "false":
            return redirect(url_for("onboard"))
        return f(*args, **kwargs)
    return decorated_function

def gen_random_id():
    rand_id = random.randint(1, 10000)
    if userinfo.find_one({"id": rand_id}):
        return gen_random_id()
    return rand_id

@app.route("/")
@login_required
@onboard_required
def index():
    if not session.get("onboarded"):
        return redirect(url_for("onboard"))
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            user = logindb.users.find_one({"username": username})
            if not user:
                logindb.insert_one({
                    "username": username,
                    "password": password,
                    "onboarded": "false"
                })
                return redirect(url_for("login"))
            else:
                return(render_template("error.html"))
        except Exception as e:
            print(e)
            return render_template("error.html")
    return render_template("signup.html", error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            user = logindb.find_one({"username": username})
            if not user:
                return render_template("login.html", error="User not found.")
            if user["password"] == password:
                session["logged_in"] = True
                session["username"] = username
                session["onboarded"] = user.get("onboarded", False)
                return redirect(url_for("index"))
            else:
                return render_template("login.html", error="Wrong username or password.")
        except:
            return render_template("error.html")
    return render_template("login.html", error=None)

@app.route('/onboard', methods=['GET', 'POST'])
@login_required
def onboard():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            job_title = request.form.get('job_title')
            company = request.form.get('company')
            industry = request.form.get('industry')
            rand = gen_random_id()
            userinfo.insert_one({
                "username": session["username"],
                "name": name,
                "email": email,
                "phone": phone,
                "job_title": job_title,
                "company": company,
                "industry": industry,
                "id": rand,
            })
            session["onboarded"] = True
            return redirect(url_for("index"))
        except:
            return render_template("error.html")
    return render_template('onboard.html')

@app.route("/search/<criteria>/<entry>")
@login_required
@onboard_required
def search(critera, entry):
    users = logindb.find({critera: entry})
    return users

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3945, debug = True)
