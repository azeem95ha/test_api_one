from flask import Flask, request, jsonify
import random
import json
from flask_sqlalchemy import SQLAlchemy

    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50),nullable=False)
    last_name = db.Column(db.String(50),nullable = False)
    country = db.Column(db.String(100))
    username = db.Column(db.String(100),unique = True)
    password = db.Column(db.String(50))
    mobile = db.Column(db.String(20))
    
    
    def __repr__(self):
        return f"{self.id}{self.first_name},{self.last_name},{self.country},{self.username},{self.password},{self.mobile}"


@app.route("/")
def get_all_users():
    output = []
    data = Users.query.all()
    for item in data:
        user_data = {"id":item.id,"first_name":item.first_name,"last_name":item.last_name,
                     "country":item.country,"mobile":item.mobile,"password":item.password,"username":item.username}
        output.append(user_data)
    return {"users":output}

@app.route("/get-user/<user_id>")
def get_user(user_id):
    data = Users.query.all()
    user_data = []
    for item in data:
        if str(item.id) == user_id:
            user_info = {"id":item.id,"first_name":item.first_name,"last_name":item.last_name,
                     "country":item.country,"mobile":item.mobile,"password":item.password,"username":item.username}
            user_data.append(user_info)
    return {"user":user_data}


@app.route("/create_user", methods=["POST"])
def create_user():
    
    if request.method == "POST":
        user = Users()
        user.first_name = request.json["first_name"]
        user.last_name = request.json["last_name"]
        user.country = request.json["country"]
        db.session.add(user)
        db.session.commit()

    return {"id":user.id}

@app.route("/delete-user/<user_id>",methods=["DELETE"])
def delete_user(user_id):
    data = Users.query.all()
    user = []
    if request.method == "DELETE":
        for item in data:
            if str(item.id) == user_id:
                db.session.delete(item)
                db.session.commit()
    return "Deleted successfully"

if __name__ == "__main__":
    app.run(debug=True)