from flask import Flask, redirect, url_for, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Password1!@localhost/flask'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route("/admin")
def admin():
    return redirect(url_for("home"))   

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("register.html")
    
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                return redirect(url_for("home"))
            else:
                return "Password is incorrect"
        else:
            return "User not found"
    else:
        return render_template("login.html")

@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        product = Product(name=name, price=price, description=description)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("home"))
    else: 
        products = Product.query.all()
        return render_template("index.html", products=products)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)