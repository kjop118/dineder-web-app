import math
from flask import render_template, url_for, flash, redirect, request, jsonify
from dineder import app, db, bcrypt
from dineder.forms import RegistrationForm, LoginForm
from dineder.models import Users, Restaurants, Cuisines, CuisinesRestaurants, UserRestaurant, Preferences
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
from geopy.distance import geodesic

from sqlalchemy import select

#def getMatchedRestaurants(user_location, weights, ):


@app.route("/")
@app.route("/home")
def home():
    # posts = Post.query.all();
    return render_template('home.html')

@app.route("/about")
def about():
    # posts = Post.query.all();
    return render_template('about.html', title="ABOUT")


@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(name=form.name.data, surname=form.surname.data, email=form.email.data, password=hashed_password)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        # flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/favourite", methods=['GET', 'POST'])
@login_required
def getFavRestaurant():
    return render_template('fav-restaurant.html', title='LIKE')

@app.route("/match-restaurant", methods=['GET', 'POST'])
def getYourMatch():
    #to chyba będzie trzeba przenieść do innego routa bo póki co odpala się po odświeżeniu 
    #strony na zakładce /match-restaurant, a nie po przycisku MATCH
    cuisines = Cuisines.query.all()

    #lista tych restauracji do algorytmu ma trafić? 

    
    #na podstawie cuisine id szukam restauracji które pasują pod to kryterium
#    restaurantsWithSpecificCuisine = CuisinesRestaurants.query.filter_by(cuisine_id=cuisine_id).all()
#   print(restaurantsWithSpecificCuisine)

    # print(cuisineInRestaurants)
    # list = Cuisines.query.filter_by(cuisine = 'Pizza').all()

    # restaurants_db = Restaurants.query.all()
    # restaurants_all = []
    #
    # for restaurant in restaurants_db:
    #     restaurants_all.append({'id': restaurant.id, 'name': restaurant.rest_name, 'online_order': restaurant.online_order,
    #                         'book_table': restaurant.book_table, 'rating': restaurant.rate, 'votes': restaurant.votes,
    #                         'price_range': restaurant.cost, 'rest_location': restaurant.rest_location,
    #                         'location': (restaurant.latitude, restaurant.longitude)})
    #
    # for restaurant in restaurants_all:
    #     print(restaurant['name'])

    if request.method == 'POST' and 'match' in request.form:
        wybrane_opcje = request.form.getlist('wybrane_opcje')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        results = latitude
        print(latitude)
        print(longitude)
        return jsonify(results=results)


    return render_template('match.html', title='MATCH', cuisines = cuisines)


def calculate_rating_score(rating, user_rating):
       if rating > user_rating:
            return 0.9
       elif rating == user_rating:
            return 0.8
       else:
            return 0.3

def calculate_cuisine_score(cuisine, user_cuisne):
    if cuisine == user_cuisne:
        return 0.9
    else:
        return 0.5

def calculate_price_range_score(price_range, user_price_range):
    # Implement your own logic to calculate the price range score
    # This is just a placeholder example
    if price_range < user_price_range:
        return 0.9
    elif price_range == user_price_range:
        return 0.8
    else:
        return 0.4

def calculate_location_score(rest_longitude, rest_latitude, user_longitude, user_latitude, allowed_distance):
    # Implement your own logic to calculate the location score
    # This is just a placeholder example
    distance = calculate_distance(rest_longitude, rest_latitude, user_longitude, user_latitude)

    # Normalize the distance value to a score between 0 and 1
    max_distance = allowed_distance  # Maximum distance considered acceptable
    normalized_distance = 1.0 - (distance / max_distance)
    return normalized_distance

def calculate_distance(lon1, lat1, lon2, lat2):
    # Implement your own distance calculation logic
    # This is just a placeholder example using the Haversine formula
    # to calculate the distance between two latitude-longitude points
    earth_radius = 6371  # Radius of the Earth in kilometers

    lon1_rad = math.radians(lon1)
    lat1_rad = math.radians(lat1)
    lon2_rad = math.radians(lon2)
    lat2_rad = math.radians(lat2)

    delta_lon = lon2_rad - lon1_rad
    delta_lat = lat2_rad - lat1_rad

    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = earth_radius * c
    return distance

@app.route("/process_match", methods=['POST'])
def process_match():
    restaurants = Restaurants.query.all()

    data = request.get_json()
    #print(data)
    user_location_lat = float(data['user_location_lat']) 
    user_location_long = float(data['user_location_long'])
    cuisine = data['cuisine']
    cuisine_w = int(data['cuisene_w'])
    rating = float(data['rating'])
    rating_w = int(data['rating_w'])
    price = ""
    if (data['price'] == 'powyżej'):
        price = 10000000
    else:
        price = float(data['price'])
        price = price*10
    price_w = int(data['price_w'])
    allowed_distance = ""
    if (data['allowed_distance'] == 'powyżej'):
        allowed_distance = 10000000
    else:
        allowed_distance = float(data['allowed_distance'])
    
    allowed_distance_w = int(data['allowed_distance_w'])

    weighted_scores = []
    for restaurant in restaurants:
        score = (
            cuisine_w * calculate_cuisine_score(restaurant.cuisine, cuisine) +
            price_w * calculate_price_range_score(restaurant.cost, price) +
            rating_w * calculate_rating_score(restaurant.rate, rating) +
            allowed_distance_w* calculate_location_score(restaurant.longitude, restaurant.latitude, user_location_long, user_location_lat, allowed_distance)
        )
        weighted_scores.append((restaurant, score))
    
    sorted_restaurants = sorted(weighted_scores, key=lambda x: x[1], reverse=True)

    top_restaurants = sorted_restaurants[:10]

    output = []
    for restaurant, score in top_restaurants:
        output.append(f"Restaurant: {restaurant.rest_name}, Score: {score}")

    for i in output:
        print(i)

    if len(output) == 0:
        print("Nie ma dopasowań")

    return '\n'.join(output)
