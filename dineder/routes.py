import math
from flask import render_template, url_for, flash, redirect, request, jsonify
from dineder import app, db, bcrypt
from dineder.forms import RegistrationForm, LoginForm
from dineder.models import Users, Restaurants, Cuisines, CuisinesRestaurants, UserRestaurant, Preferences, MatchedRestaurants, TempMatchTable
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
import requests
from geopy.distance import geodesic


@app.route("/")
@app.route("/home")
def home():
    clearMatchChoice()
    clearMatchRestaurants()

    return render_template('home.html')


@app.route("/about")
def about():
    clearMatchChoice()
    clearMatchRestaurants()
    return render_template('about.html', title="ABOUT")


@app.route("/register", methods=['GET', 'POST'])
def register():
    clearMatchChoice()
    clearMatchRestaurants()

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
    clearMatchChoice()
    clearMatchRestaurants()

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
    clearMatchChoice()
    clearMatchRestaurants()

    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    clearMatchChoice()
    clearMatchRestaurants()

    preferences = Preferences.query.all()
    if request.method == 'POST':
        preference_id = request.form.get('preference_id')
        preference = Preferences.query.get_or_404(preference_id)

        # decyzja na podjecia na podstawie przycisku albo usuwam albo generuje
        cuisine = preference.cuisine
        price = preference.price
        ratings = preference.ratings
        distance = preference.distance
        cuisine_weight = preference.cuisine_importance
        price_weight = preference.price_importance
        ratings_weight = preference.ratings_importance
        distance_weight = preference.distance_importance

        accountButtonType = request.form.get('accountButtonType')
        if accountButtonType == 'deleteFilter':
            print(cuisine)
            print(price)
            print(ratings)
            print(distance)
            print(cuisine_weight)
            print(price_weight)
            print(ratings_weight)
            print(distance_weight)

            db.session.delete(preference)
            db.session.commit()
            return redirect(url_for('account'))

        elif accountButtonType == "getLocation":
            matchChoice = TempMatchTable(cuisine=cuisine, cuisine_weight=cuisine_weight, price=price,
                                         price_weight=price_weight, ratings=ratings, ratings_weight=ratings_weight,
                                         distance=distance, distance_weight=distance_weight)
            db.session.add(matchChoice)
            db.session.commit()
            return redirect(url_for('match'))

    return render_template('account.html', title='Account', preferences=preferences)


@app.route("/favourite", methods=['GET', 'POST'])
@login_required
def favourite():
    clearMatchChoice()
    clearMatchRestaurants()
    userRestaurants = UserRestaurant.query.filter_by(user_id=current_user.id).all()

    favRestaurants = []
    print(len(userRestaurants))
    if len(userRestaurants) > 0:
        for userRestaurant in userRestaurants:
            favRestaurant = Restaurants.query.filter_by(id=userRestaurant.restaurant_id).first()
            restaurantCuisines = favRestaurant.cuisine
            # print(restaurantCuisines)
            cuisines = []
            for restaurantCuisine in restaurantCuisines:
                cuisine_id = restaurantCuisine.cuisine_id
                cuisines.append(Cuisines.query.get(cuisine_id))

            restaurantCuisine = ""
            for cuisine in cuisines:
                if restaurantCuisine == "":
                    restaurantCuisine = cuisine.cuisine
                else:
                    restaurantCuisine = restaurantCuisine + ", " + cuisine.cuisine

            favRestaurants.append({'restaurant': favRestaurant, 'cuisines': restaurantCuisine})

    if request.method == 'POST':
        favRestaurant_id = request.form.get('favRestaurant_id')
        userRestaurant = UserRestaurant.query.filter_by(id=favRestaurant_id).first()
        db.session.delete(userRestaurant)
        db.session.commit()
        return redirect(url_for('favourite'))

    return render_template('fav-restaurant.html', title='LIKE', favRestaurants=favRestaurants)




# @app.route("/process_match", methods=['POST'])
# def process_match():
#     restaurants = Restaurants.query.all()
#
#     data = request.get_json()
#     #print(data)
#     user_location_lat = float(data['user_location_lat'])
#     user_location_long = float(data['user_location_long'])
#     cuisine = data['cuisine']
#     cuisine_w = int(data['cuisene_w'])
#     rating = float(data['rating'])
#     rating_w = int(data['rating_w'])
#     price = ""
#     if (data['price'] == 'powyżej'):
#         price = 10000000
#     else:
#         price = float(data['price'])
#         price = price*10
#     price_w = int(data['price_w'])
#     allowed_distance = ""
#     if (data['allowed_distance'] == 'powyżej'):
#         allowed_distance = 10000000
#     else:
#         allowed_distance = float(data['allowed_distance'])
#
#     allowed_distance_w = int(data['allowed_distance_w'])
#
#     weighted_scores = []
#     for restaurant in restaurants:
#         score = (
#             cuisine_w * calculate_cuisine_score(restaurant.cuisine, cuisine) +
#             price_w * calculate_price_range_score(restaurant.cost, price) +
#             rating_w * calculate_rating_score(restaurant.rate, rating) +
#             allowed_distance_w* calculate_location_score(restaurant.longitude, restaurant.latitude, user_location_long, user_location_lat, allowed_distance)
#         )
#         weighted_scores.append((restaurant, score))
#
#     sorted_restaurants = sorted(weighted_scores, key=lambda x: x[1], reverse=True)
#
#     top_restaurants = sorted_restaurants[:10]
#
#     output = []
#     for restaurant, score in top_restaurants:
#         output.append(f"Restaurant: {restaurant.rest_name}, Score: {score}")
#
#     for i in output:
#         print(i)
#
#     if len(output) == 0:
#         print("Nie ma dopasowań")
#
#     return '\n'.join(output)


@app.route("/match", methods=['GET', 'POST'])
def match():
    cuisines = Cuisines.query.all()  # pobranie wszystkich dostępnych rodzajów kuchni z bazy do wyświetlenie ich w liście dla użytkownika
    matchedRestaurants = MatchedRestaurants.query.all()
    matchChoice = TempMatchTable.query.first()

    if request.method == 'POST':
        cuisine = request.form.get('cuisine')
        price = float(request.form.get('price'))
        ratings = float(request.form.get('ratings'))
        distance = float(request.form.get('distance'))
        cuisine_weight = int(request.form.get('cuisine_weight'))
        price_weight = int(request.form.get('price_weight'))
        ratings_weight = int(request.form.get('ratings_weight'))
        distance_weight = int(request.form.get('distance_weight'))

        #przypadek do obsluzenia co gdy uzytkonik nie poda rodzaju kuchni
        # if cuisine == "":
        #     print(cuisine)

        #zapis parametrów do tymczasowej tabeli w celu przechowywania wyników
        if matchChoice:
            db.session.delete(matchChoice)
            db.session.commit()

        matchChoice = TempMatchTable(cuisine=cuisine, cuisine_weight=cuisine_weight, price=price, price_weight=price_weight, ratings=ratings, ratings_weight=ratings_weight, distance=distance, distance_weight=distance_weight)
        db.session.add(matchChoice)
        db.session.commit()

        submit_type = request.form.get('submitType')
        print(submit_type)
        if submit_type == 'save':
            preferences = Preferences(cuisine=cuisine, cuisine_importance=cuisine_weight, price=price,
                                      price_importance=price_weight, ratings=ratings, ratings_importance=ratings_weight,
                                      distance=distance, distance_importance=distance_weight, user_id=current_user.id)
            db.session.add(preferences)
            db.session.commit()

        elif submit_type == 'getLocation':
            # pobranie lokalizacji użytkownika
            res = requests.get('https://ipinfo.io/')
            data = res.json()
            location = data['loc'].split(',')
            latitude = float(location[0])
            longitude = float(location[1])

            # print("Latitude : ", latitude)
            # print("Longitude : ", longitude)

            # wyznaczanie wag - które filtry będę uwzględnione jako pierwsze
            restaurants = Restaurants.query.all()
            weighted_scores = []

            for restaurant in restaurants:
                score = (
                    cuisine_weight * calculate_cuisine_score(restaurant.cuisine, cuisine) +
                    price_weight * calculate_price_range_score(restaurant.cost, price/10) +
                    ratings_weight * calculate_rating_score(restaurant.rate, ratings) +
                    distance_weight * calculate_location_score(restaurant.longitude, restaurant.latitude, longitude, latitude, distance)
                )
                weighted_scores.append((restaurant, score))

            sorted_restaurants = sorted(weighted_scores, key=lambda x: x[1], reverse=True)
            top_restaurants = sorted_restaurants[:10]

            results = []
            for match in top_restaurants:
                results.append(match[0])

            #wyczyszczenie tabeli pomocniczej
            matchedRestaurants = MatchedRestaurants.query.all()
            for matchedRestaurant in matchedRestaurants:
                db.session.delete(matchedRestaurant)
                db.session.commit()
            #
            #zapis wyniku do bazy
            for restaurant in results:
                match = Restaurants.query.filter_by(id=restaurant.id).first()
                matchedRestaurant = MatchedRestaurants(rest_name=match.rest_name, online_order=match.online_order,
                    book_table=match.book_table, rate=match.rate, votes=match.votes, rest_location=match.rest_location,
                    cost=match.cost, longitude=match.longitude, latitude=match.latitude)
                db.session.add(matchedRestaurant)
                db.session.commit()

            matchedRestaurants = MatchedRestaurants.query.all()
        elif submit_type == 'saveRestaurant':
            fav_rest_name = request.form.get('fav-rest-id')
            restaurant = Restaurants.query.filter_by(rest_name=fav_rest_name).first()
            fav_rest = UserRestaurant(user_id=current_user.id, restaurant_id=restaurant.id)
            db.session.add(fav_rest)
            db.session.commit()
            return redirect(url_for('favourite'))

        return redirect(url_for('match'))

    return render_template('match.html', title='MATCH', cuisines=cuisines, matchedRestaurants=matchedRestaurants, matchChoice=matchChoice)


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

def clearMatchRestaurants():
    matchedRestaurants = MatchedRestaurants.query.all()
    for matchedRestaurant in matchedRestaurants:
        db.session.delete(matchedRestaurant)
        db.session.commit()\

def clearMatchChoice():
    matchChoice = TempMatchTable.query.first()
    if matchChoice:
        db.session.delete(matchChoice)
        db.session.commit()