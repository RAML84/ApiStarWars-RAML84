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
from models import db, User, People, Planets, Favorites
import json
#from models import Person

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
@app.route('/')
def sitemap():
    return generate_sitemap(app)

   #-----------------METODOS GET---------------# 

    ## GET USER
@app.route('/user', methods=['GET'])
def getUser():
    user = User.query.all()
    result = [element.serialize() for element in user]
    return jsonify(result), 200

   ## GET PEOPLE
@app.route('/people', methods=['GET'])
def getPeople():
    people = People.query.all()
    result = [element.serialize() for element in people]
    return jsonify(result), 200

  ## GET PLANETS
@app.route('/planet', methods=['GET'])
def getPlanets():
    planets = Planets.query.all()
    result = [element.serialize() for element in planets]
    return jsonify(result), 200

  ## GET FAVORITES
@app.route('/favorite', methods=['GET'])
def getFavorites():
    favorites = Favorites.query.all()
    result = [element.serialize() for element in favorites]
    return jsonify(result), 200

#-----------------METODOS GET POR ID---------------# 

                   ### GET USER ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    user = User.query.get(user_id)
    result = user.serialize()
    return jsonify(result), 200

### GET PEOPLE ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    people = People.query.get(people_id)
    result = people.serialize()
    return jsonify(result), 200

### GET PLANETS ID
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planets.query.get(planet_id)
    result = planet.serialize()
    return jsonify(result), 200

### GET FAVORITES ID
@app.route('/favorite/<int:favorite_id>', methods=['GET'])
def get_favorite_id(favorite_id):
    favorite = Favorites.query.get(favorite_id)
    result = favorite.serialize()
    return jsonify(result), 200

#-----------------METODOS POST---------------# 

### POST USER
@app.route('/users', methods= ['POST'])
def createUser():
    data= request.data
    data = json.loads(data)
    newUser = User(id = data["id"], name = data["name"], email = data["email"], password = data["password"], is_active = data["is_active"])
    db.session.add(newUser)
    db.session.commit()

    return jsonify(newUser.serialize())

### POST PEOPLE
@app.route('/people', methods= ['POST'])
def createPeople():
    data= request.data
    data = json.loads(data)
    people = People(id = data["id"], name = data["name"], description= data["description"], gender = data["gender"], height = data["height"])
    db.session.add(people)
    db.session.commit()

    return jsonify(people.serialize())

### POST PLANETS
@app.route('/planet', methods= ['POST'])
def createPlanet():
    data= request.data
    data = json.loads(data)
    planet = Planets(id = data["id"], name = data["name"], diameter= data["diameter"], description = data["description"] )
    db.session.add(planet)
    db.session.commit()

    return jsonify(planet.serialize())

#-----------------METODOS DELETE---------------# 

### DELETE PEOPLE
@app.route('/people/<int:people_id>', methods= ['DELETE'])
def deletePeople(people_id):
    people = People.query.get(people_id)
    db.session.delete(people)
    db.session.commit()

    response_body = {"msg": "DELETE"}
    return jsonify(people.serialize())


### DELETE PLANET
@app.route('/planet/<int:planet_id>', methods= ['DELETE'])
def deletePlanet(planet_id):
    planet = Planets.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()

    response_body = {"msg": "DELETE"}
    return jsonify(planet.serialize())

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
