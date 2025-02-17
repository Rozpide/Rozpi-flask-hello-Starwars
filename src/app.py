"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite, Vehicle


app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
#----------------------------people-------------------------------

@app.route('/people', methods=['GET'])# Aqui enviamos una solicitud GET a la ruta /people para obtener todos los personajes
def get_all_people():
    all_people = People.query.all()# Aqui estamos obteniendo todos los personajes de la base de datos
    return jsonify([person.serialize() for person in all_people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])# AQui enviamos una solicitud GET a la ruta /people/<people_id> para obtener un personaje en particular a traves de su ID
def get_person(people_id):
    person = People.query.get(people_id)# Aqui estamos obteniendo un personaje en particular de la base de datos a traves de su ID
    if not person:
        return jsonify({"msg": "Person not found"}), 404 # Si el personaje no existe en la base de datos, se devuelve un mensaje de error
    return jsonify(person.serialize()), 200 # Si el personaje existe en la base de datos, se devuelve el personaje y un codigo de estado 200

#----------------------------planets-------------------------------

@app.route('/planets', methods=['GET'])# A partir de ahora igual que con los personajes, pero con los planetas
def get_all_planets():
    all_planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in all_planets]), 200
# A partir de ahora igual que con los personajes, pero con los planetas
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

#----------------------------users-------------------------------

# Este endpoint nos permite obtener todos los usuarios de la base de datos
@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    return jsonify([user.serialize() for user in all_users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    user.username = username if username else user.username
    user.email = email if email else user.email
    user.password = password if password else user.password

    db.session.commit()
    return jsonify(user.serialize()), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200
#----------------------------vehicles-------------------------------

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicle.query.all()
    return jsonify([vehicle.serialize() for vehicle in all_vehicles]), 200

@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"msg": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200

@app.route('/vehicles', methods=['POST'])
def create_vehicle():
    name = request.json.get('name')
    model = request.json.get('model')
    manufacturer = request.json.get('manufacturer')
    cost_in_credits = request.json.get('cost_in_credits')
    color = request.json.get('color')
    year_of_manufacture = request.json.get('year_of_manufacture')

    new_vehicle = Vehicle(
        name=name,
        model=model,
        manufacturer=manufacturer,
        cost_in_credits=cost_in_credits,
        color=color,
        year_of_manufacture=year_of_manufacture
    )
    db.session.add(new_vehicle)
    db.session.commit()
    return jsonify(new_vehicle.serialize()), 201


#----------------------------favorites-------------------------------
# Este endpoint nos permite agregar un favorito a un usuario
@app.route('/favorites', methods=['GET'])
def get_all_favorites():
    all_favorites = Favorite.query.all()
    return jsonify([favorite.serialize() for favorite in all_favorites]), 200

@app.route('/favorites', methods=['POST'])
def create_favorite():
    user_id = request.json.get('user_id')
    vehicle_id = request.json.get('vehicle_id')
    people_id = request.json.get('people_id')
    planet_id = request.json.get('planet_id')

    new_favorite = Favorite(
        user_id=user_id,
        vehicle_id=vehicle_id,
        people_id=people_id,
        planet_id=planet_id
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200


# Este endpoint nos permite eliminar un favorito a traves de su ID
@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

#-----------------------------------------------------------
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
