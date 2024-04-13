from flask import Flask, redirect, url_for, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Password1!@localhost/flask'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)

@app.route("/data")
def data():
    users = User.query.all()
    return jsonify([{'name': user.name, 'price': user.price, 'description': user.description} for user in users])

@app.route("/admin")
def admin():
    return redirect(url_for("home"))   

@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        user = User(name=name, price=price, description=description)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("data"))
    else: 
        return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)