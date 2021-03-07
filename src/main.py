"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planet, Vehicle, Favorites_Characters, Favorites_Planets, Favorites_Vehicles
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)






# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# EndPoints de usuarios

@app.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    all_users = list(map(lambda user: user.serialize2(),all_users))
    return jsonify(all_users), 200

@app.route('/user', methods=['POST'])
def create_user():
    email = request.json.get('email')
    password = request.json.get('password')
    is_active = request.json.get('is_active')
    first_name = request.json.get('first_name')
    second_name = request.json.get('second_name')
  
    if not email:
        return jsonify({"msg": "El email no puede estar vacio"})

    new_user = User()
    new_user.email = email
    new_user.password = password
    new_user.is_active = is_active
    new_user.first_name = first_name
    new_user.second_name = second_name

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Usuario creado exitosamente"}), 201

# EndPoints de personajes

@app.route('/people', methods=['GET'])
def get_all_people():
    all_characters = Characters.query.all()
    all_characters = list(map(lambda char: char.serialize2(),all_characters))
    return jsonify(all_characters)

@app.route('/people/<int:uid>', methods=['GET'])
def get_char(uid):
    char = Characters.query.filter_by(uid=uid).first()
    if not char:
        return jsonify({"msg":"Char no encontrado"})
    char = char.serialize()
    return jsonify(char)

@app.route('/people', methods=['POST'])
def create_char():
    name = request.json.get('name')
    height = request.json.get('height')
    mass = request.json.get('mass')
    hair_color = request.json.get('hair_color')
    skin_color = request.json.get('skin_color')
    eye_color = request.json.get('eye_color')
    birth_year = request.json.get('birth_year')
    gender = request.json.get('gender')
    homeworld = request.json.get('homeworld')

    if not name:
        return jsonify({"msg": "El nombre no puede estar vacio"})
    
    new_char = Characters()
    new_char.name = name
    new_char.height = height
    new_char.mass = mass
    new_char.hair_color = hair_color
    new_char.skin_color = skin_color
    new_char.eye_color = eye_color
    new_char.birth_year = birth_year
    new_char.gender = gender
    new_char.homeworld = homeworld

    db.session.add(new_char)
    db.session.commit()

    return jsonify({"msg": "Character creado exitosamente"}), 201

# EndPoints de planetas

@app.route('/planet', methods=['GET'])
def get_all_planet():
    all_planet = Planet.query.all()
    all_planet = list(map(lambda pla: pla.serialize2(),all_planet))  
    return jsonify(all_planet)

@app.route('/planet/<int:uid>', methods=['GET'])
def get_planet(uid):
    pla = Planet.query.filter_by(uid=uid).first()
    if not pla:
        return jsonify({"msg":"Planeta no encontrado"})
    pla = pla.serialize()
    return jsonify(pla)

@app.route('/planet', methods=['POST'])
def create_planet():
    name = request.json.get('name')
    diameter = request.json.get('diameter')
    rotation_period = request.json.get('rotation_period')
    orbital_period = request.json.get('orbital_period')
    gravity = request.json.get('gravity')
    population = request.json.get('population')
    climate = request.json.get('climate')
    terrain = request.json.get('terrain')
    surface_water = request.json.get('surface_water')
    created = request.json.get('created')
    edited = request.json.get('edited')

    if not name:
        return jsonify({"msg": "El nombre no puede estar vacio"})
    
    new_planet = Planet()
    new_planet.name = name
    new_planet.diameter = diameter
    new_planet.rotation_period = rotation_period
    new_planet.orbital_period = orbital_period
    new_planet.gravity = gravity
    new_planet.population = population
    new_planet.climate = climate
    new_planet.terrain = terrain
    new_planet.surface_water = surface_water

    db.session.add(new_planet)
    db.session.commit()

    return jsonify({"msg": "Planeta creado exitosamente"}), 201

# EndPoints de vehiculos

@app.route('/vehicle', methods=['GET'])
def get_all_vehicle():
    all_vehicle = Vehicle.query.all()
    all_vehicle = list(map(lambda vehicle: vehicle.serialize2(),all_vehicle))  
    return jsonify(all_vehicle)

@app.route('/vehicle/<int:uid>', methods=['GET'])
def get_vehicle(uid):
    vehicle = Vehicle.query.filter_by(uid=uid).first()
    if not vehicle:
        return jsonify({"msg":"Vehiculo no encontrado"})
    vehicle = vehicle.serialize()
    return jsonify(vehicle)

@app.route('/vehicle', methods=['POST'])
def create_vehicle():
    name = request.json.get('name')
    model = request.json.get('model')
    starship_class = request.json.get('starship_class')
    manufacturer = request.json.get('manufacturer')
    cost_in_credits = request.json.get('cost_in_credits')
    length = request.json.get('length')
    crew = request.json.get('crew')
    passengers = request.json.get('passengers')
    max_atmosphering_speed = request.json.get('max_atmosphering_speed')
    hyperdrive_rating = request.json.get('hyperdrive_rating')
    mglt = request.json.get('mglt')
    cargo_capacity = request.json.get('cargo_capacity')
    consumables = request.json.get('consumables')
    pilots = request.json.get('pilots')
    created = request.json.get('created')
    edited = request.json.get('edited')

    if not name:
        return jsonify({"msg": "El nombre no puede estar vacio"})
    
    new_vehicle = Vehicle()
    new_vehicle.name = name
    new_vehicle.model = model
    new_vehicle.starship_class = starship_class
    new_vehicle.manufacturer = manufacturer
    new_vehicle.cost_in_credits = cost_in_credits
    new_vehicle.length = length
    new_vehicle.crew = crew
    new_vehicle.passengers = passengers
    new_vehicle.max_atmosphering_speed = max_atmosphering_speed
    new_vehicle.hyperdrive_rating = hyperdrive_rating
    new_vehicle.mglt = mglt
    new_vehicle.cargo_capacity = cargo_capacity
    new_vehicle.consumables = consumables
    new_vehicle.pilots = pilots

    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify({"msg": "Vehiculo creado exitosamente"}), 201

# EndPoints de favoritos

@app.route('/user/<int:user_uid>/favorite', methods=['GET'])
def get_user_favorite(user_uid):
    user = User.query.get(user_uid)
    if not user:
        return jsonify({"msg:":"Usuario no encontrado"})
    user = user.serialize()
    return jsonify(user)

@app.route('/user/<int:user_id>/favorite', methods=['POST'])
def all_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': "No existe un usuario con ese ID"})
    character_uidreq = request.json.get('character_uid')
    planet_uid = request.json.get('planet_uid')
    vehicle_uid = request.json.get('vehicle_uid')

    if not character_uidreq and not planet_uid and not vehicle_uid:
        return jsonify({'msg': "Debes de especificar un ID de un personaje, planeta o vehiculo"})
    if character_uidreq:
        character = Characters.query.get(character_uidreq)
        if not character:
            return jsonify({'msg': "El ID del personaje no es valido"})
        new_fav = Favorites_Characters()
        new_fav.user_uid = user_id
        new_fav.character_uidreq = character_uidreq

        db.session.add(new_fav)
        db.session.commit()

    if planet_uid:
        planet = Planet.query.get(planet_uid)
        if not planet:
            return jsonify({'msg': "El ID del planeta no es valido"})
        new_fav = Favorites_Planets()
        new_fav.user_uid = user_id
        new_fav.planet_uid = planet_uid

        db.session.add(new_fav)
        db.session.commit()

    if vehicle_uid:
        vehicle = Vehicle.query.get(vehicle_uid)
        if not vehicle:
            return jsonify({'msg': "El ID del vehiculo no es valido"})
        new_fav = Favorites_Vehicles()
        new_fav.user_uid = user_id
        new_fav.vehicle_uid = vehicle_uid

        db.session.add(new_fav)
        db.session.commit()

    return jsonify({"msg": "Favorito agregado exitosamente"}), 201

#favoritos delete

@app.route('/user/<int:user_uid>/favorite', methods=['DELETE'])
def delete_favorite(user_uid):
    user = User.query.get(user_uid)
    if not user:
        return jsonify({'msg': "No existe un usuario con ese ID"})
    character_uid_req = request.json.get('character_uid')
    planet_uid_req = request.json.get('planet_uid')
    vehicle_uid_req = request.json.get('vehicle_uid')
    
    if not character_uid_req and not planet_uid_req and not vehicle_uid_req:
        return jsonify({'msg': "Debes de especificar un ID de un personaje, planeta o vehiculo"})
    
    if character_uid_req:
        character = Favorites_Characters.query.filter_by(user_uid=user_uid, character_uid=character_uid_req).first()  
        db.session.delete(character)
        db.session.commit()

    if planet_uid_req:
        planet = Favorites_Planets.query.filter_by(user_uid=user_uid, planet_uid=planet_uid_req).first()  
        db.session.delete(planet)
        db.session.commit()

    if vehicle_uid_req:
        vehicle = Favorites_Vehicles.query.filter_by(user_uid=user_uid, vehicle_uid=vehicle_uid_req).first()
        db.session.delete(vehicle)
        db.session.commit()

    return jsonify({"msg": "Favorito eliminado exitosamente"}), 201

#registrar Api

@app.route('/register', methods= ['POST'])
def register():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        is_active = request.json.get("is_active", True) 
        first_name = request.json.get("first_name")
        second_name = request.json.get("second_name")

        if not email:
            return jsonify({"msg":"email es requerido"}), 400
        if not password:
            return jsonify({"msg":"password es requerido"}), 400

        user = User.query.filter_by(email=email).first()
        if user: 
            return jsonify({"msg":"Ya esta registrado"}), 400

        user = User()
        user.email = email
        hashed_password = generate_password_hash(password)
        user.password = hashed_password
        user.is_active = is_active
        user.first_name = first_name
        user.second_name = second_name

        db.session.add(user)
        db.session.commit()

        return jsonify({"success": "Thaks, your register was successfully", "status": "true"}), 200


#LOG IN
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        if not email:
            return jsonify({"Mensaje": "El email es requerido"}), 400
        if not password:
            return jsonify({"Mensaje": "La contraseña es requerida"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"Mensaje": "El email es incorrecto"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({"Mensaje": "La constraseña es incorrecta"}), 401

        # crear el token
        expiracion = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.email, expires_delta=expiracion)

        data = {
            "user": user.serialize(),
            "token": access_token,
            "expires": expiracion.total_seconds()*1000
        }

        return jsonify(data), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)