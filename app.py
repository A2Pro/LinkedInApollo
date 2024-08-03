from flask import Flask, render_template, session, redirect

app = Flask(__name__)

@app.route("/")
def index():
    if not session["logged_in"] or not session["username"] or not session["id"]:
        return redirect("/login")
    if not session["onboarded"]:
        return redirect("/onboard")
    return render_template("index.html", user)

@app.route('/onboard', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        job_title = request.form.get('job_title')
        company = request.form.get('company')
        industry = request.form.get('industry')
        print(f"Received form data: Name={name}, Email={email}, Phone={phone}, Job Title={job_title}, Company={company}, Industry={industry}")

        return redirect("index.html")

    return render_template('onboard.html')