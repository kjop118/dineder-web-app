import math
from flask import render_template, url_for, flash, redirect, request, jsonify
from dineder import app, db, bcrypt
from dineder.forms import RegistrationForm, LoginForm
from dineder.models import Users, Restaurants, Cuisines, CuisinesRestaurants, UserRestaurant, Preferences, MatchedRestaurants, TempMatchTable
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
import requests
from geopy.distance import geodesic

from sqlalchemy import select


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
    return render_template('account.html', title='Account', preferences=preferences)


@app.route("/favourite", methods=['GET', 'POST'])
@login_required
def getFavRestaurant():
    clearMatchChoice()
    clearMatchRestaurants()

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


@app.route("/match", methods=['GET', 'POST'])
def match():
    restaurants = Restaurants.query.all()

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

        if submit_type == 'save':
            preferences = Preferences(cuisine=cuisine, cuisine_importance=cuisine_weight, price=price,
                                      price_importance=price_weight, ratings=ratings, ratings_importance=ratings_weight,
                                      distance=distance, distance_importance=distance_weight, user_id=current_user.id)
            db.session.add(preferences)
            db.session.commit()

        elif submit_type == 'getLocation':

            print("cześć")

            # pobranie lokalizacji użytkownika
            res = requests.get('https://ipinfo.io/')
            data = res.json()
            location = data['loc'].split(',')
            latitude = location[0]
            longitude = location[1]
            user_location = (latitude, longitude)

            # print("Latitude : ", latitude)
            # print("Longitude : ", longitude)

            # wyznaczanie wag - które filtry będę uwzględnione jako pierwsze

            weighted_scores = []
            for restaurant in restaurants:
                score = (
                    cuisine_weight * calculate_cuisine_score(restaurant.cuisine, cuisine) +
                    price_weight * calculate_price_range_score(restaurant.cost, price) +
                    ratings_weight * calculate_rating_score(restaurant.rate, ratings) +
                    distance_weight* calculate_location_score(restaurant.longitude, restaurant.latitude, longitude, latitude, distance)
                )
                weighted_scores.append((restaurant, score))
            
            sorted_restaurants = sorted(weighted_scores, key=lambda x: x[1], reverse=True)

            #to matched Restaurant wrzuć to 
            top_restaurants = sorted_restaurants[:10]

            
            # weights = []
            # pair_rating = ("rating", ratings_weight)
            # pair_price = ("price", price_weight)
            # pair_distance = ("allowed_distance", distance_weight)
            # weights.append(pair_rating)
            # weights.append(pair_price)
            # weights.append(pair_distance)
            # weights = sorted(weights, key=lambda x: x[1], reverse=True)

            # # na podstawie nazwy kuchni pobieram id cusine - kuchnia kryterium, które będzie najważniejsze
            # row_cuisine = Cuisines.query.filter_by(cuisine=cuisine).first()
            # # print(row_cuisine.id)
            # rowsCuisneRestaurant = CuisinesRestaurants.query.filter_by(cuisine_id=row_cuisine.id).all()
            # print(rowsCuisneRestaurant)
            # filtered_restaurants = []
            # for rowCuisneRestaurant in rowsCuisneRestaurant:
            #     restaurant = Restaurants.query.filter_by(id=rowCuisneRestaurant.restaurant_id).first()
            #     filtered_restaurants.append({'id': restaurant.id,'name': restaurant.rest_name, 'cuisine': cuisine, 'price_range': restaurant.cost/10,
            #                    'rating': restaurant.rate, 'location': (restaurant.latitude, restaurant.longitude)})

            # for i in weights:
            #     if i[0] == "price":
            #         filtered_restaurants = price_filter(price, filtered_restaurants)
            #     if i[0] == "rating":
            #         filtered_restaurants = rating_filter(ratings, filtered_restaurants)
            #     if i[0] == "allowed_distance":
            #         filtered_restaurants = location_filter(user_location, distance, filtered_restaurants)

            # lista tych restauracji do algorytmu ma trafić? tak ma trafić: algorytm do [rzetestowania
            # params_weights = [cuisine_weight, price_weight, ratings_weight, distance_weight]
            # result = ahpCalculate(filtered_restaurants, user_location, params_weights, distance)
            # print(result)

            #tymczasowe przyrównanie
            result = top_restaurants
            for i in result:
                print(i)
            #wyczyszczenie tabeli pomocniczej
            matchedRestaurants = MatchedRestaurants.query.all()
            for matchedRestaurant in matchedRestaurants:
                db.session.delete(matchedRestaurant)
                db.session.commit()

            #zapis wyniku do bazy
            for restaurant in result:
                match = Restaurants.query.filter_by(id=restaurant['id']).first()
                matchedRestaurant = MatchedRestaurants(rest_name=match.rest_name, online_order=match.online_order,
                    book_table=match.book_table, rate=match.rate, votes=match.votes, rest_location=match.rest_location,
                    cost=match.cost, longitude=match.longitude, latitude=match.latitude)
                db.session.add(matchedRestaurant)
                db.session.commit()

            matchedRestaurants = MatchedRestaurants.query.all()
            print(matchedRestaurants)

            # na podstawie cuisine id szukam restauracji które pasują pod to kryterium
            # restaurantsWithSpecificCuisine = CuisinesRestaurants.query.filter_by(cuisine_id=cuisine_id.id).all()
            # print(restaurantsWithSpecificCuisine)
        return redirect(url_for('match'))
        # return render_template('match.html', title='MATCH', cuisines=cuisines, matchedRestaurants=matchedRestaurants, saved_cuisine=cuisine,
        #                        saved_price=price, saved_ratings=ratings, saved_distance=distance,
        #                        saved_cuisine_weight=cuisine_weight, saved_price_weight=price_weight,
        #                        saved_ratings_weight=ratings_weight, saved_distance_weight=distance_weight)

    return render_template('match.html', title='MATCH', cuisines=cuisines, matchedRestaurants=matchedRestaurants, matchChoice=matchChoice)


def price_filter(price, restaurants):
    result = []
    for i in restaurants:
        if i["price_range"] < price:
            result.append(i)
    return result


def rating_filter(rating, restaurants):
    result = []
    for i in restaurants:
        if i["rating"] > rating:
            result.append(i)
    return result


def location_filter(user_location, allowed_distance, restaurants):
    # tu jeszcze normalizacja była?
    result = []
    for restaurant in restaurants:
        restaurant_location = restaurant['location']
        distance = geodesic(user_location, restaurant_location).km
        if distance < allowed_distance:
            result.append(restaurant)
    return result




def ahpCalculate(restaurants, user_location, weights, distance):
    w1 = weights[0]  # Waga dla kryterium Rodzaj kuchni
    w2 = weights[1]  # Waga dla kryterium Zakres cenowy
    w3 = weights[2]  # Waga dla kryterium Ocena
    w4 = weights[3]  # Waga dla kryterium Dystans
    max_distance_allowed = distance  # Maksymalny dozwolony dystans od użytkownika (w kilometrach)

    # Obliczanie odległości użytkownika od restauracji
    distances = []
    for restaurant in restaurants:
        restaurant_location = restaurant['location']
        distance = geodesic(user_location, restaurant_location).km
        distances.append(distance)

    # Normalizacja odległości
    max_distance = max(distances)
    normalized_distances = [distance / max_distance for distance in distances]

    # Macierz porównań
    comparison_matrix = np.array([
        [1, w1, w2, w3],  # Rodzaj kuchni
        [1 / w1, 1, w4, w4],  # Zakres cenowy
        [1 / w2, 1 / w4, 1, w4],  # Ocena
        [1 / w3, 1 / w4, 1 / w4, 1]  # Dystans
    ])

    # Waga dystansu
    normalized_distances_weight = w4  # Waga dla dystansu (ostatniego kryterium)

    # Uwzględnienie wag dla odległości w macierzy porównań
    weighted_comparison_matrix = np.copy(comparison_matrix)
    for i, distance_weight in enumerate(normalized_distances):
        if distances[i] > max_distance_allowed:
            distance_weight = 0

        weighted_comparison_matrix[i][-1] = distance_weight * normalized_distances_weight

    # Obliczanie wag kryteriów
    sum_column = np.sum(weighted_comparison_matrix, axis=0)
    criteria_weights = sum_column / np.sum(sum_column)

    # Obliczanie oceny restauracji
    scores = np.dot(weighted_comparison_matrix, criteria_weights)

    # Sortowanie restauracji w oparciu o ocenę
    sorted_restaurants = [restaurant for _, restaurant in sorted(zip(scores, restaurants), reverse=True)]

    # Wybór najlepszych 10 restauracji
    top_10_restaurants = sorted_restaurants[:10]

    # Wyświetlanie wyników
    # for i, restaurant in enumerate(top_10_restaurants):
    #     print(
    #         f"{i + 1}. {restaurant['name']}: {restaurant['cuisine']}, {restaurant['price_range']}, {restaurant['rating']}")
    return top_10_restaurants

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

