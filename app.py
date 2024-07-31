from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import csv
from flask import Flask, render_template, session, redirect, jsonify, request
chrome_options = Options()
h1 = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64"
h2 = "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument(h1 + h2)

chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)



app = Flask(__name__)

@app.route("/")
def index():
    if(session["logged_in"] == False):
        return(redirect("/login"))



@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check if any field is missing
    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    user = collection.find_one({"username": username})
    if not user:
        return jsonify({"status": "nouser"})
    if user["password"] == password:
        response = jsonify({"status": "works"})
        response.set_cookie("username", username)
        return response
    else:
        return jsonify({"status": "wrong"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check if any field is missing
    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    # Check if the username already exists
    if collection.find_one({"username": username}):
        return jsonify({"status": "error", "message": "Username already exists"}), 400

    # Insert the new user into the collection
    collection.insert_one({
        "username": username,
        "password": password,
    })

@app.route("/autofill_linkedin/<url>")
def linkedin_fill(url):
    driver.get(url)
    time.sleep(3)
    with open(f"{url}.html", "w") as f:
       f.write(driver.page_source)
