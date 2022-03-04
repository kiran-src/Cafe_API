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

def check_bool(bool):
    if bool.lower() == 'true':
        return True
    elif bool.lower() == 'false':
        return False
    else:
        return None

cafes = db.session.query(Cafe).all()

@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record

@app.route('/all')
def all():
    cafes_dict = []
    for i in cafes:
        cafes_dict.append(i.to_dict())
    return jsonify(cafes=cafes_dict)

@app.route('/random', methods=['GET'])
def random():
    cafe_random = choice(cafes)

    # Return a dictionary
    # cafe_dict = {
    #     'id': cafe_random.id,
    #     'name': cafe_random.name,
    #     'map_url': cafe_random.map_url,
    #     'img_url': cafe_random.img_url,
    #     'location': cafe_random.location,
    #     'seats': cafe_random.seats,
    #     'has_toilet': cafe_random.has_toilet,
    #     'has_wifi': cafe_random.has_wifi,
    #     'has_sockets': cafe_random.has_sockets,
    #     'can_take_calls': cafe_random.can_take_calls,
    #     'coffee_price': cafe_random.coffee_price
    # }
    # return f"{cafe_dict}"

    # Retun a JSON using Jsonify
    return jsonify(cafe=cafe_random.to_dict())

@app.route('/search', methods=['GET'])
def search():
    search_cafes = []
    query = request.args.get("query")
    result = request.args.get("result")
    print("A")
    check = True
    for i in cafes[0].__table__.columns:
        if i.name == query:
            check = False
    if check:
        return jsonify(error=f"Database does not have a dataset named {query} ")
    for i in cafes:
        if f"{getattr(i, query)}".lower() == f"{result}".lower():
            search_cafes.append(i.to_dict())
    if search_cafes == []:
        return jsonify(error=f"Database does not have an entry named {result} ")
    else:
        return jsonify(cafe=search_cafes)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get("name")
    map_url = request.form.get("map_url")
    img_url = request.form.get("img_url")
    location = request.form.get("location")
    seats = request.form.get("seats")
    has_toilet = check_bool(request.form.get("has_toilet"))
    has_wifi = check_bool(request.form.get("has_wifi"))
    has_sockets = check_bool(request.form.get("has_sockets"))
    can_take_calls = check_bool(request.form.get("can_take_calls"))
    coffee_price = request.form.get("coffee_price")
    to_add = Cafe(
        name=name,
        map_url=map_url,
        img_url=img_url,
        location=location,
        seats=seats,
        has_toilet=has_toilet,
        has_wifi=has_wifi,
        has_sockets=has_sockets,
        can_take_calls=can_take_calls,
        coffee_price=coffee_price
    )
    db.session.add(to_add)
    db.session.commit()
    success = {'success': "Successfully added to the cafe"}
    return jsonify(response=success)

@app.route('/update-price/<cafe_id>', methods=['PATCH'])
def price_change(cafe_id):
    c_price = request.form.get("coffee_price")
    cof = Cafe.query.filter_by(id=cafe_id).first()
    # print(cof.coffee_price)
    cof.coffee_price = c_price
    # Cafe.query.filter_by(id=cafe_id).first().coffee_price = c_price
    db.session.commit()
    # print(cof.coffee_price)
    success = {'success': "Successfully updated the cafe"}
    return jsonify(response=success)

if __name__ == '__main__':
    app.run(debug=True)
