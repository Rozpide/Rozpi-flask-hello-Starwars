import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite, Vehicle

app = Flask(__name__)
app.url_map.strict_slashes = False

# Configuración de la base de datos
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

# Manejar/serializar errores como un objeto JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar un sitemap con todos los endpoints-------------------------
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#--------*********DIVIDO POR MODELOS PARA IMPLEMENTAR ENDPOINT********
#----------------------------personajes-------------------------------

# Obtener todos los personajes
@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    return jsonify([person.serialize() for person in all_people]), 200

# Obtener un personaje específico por ID---------------------------

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize()), 200
# Crear un nuevo personaje
@app.route('/people', methods=['POST'])
def create_person():
    name = request.json.get('name')
    gender = request.json.get('gender')
    birth_year = request.json.get('birth_year')
    eye_color = request.json.get('eye_color')

    new_person = People(
        name=name,
        gender=gender,
        birth_year=birth_year,
        eye_color=eye_color
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.serialize()), 201

# Actualizar un personaje específico por ID
@app.route('/people/<int:people_id>', methods=['PUT'])
def update_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404

    name = request.json.get('name')
    gender = request.json.get('gender')
    birth_year = request.json.get('birth_year')
    eye_color = request.json.get('eye_color')

    person.name = name if name else person.name
    person.gender = gender if gender else person.gender
    person.birth_year = birth_year if birth_year else person.birth_year
    person.eye_color = eye_color if eye_color else person.eye_color

    db.session.commit()
    return jsonify(person.serialize()), 200

# Eliminar un personaje específico por ID
@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found"}), 404
    
    db.session.delete(person)
    db.session.commit()
    return jsonify({"msg": "Person deleted"}), 200

#----------------------------planetas-------------------------------

# Obtener todos los planetas
@app.route('/planets', methods=['GET'])
def get_all_planets():
    all_planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in all_planets]), 200

# Obtener un planeta específico por ID--------------------------------

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200
# Crear un nuevo planeta
@app.route('/planets', methods=['POST'])
def create_planet():
    name = request.json.get('name')
    climate = request.json.get('climate')
    terrain = request.json.get('terrain')
    population = request.json.get('population')

    new_planet = Planet(
        name=name,
        climate=climate,
        terrain=terrain,
        population=population
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

# Actualizar un planeta específico por ID
@app.route('/planets/<int:planet_id>', methods=['PUT'])
def update_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    name = request.json.get('name')
    climate = request.json.get('climate')
    terrain = request.json.get('terrain')
    population = request.json.get('population')

    planet.name = name if name else planet.name
    planet.climate = climate if climate else planet.climate
    planet.terrain = terrain if terrain else planet.terrain
    planet.population = population if population else planet.population

    db.session.commit()
    return jsonify(planet.serialize()), 200

# Eliminar un planeta específico por ID
@app.route('/planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404

    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg": "Planet deleted"}), 200
    

#----------------------------usuarios-------------------------------

# Obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    return jsonify([user.serialize() for user in all_users]), 200

# Obtener un usuario específico por ID-------------------

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.serialize()), 200

# Crear un nuevo usuario-----------------------------------

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if not username or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    new_user = User(
        username=username,
        email=email,
        password=password,
        is_active=True  # Suponiendo que el nuevo usuario es activo por defecto
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201


# Actualizar un usuario específico por ID
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

# Eliminar un usuario específico por ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200

#----------------------------vehículos-------------------------------

# Obtener todos los vehículos
@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicle.name.query.all()
    return jsonify([vehicle.serialize() for vehicle in all_vehicles]), 200

# Obtener un vehículo específico por ID
@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"msg": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200

# Crear un nuevo vehículo
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

#----------------------------favoritos-------------------------------

# Obtener todos los favoritos
@app.route('/favorites', methods=['GET'])
def get_all_favorites():
    all_favorites = Favorite.query.all()
    return jsonify([favorite.serialize() for favorite in all_favorites]), 200

# Crear un nuevo favorito
@app.route('/favorites', methods=['POST'])
def create_favorite():
    user_id = request.json.get('user_id')
    vehicle_id = request.json.get('vehicle')
    people_id = request.json.get('people_id')
    planet_id = request.json.get('planet_id')
    username = request.json.get('username')

    new_favorite = Favorite(
        user_id=user_id,
        vehicle_id=vehicle_id,
        people_id=people_id,
        planet_id=planet_id,
        username=username
    )
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

# Obtener los favoritos de un usuario específico-------------------

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

# Añadir un nuevo planeta favorito al usuario actual
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

# Añadir un nuevo personaje favorito al usuario actual
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.json.get('user_id')
    new_favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

# Eliminar un planeta favorito por ID
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

# Eliminar un personaje favorito por ID
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.json.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

# Endpoint de ejemplo
@app.route('/user', methods=['GET'])
def handle_hello():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }
    return jsonify(response_body), 200

# Esto solo se ejecuta si se ejecuta `$ python src/app.py`
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
