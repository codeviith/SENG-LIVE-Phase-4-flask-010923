#!/usr/bin/env python3

# 📚 Review With Students:
    # Request-Response Cycle
    # Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports

import os
from flask import Flask, jsonify, make_response, request, session
from flask_migrate import Migrate
from models import db, Pet, Owner

# 3. ✅ Initialize the App
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' ### this is where the database is configured.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  ### this is for logging any modifications done (would be on normally in production)
app.secret_key = os.envrion.get('SECRET_KEY')

#Initialize database
db.init_app(app) ### this is where the database is initialized


    # Configure the database
    # ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'`
    # ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False` 


# 4. ✅ Migrate
migrate = Migrate()
migrate.init_app(app, db) ### can also be combined to a one liner: migrate = Migrate(app,db)


excluded_endpoints = ['login', 'signup', 'check_session', 'root']

@app.before_request
def check_logged_in():
    if request.endpoint not in excluded_endpoints:
        user_id = session.get('user_id') ### using session.get because we dont want it to crash and just return none instead.
        user = User.query.filter(User.id == user_id).first()

        if not user:
            # invalid cookie
            return {'message': 'Invalid session.'}, 401


# 5. ✅ Navigate to `seed.rb`

### execute python seed.py


# 6. ✅ Routes
@app.route('/')
def root():
    return '<h1>Main Page</h1>'

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new_user = User(username = data['username'])
    new_user.password_hash = data['password']

    db.sessoin.add(new_user)
    db.session.commit()

    return {'message': 'User successfully registered.'}, 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # check if user exists
    user = User.query.filter(User.username == data['username']).first()

    if not user:
        return {'message': 'User not found.'}, 404
    elif user.authenticate(data['password']):
        # password matched, add cookie
        session['user_id'] = user.id # user_id can be named as anything you want
        return {'message': 'Login success'}, 201
    else:
        # password does not match, send error response
        return {'message': 'Login failed'}, 403


@app.route('/check_session') ### this is used for every page that needs to be logged in
def check_session():
    user_id = session.get('user_id') ### using session.get because we dont want it to crash and just return none instead.
    user = User.query.filter(User.id == user_id).first()

    if not user:
        # invalid cookie
        return {'message': 'Invalid session.'}, 401
    
    return {'message': 'Valid session'}, 200


@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id') ### pop is the method called to delete sessoin.
    return {'message': 'Logged out successful.'}, 200


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return make_response(jsonify({"hello": "world"}), 200)


@app.route('/pets', methods=['GET', 'POST'])
def get_all_pets():
    if request.method == 'GET':
        pets = Pet.query.all()
        body = [pet.to_dict() for pet in pets]
    else: # POST
        pet_data = request.get_json() ### 

        # validate
        if 'name' not in pet_data:
            return ({'message': 'A name is required'}, 403)

        new_pet = Pet(
            name=pet_data.get('name'),
            owner_id=pet_data.get('owner_id')
        )

        # add to db
        db.session.add(new_pet)
        db.session.commit()

        return (new_pet.to_dict(), 201)


@app.route('/pets/<int:id>', methods=['GET', 'DELETE', 'PATCH']) ### the pro of using methods is: we can write code to be used globally for all the methods.
def pets_by_id(id):
    # query the db for a pet wth this matching id
    pet = Pet.query.filter(Pet.id == id).first()
    
    if request.method == 'GET':
        if not pet:
            return ({'mesage': 'No pets found.'}, 404)

        # manually write out dict
        # return make_response(jsonify({
        #     "id": pet.id,
        #     "name": pet.name
        # }), 200)

        # send json data to client
        # use to_dict() to return dict
        # inside to_dict(), can use a custom rule to leave out what we don't need or want
        return make_response(jsonify(pet.to_dict(rules=('-owner',))), 200)
    elif request.method == 'DELETE':
        # delete the matching id from db
        db.session.delete(pet)
        db.session.commit()

        return ({}, 200)
    elif request.method == 'PATCH':
        pet_data = request.get_json()

        ### option#1 - tedious for large db
        if 'name' in pet_data:
            pet.name = pet_data['name']
        if 'owner_id' in pet_data:
            pet.owner_id = pet_data['owner_id']
        
        ### option#2 - slightly easier
        for field in pet_data:
            # pet.field = pet_data[field] ### <-- does not work bc python cannot parse it correctly
            setattr(pet, field, pet_data[field])

            # add back to db
            db.session.add(pet)
            db.session.commit()

        return make_response(pet.to_dict(), 200)



@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter(Owner.id == id).one()
    return make_response(jsonify(owner.to_dict()), 200)




# 7. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`

# 8. ✅ Create a dynamic route


# 9.✅ Update the route to find a `production` by its `title` and send it to our browser



# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`

if __name__ == '__main__':
    app.run(port=5555, debug=True)
