# 📚 Review With Students:
    # Review models
    # Review MVC
#SQLAlchemy import
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

# 📚 Review With Students:
    # What SQLAlchemy() is replacing from SQLAlchemy in phase 3

db = SQLAlchemy()
bcrypt = Bcrypt()


class Pet(db.Model, SerializerMixin):
    __tablename_ = 'pets_table'

    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True) ## the parentheses after the db.Integer/db.String is optional if you want to pass in arguments, i.e. length, etc.
    name = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners_table.id'))

    owner = db.relationship('Owner', back_populates='pet')

    @validateS('name')
    def validate_name(self, key, new_name):
        if len(new_name) == 0:
            raise ValueError('name must be at least one character!')
        return new_name # this values is what gets set as the new name


    def __repr__(self):
        return f'<Pet {self.name}'


class Owner(db.Model, SerializerMixin):
    __tablename__ = 'owners_table'

    serialize_rules = ()

    id = db.Column(db.Ineger, primary_key=True)
    name = db.Column(db.String, nullable=False)

    pet = db.relationship('Pet', back_populates='owner', cascade='all, delete-orphan')


    def __repr__(self):
        return f'<Owner {self.name}'




class User(db.Model, SerializerMixin):
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String)

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @passowrd_hash.setter
    def password_hash(self, new_pwd):
        pwd_hash = bcrypt.generate_password_hash(new_pwd.encode('utf-8'))  ### utf-8 is a global encoding table. By default python language is always encoded in utf-8.
        self._password_hash = pwd_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash,
            password.encode('utf-8')
        )






# 1. ✅ Create a Production Model
	# tablename = 'Productions'
	# Columns:
        # title: string, genre: string, budget:float, image:string,director: string, description:string, ongoing:boolean, created_at:date time, updated_at: date time 
# 2. ✅ navigate to app.py
