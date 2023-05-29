from datetime import datetime
from dineder import db, login_manager
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    restaurant = db.relationship('UserRestaurant', backref='user-fav-rest', lazy=True)
    preferences = db.relationship('Preferences', backref='user-filters', lazy=True)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dump({'user_id':self.id}).decode('utf-8')

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


class Restaurants(db.Model):
    __tablename__ = 'restaurants'
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
    user = db.relationship('UserRestaurant', backref='fav-rest', lazy=True)
    cuisine = db.relationship('CuisinesRestaurants', backref='restaurant-cuisine', lazy=True)

    def __repr__(self):
        return '<Restaurant %r>' % self.rest_name


class UserRestaurant(db.Model):
    __tablename__ = 'user_restaurant'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    def __repr__(self):
        return '<FAV RESTAURANT for user %r>' % self.user_id


class Cuisines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cuisine = db.Column(db.String(300), nullable=False)
    restaurant = db.relationship('CuisinesRestaurants', backref='restaurant-with-cuisine', lazy=True)

    def __repr__(self):
        return '<Cuisine %r>' % self.cuisine


class CuisinesRestaurants(db.Model):
    __tablename__ = 'cuisine_restaurant'
    id = db.Column(db.Integer, primary_key=True)
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisines.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    def __repr__(self):
        return '<Restaurants and cuisines %r>' % self.restaurant_id


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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"User preferences('{self.cuisine}', '{self.price}', '{self.ratings}', '{self.distance}')"


class MatchedRestaurants(db.Model):
    __tablename__ = 'matched_restaurants'
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
    cuisines = db.Column(db.String(200), nullable=False)
    distance = db.Column(db.Float)

    def __repr__(self):
        return '<Matched Restaurant %r>' % self.rest_name


class TempMatchTable(db.Model):
    __tablename__ = 'temp_match_table'
    id = db.Column(db.Integer, primary_key=True)
    cuisine = db.Column(db.String(300), nullable=False)
    cuisine_weight = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(300), nullable=False)
    price_weight = db.Column(db.Integer, nullable=False)
    ratings = db.Column(db.String(300), nullable=False)
    ratings_weight = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.String(300), nullable=False)
    distance_weight = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Temp Matched Choice%r>' % self.cuisine
