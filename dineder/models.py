from datetime import datetime
from dineder import db, login_manager
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_fk = db.relationship('Users', backref='user_id', lazy=True)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dump({'user_id':self.id}).decode('utf-8')

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rest_name = db.Column(db.String(100), nullable=False)
    online_order = db.Column(db.Boolean)
    book_table = db.Column(db.Boolean)
    rate = db.Column(db.Float)
    votes = db.Column(db.Integer, nullable=True)
    rest_location = db.Column(db.String(20), nullable=False)
    cost = db.Column(db.Float)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    def __repr__(self):
        return '<Restaurant %r>' % self.rest_name

class user_restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.relationship('Users', backref='id', lazy=True)
    restaurant_id = db.relationship('Restaurants', backref='id', lazy=True)

    def __repr__(self):
        return '<FAV RESTAURANT for user %r>' % self.user_id

class Cuisines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuisine = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<Restaurant %r>' % self.cuisine

# class cuisines_restaurants(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     cuisine_id = db.relationship('Cuisine', backref='id', lazy=True)
#     restaurant_id = db.relationship('Restaurants', backref='id', lazy=True)
#
#     def __repr__(self):
#         return '<Restaurants and cuisines %r>' % self.restaurant_id


class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuisine = db.Column(db.String(300), nullable=False)
    cuisine_importance = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(300), nullable=False)
    price_importance = db.Column(db.Integer, nullable=False)
    ratings = db.Column(db.String(300), nullable=False)
    ratings_importance = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.String(300), nullable=False)
    distance_importance = db.Column(db.Integer, nullable=False)
    user_id = db.relationship('Users', backref='id', lazy=True)

    def __repr__(self):
        return f"User preferences('{self.cuisine}', '{self.price}', '{self.ratings}', '{self.distance}')"
