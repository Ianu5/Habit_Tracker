import os
from datetime import date

from flask import Flask, g, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from helpers import login_required, color_dates
import customcalendar # Customized the calendar module to fit my needs

app  = Flask(__name__)
app.config["SESSION_PERMANENT"] = False 
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
@login_required
def index():
    if request.method == "GET":
        conn = sqlite3.connect("habits.db", check_same_thread=False)
        db = conn.cursor()
        db.execute("SELECT * FROM habits WHERE user_id = ?", (session["user_id"],))
        row = db.fetchall()
        habits = [x[2] for x in row]
        length = (len(habits))
        conn.close()
        return render_template("/index.html", habits=habits, len=length)

@app.route("/add_habit", methods=["GET", "POST"])
@login_required
def add_habit():
    if request.method == "POST":

        if not request.form.get("habit"):
           return redirect("/")
        
        else:
            conn = sqlite3.connect("habits.db", check_same_thread=False)
            db = conn.cursor()
            db.execute("INSERT INTO habits (user_id, habitname) VALUES(?, ?)", (session["user_id"], request.form.get("habit")))
            conn.commit()
            conn.close()

    return redirect("/")

@app.route("/update_habit", methods=["POST"])
@login_required
def update_habit():
    if request.method == "POST":
        conn = sqlite3.connect("habits.db", check_same_thread=False)
        db = conn.cursor()
        today = date.today()
        for x in request.form:
            db.execute("INSERT INTO tracking (user_id, habitname, date) VALUES(?, ?, ?)", (session["user_id"], x, today))
        conn.commit()
        conn.close()
        return redirect("/")
    

@app.route("/delete_habit", methods=["GET", "POST"])
@login_required
def delete_habit():
    if request.method == "POST":
        conn = sqlite3.connect("habits.db", check_same_thread=False)
        db = conn.cursor()
        db.execute("DELETE FROM habits WHERE habitname = ? AND user_id = ?", (request.form.get("habit"), session["user_id"]))
        conn.commit()
        conn.close()
    return redirect("/")


@app.route("/habit_history", methods=["POST"])
@login_required
def habit_history():
    if request.method == "POST":
        year = int(request.form.get("year"))
        habit = request.form.get("habit")
        calendar = []
        cal = customcalendar.HTMLCalendar()

        conn = sqlite3.connect("habits.db", check_same_thread=False)
        db = conn.cursor()
        db.execute("SELECT SUBSTR(date, INSTR(date, ?)) FROM tracking WHERE user_id == ? AND habitname == ?", (year, session["user_id"], habit))
        rows = db.fetchall()
        
        for i in range(1, 13):
            month = cal.formatmonth(year, i)
            month = color_dates(month, rows, i)
            calendar.append(month)

    return render_template("/history.html", calendar=''.join(calendar))
        

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("login.html", error="where's your username?")

        elif not request.form.get("password"):
            return render_template("login.html", error2="where's your password?")

        conn = sqlite3.connect("habits.db", check_same_thread=False)
        db = conn.cursor()
        db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        row = db.fetchall()

        if len(row) != 1:
            conn.close()
            return render_template("login.html", error="no user with that username found")

        elif not check_password_hash(row[0][2], request.form.get("password")):
            conn.close()
            return render_template("login.html", error2="the password is wrong")

        else:
            session["user_id"] = row[0][0]
            conn.close()
            return redirect("/")

    return render_template("/login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("/register.html", error_username="must provide username")

        conn = sqlite3.connect("habits.db", check_same_thread=False)
        db = conn.cursor()
        db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        row = db.fetchall()

        if not request.form.get("password"):
            return render_template("register.html", error_password="must provide password")
        elif not request.form.get("confirmation"):
            return render_template("register.html", error_password="must confirm password")
        elif len(row) == 1:
            return render_template("register.html", error_username="username already taken")
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error_password="confirmation does not match password")

        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=3)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (request.form.get("username"), hash))
        conn.commit()
        conn.close()
        return render_template("/login.html")
    else:
        return render_template("/register.html")
    

@app.route("/logout")
def logout():
    # clear user from session and redirect to login page
    if not session:
        return redirect("/")
    else:
        session.clear()
        return redirect("/")
