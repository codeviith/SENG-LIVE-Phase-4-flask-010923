# 📚 Review With Students:
    # Review models
    # Review MVC
#SQLAlchemy import
from flask_sqlalchemy import SQLAlchemy

# 📚 Review With Students:
    # What SQLAlchemy() is replacing from SQLAlchemy in phase 3
     
db = SQLAlchemy()

class Pet(db.Model):
    __tablename_ = 'pets'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)


    def __repr__(self):
        return f'<Pet {self.name}'





# 1. ✅ Create a Production Model
	# tablename = 'Productions'
	# Columns:
        # title: string, genre: string, budget:float, image:string,director: string, description:string, ongoing:boolean, created_at:date time, updated_at: date time 
# 2. ✅ navigate to app.py
