from flask import Flask, request, redirect, url_for, render_template,jsonify

from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("name")  
        password = request.form.get("password")

        if not username or not password:
            return "Username and password required"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/getlist")
def users():
    all_users = User.query.all()
 
    users_list = []
    for u in all_users:
        users_list.append({
            "id": u.id,
            "username": u.username,
            "password": u.password  
        })
    
    return jsonify(users_list)

if __name__ == "__main__":
    app.run(debug=True, port=5777)
