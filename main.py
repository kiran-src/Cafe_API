from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice
app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dict = {}
        for i in self.__table__.columns:
            dict[i.name] = getattr(self, i.name)
        return dict

cafes = db.session.query(Cafe).all()

@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record

@app.route('/random', methods=['GET'])
def random():
    cafe_random = choice(cafes)

    # Return a dictionary
    cafe_dict = {
        'id': cafe_random.id,
        'name': cafe_random.name,
        'map_url': cafe_random.map_url,
        'img_url': cafe_random.img_url,
        'location': cafe_random.location,
        'seats': cafe_random.seats,
        'has_toilet': cafe_random.has_toilet,
        'has_wifi': cafe_random.has_wifi,
        'has_sockets': cafe_random.has_sockets,
        'can_take_calls': cafe_random.can_take_calls,
        'coffee_price': cafe_random.coffee_price
    }
    # return f"{cafe_dict}"

    # Retun a JSON using Jsonify
    return jsonify(cafe=cafe_random.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
