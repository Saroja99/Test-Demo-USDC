import cv2
import numpy as np
import base64
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config.config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from models.models import db, Demo, DemoScore
from forms.form import RegistrationForm, LoginForm

app = Flask(__name__)

# Flask-Mail Configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "anushree.deshapande1999@gmail.com"  # Change this
app.config["MAIL_PASSWORD"] = "xyfc mdwo xlwu ynpp"  # Change this
app.config["MAIL_DEFAULT_SENDER"] = "saroja.deshapande99@gmail.com"

# Initialize Flask-Mail
mail = Mail(app)

# Flask Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = SECRET_KEY

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

# Function to send an alert email
def send_alert_email(email):
    msg = Message("Exam Violation Alert", recipients=[email])
    msg.body = "An unauthorized object (mobile/electronic device) was detected during your exam session. Please adhere to the exam rules."
    
    try:
        mail.send(msg)
        print("Email alert sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

@app.route("/", methods=["GET", "POST"])
def index():
    register_form = RegistrationForm()
    login_form = LoginForm()

    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        
        new_user = Demo(
            first_name=register_form.first_name.data,
            last_name=register_form.last_name.data,
            email=register_form.email.data,
            phone=register_form.phone.data,
            dob=register_form.dob.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration completed!", "success")
        return redirect(url_for("index"))

    if login_form.validate_on_submit():
        user = Demo.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            session["user_id"] = user.id
            flash("Successfully logged in!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Credentials!", "danger")

    return render_template("login_register.html", register_form=register_form, login_form=login_form)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for("index"))
    return render_template("dashboard.html")

@app.route("/exam", methods=["GET", "POST"])
def exam():
    if "user_id" not in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        score = request.form.get("score", 0, type=int)
        new_score = DemoScore(user_id=session["user_id"], score=score)
        db.session.add(new_score)
        db.session.commit()
        return redirect(url_for("thank_you"))

    return render_template("exam.html")

@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")

@app.route("/view_score", methods=["GET", "POST"])
def view_score():
    if "user_id" not in session:
        return redirect(url_for("index"))

    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = Demo.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            session["user_id"] = user.id
            score = DemoScore.query.filter_by(user_id=user.id).first()
            if score:
                return render_template("scores.html", score=score.score, name=user.first_name + " " + user.last_name, email=user.email)
            else:
                flash("No score found!", "warning")
                return redirect(url_for("view_score"))
        else:
            flash("Invalid Credentials!", "danger")

    return render_template("login_for_score.html", login_form=login_form)

if __name__ == "__main__":
    app.run(debug=True)
