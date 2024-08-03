from flask import Flask, render_template, session, redirect, request
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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in") or not session.get("username") or not session.get("id"):
            flash("You need to be logged in to access this page.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def gen_random_id():
    random = random.randint(1, 10,000)
    if(random in userinfo):
        gen_random_id()
    return random

@app.route("/")
@login_required
def index():
    if not session["onboarded"]:
        return redirect("/onboard")
    return render_template("index.html", user)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            if username in login:
                return render_template("signup.html", error = "Username taken.")
            else:
                logindb.insert_one({
                    "username" : username,
                    "password" : password
                })
                return redirect("/login")
        except:
            return("error.html")
    else:
        return render_template("signup.html", error = None)

@app.route("/login", methods = ['GET', 'POST'])
def login():

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form.get("username")
            password = request.form.get("password")
            if logindb[username] == password:
                session["logged_in"] = True
                session["username"] = username
            else:
                return render_template("login.html", error = "Wrong password / Username.")
        except:
            return("error.html")
    else:
        return render_template("login.html", error = None)


@app.route('/onboard', methods=['GET', 'POST'])
@login_required
def onboard():
    if()
    if request.method == 'POST':
      try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        job_title = request.form.get('job_title')
        company = request.form.get('company')
        industry = request.form.get('industry')
        password = request.form.get('password')
        rand = gen_random_id()
        userinfo.insert_one({
            "username" : session["username"]
            "name" : name,
            "email": email,
            "phone" : phone,
            "job_title" : job_title,
            "company" : company,
            "industry" : industry,
            "id" : rand,
            "password" : password
        })

        return redirect("index.html")
      except:
        return("error.html")
    return render_template('onboard.html')

app.run(host = '0.0.0.0', port = 3945)