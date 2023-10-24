#!/usr/bin/env python3

# 📚 Review With Students:
    # Request-Response Cycle
    # Web Servers and WSGI/Werkzeug

# 1. ✅ Navigate to `models.py`

# 2. ✅ Set Up Imports
from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from models import db, Production

# 3. ✅ Initialize the App
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' ### this is where the database is configured.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  ### this is for logging any modifications done (would be on normally in production)

#Initialize database
db.init_app(app) ### this is where the database is initialized


    # Configure the database
    # ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'`
    # ['SQLALCHEMY_TRACK_MODIFICATIONS'] = False` 


# 4. ✅ Migrate
migrate = Migrate()
migrate.init_app(app, db) ### can also be combined to a one liner: migrate = Migrate(app,db)


# 5. ✅ Navigate to `seed.rb`

# 6. ✅ Routes
@app.route('/')
def root():
    return '<h1>Main Page</h1>'

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return make_response(jsonify({"hello": "world"}), 200)

@app.route('/books/<int:id>')
def book_by_id(id):
    return make_response(jsonify({"id": id}), 200)

# 7. ✅ Run the server with `flask run` and verify your route in the browser at `http://localhost:5000/`

# 8. ✅ Create a dynamic route



# 9.✅ Update the route to find a `production` by its `title` and send it to our browser
    
   

# Note: If you'd like to run the application as a script instead of using `flask run`, uncomment the line below 
# and run `python app.py`

if __name__ == '__main__':
    app.run(port=5555, debug=True)
