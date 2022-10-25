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
from models import db, User, Favourite, People, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/user', methods=['POST'])
def creating_user():

    request_body = request.get_json(force=True)
    request_keys = list(request_body.keys())

    if len(request_keys)==0:
        return "The request body is null", 400
    elif 'email' not in request_keys or request_body['email']=="":
        return 'You need to specify the email', 400
    elif 'password' not in request_keys or request_body['password']=="":
        return 'You need to specify the password', 400
    elif User.query.filter_by(email = request_body['email']).first() != None:
        return 'This email is already in use',500
    else:
        email = request_body['email']
        password = request_body['password']
        is_active = request_body['is_active']

        new_user = User(email, password, is_active)
        db.session.add(new_user)
        db.session.commit()
        return 'User added', 200



@app.route('/user', methods=['GET'])
def returning_users():

    all_users = User.query.all()

    if len(all_users) == 0:
        return jsonify({"msg":"No users registered yet"}),500
    else:
        all_users = list(map(lambda x: x.serialize(), all_users))
        json_text = jsonify(all_users)
        return json_text



@app.route('/people', methods=['POST'])
def make_people():

    name_request = request.json.get("name", None)
    height_request = request.json.get("height", None)
    mass_request = request.json.get("mass", None)
    skin_color_request = request.json.get("skin_color", None)
    gender_request = request.json.get("gender", None)
    birth_year_request = request.json.get("birth_year", None)
    eye_color_request = request.json.get("eye_color", None)

    new_character = People(
        name = name_request,
        height = height_request,
        mass = mass_request,
        skin_color = skin_color_request,
        gender = gender_request,
        birth_year = birth_year_request,
        eye_color = eye_color_request
    )

    db.session.add(new_character)
    db.session.commit()

    return 'character added', 200



@app.route('/people/<int:id>', methods=['PUT'])
def update_people(id):
    
    request_body_character = request.get_json()
    character = People.query.get(id)
    if character is None:
        return 'character not found', 404

    if "name" in request_body_character:
        character.name =  request_body_character["name"]
    if "height" in request_body_character:
        character.height =  request_body_character["height"]
    if "mass" in request_body_character:
        character.mass =  request_body_character["mass"]
    if "skin_color" in request_body_character:
        character.skin_color =  request_body_character["skin_color"]
    if "gender" in request_body_character:
        character.gender =  request_body_character["gender"]
    if "birth_year" in request_body_character:
        character.birth_year =  request_body_character["birth_year"]
    if "eye_color" in request_body_character:
        character.eye_color =  request_body_character["eye_color"]
    db.session.commit()

    return 'character updated', 200



@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people(id):
    
    character_to_delete= People.query.get(id)

    if character_to_delete is None:
        return 'character not found', 404
    db.session.delete(character_to_delete)
    db.session.commit()
    
    return 'character deleted', 200



@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    json_text = jsonify(all_people)
    return json_text



@app.route('/people/<int:id>', methods=['GET'])
def get_character(id):

    get_body_character= People.query.get(id)

    return jsonify({'char': [get_body_character.serialize()]}), 200
    


@app.route('/planet', methods=['POST'])
def create_planet():

    name_request = request.json.get("name", None)
    climate_request = request.json.get("climate", None)
    population_request = request.json.get("population", None)
    orbital_period_request = request.json.get("orbital_period", None)
    rotation_period_request = request.json.get("rotation_period", None)
    diameter_request = request.json.get("diameter", None)

    new_planet = Planet(
        name = name_request,
        climate = climate_request,
        population = population_request,
        orbital_period = orbital_period_request,
        rotation_period = rotation_period_request,
        diameter = diameter_request
    )

    db.session.add(new_planet)
    db.session.commit()

    return 'planet added', 200



@app.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):
    request_body_planet = request.get_json()
    planet = Planet.query.get(id)
    if planet is None:
        return 'Planet not found', 404

    if "name" in request_body_planet:
        planet.name =  request_body_planet["name"]
    if "climate" in request_body_planet:
        planet.climate =  request_body_planet["climate"]
    if "population" in request_body_planet:
        planet.population =  request_body_planet["population"]
    if "orbital_period" in request_body_planet:
        planet.orbital_period =  request_body_planet["orbital_period"]
    if "rotation_period" in request_body_planet:
        planet.rotation_period =  request_body_planet["rotation_period"]
    if "diameter" in request_body_planet:
        planet.diameter =  request_body_planet["diameter"]

    db.session.commit()

    return 'planet updated', 200



@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet_to_delete= Planet.query.get(id)

    if planet_to_delete is None:
        return 'planet not found', 404
    db.session.delete(planet_to_delete)
    db.session.commit()
    
    return 'planet deleted', 200



@app.route('/planet', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    json_text = jsonify(all_planets)
    return json_text, 200



@app.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    get_body_planet= Planet.query.get(id)

    return jsonify({'planet': [get_body_planet.serialize()]}), 200



@app.route('/favourites', methods=['GET'])
def get_fav():
    active_user = User.query.filter_by(is_active=True).first()
    try:
        if active_user == None:
            raise Exception()
    except Exception:
        return jsonify({"msg":"No user is active"}),500
    else:
        fav = Favourite.query.filter_by(user_id=active_user.id)
        fav = list(map(lambda x: x.serialize(), fav))

        return jsonify(fav),200



@app.route('/favourite/planet/<int:planet_id>', methods=['POST'])
def add_favourite_planet(planet_id):
    
    active_user = User.query.filter_by(is_active=True).first()
    check_fav = Favourite.query.filter_by(user_id=active_user.id, planet_id=planet_id).first()

    try:
        check_planet = Planet.query.get(planet_id)
        if check_planet == None:
            raise ValueError()
    except ValueError:
        return jsonify({"msg":"The planet doesnt exist in the database"}),400

    try:
        new_favourite_planet = Favourite(user_id=active_user.id, planet_id=planet_id)
        if check_fav != None:
            raise Exception()
    except Exception:
        return jsonify({"msg":"The user already has this planet as favourite"}),500
    else:
        db.session.add(new_favourite_planet)
        db.session.commit()
        return jsonify(new_favourite_planet.serialize()),200



@app.route('/favourite/people/<int:character_id>', methods=['POST'])
def add_favourite_character(character_id):

    active_user = User.query.filter_by(is_active=True).first()
    checkFav = Favourite.query.filter_by(user_id=active_user.id, character_id=character_id).first()
    try:
        checkChar = People.query.get(character_id)
        if checkChar == None:
            raise ValueError()
    except ValueError:
        return jsonify({"msg":"The character doesnt exist in the database"}),400

    try:
        new_favourite_character = Favourite(user_id=active_user.id, character_id=character_id)
        if checkFav != None:
            raise Exception()
    except Exception:
        return jsonify({"msg":"The user already has this character as favourite"}),500
    else:
        db.session.add(new_favourite_character)
        db.session.commit()
        return jsonify(new_favourite_character.serialize()),200



@app.route('/favourite/planet/<int:planet_id>', methods = ['DELETE'])
def delete_favourite_planet(planet_id):
    active_user = User.query.filter_by(is_active=True).first()
    try:
        checkPlanet = Planet.query.get(planet_id)
        if checkPlanet == None:
            raise ValueError()
    except ValueError:
        return jsonify({"msg":"The planet doesnt exist in the database"}),400
    try:
        user_fav_planet = Favourite.query.filter_by(user_id=active_user.id, planet_id=planet_id).first()
        if user_fav_planet == None:
            raise Exception()
    except Exception:
        return jsonify({"msg":"This user doesnt have this planet as favourite"}),500
    else:
        db.session.delete(user_fav_planet)
        db.session.commit()
        return jsonify(user_fav_planet.serialize()),200



@app.route('/favourite/people/<int:character_id>', methods = ['DELETE'])
def delete_favourite_character(character_id):
    active_user = User.query.filter_by(is_active=True).first()
    try:
        checkChar = People.query.get(character_id)
        if checkChar == None:
            raise ValueError()
    except ValueError:
        return jsonify({"msg":"The character doesnt exist in the database"}),400

    try:
        user_fav_character = Favourite.query.filter_by(user_id=active_user.id, character_id=character_id).first()
        if user_fav_character == None:
            raise Exception()
    except Exception:
        return jsonify({"msg":"This user doesnt have this character as favourite"}),500
    else:
        db.session.delete(user_fav_character)
        db.session.commit()
        return jsonify(user_fav_character.serialize()),200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
