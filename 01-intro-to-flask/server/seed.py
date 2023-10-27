#!/usr/bin/env python3

from app import app
from models import db, Pet, Owner

with app.app_context():
    # delete everything from all tables
    Pet.query.delete()
    Owner.query.delete()

    o1 = Owner(name='Joe')
    o2 = Owner(name='Anne')

    db.sesion.add_all([o1, o2]) ### owners will get their ids here

    p1 = Pet(name='Fido', owner=o1)
    p2 = Pet(name='Rex', owner=o1)
    p3 = Pet(name='Fluffy', owner=o2)
    
    db.session.add_all([p1, p2, p3])
    db.session.commit()