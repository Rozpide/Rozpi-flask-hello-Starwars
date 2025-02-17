from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(20), nullable=True)
    birth_year = db.Column(db.String(20), nullable=True)
    eye_color = db.Column(db.String(20), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(20), nullable=True)
    terrain = db.Column(db.String(20), nullable=True)
    population = db.Column(db.String(20), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
        }
        
class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    model = db.Column(db.String(120), nullable=False)
    manufacturer = db.Column(db.String(120), nullable=False)
    cost_in_credits = db.Column(db.String(120), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    year_of_manufacture = db.Column(db.String(4), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "color": self.color,
            "year_of_manufacture": self.year_of_manufacture,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)

    user = db.relationship('User', backref='favorites')
    vehicle = db.relationship('Vehicle', backref='favorites')
    people = db.relationship('People', backref='favorites')
    planet = db.relationship('Planet', backref='favorites')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user.username,
            "vehicle_id": self.vehicle_id,
            "vehicle_name": self.vehicle.name if self.vehicle else None,
            "people_id": self.people_id,
            "people_name": self.people.name if self.people else None,
            "planet_id": self.planet_id,
            "planet_name": self.planet.name if self.planet else None,
        }
