from flask import render_template, url_for, flash, redirect, request, jsonify
from dineder import app, db, bcrypt
from dineder.forms import RegistrationForm, LoginForm
from dineder.models import Users, Restaurants, Cuisines, CuisinesRestaurants, UserRestaurant, Preferences
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
import requests
from geopy.distance import geodesic


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
    preferences = Preferences.query.all()
    if request.method == 'POST':
        preference_id = request.form.get('preference_id')
        preference = Preferences.query.get_or_404(preference_id)

        # decyzja na podjecia na podstawie przycisku albo usuwam albo generuje
        cuisine = preference.cuisine
        price = preference.price
        ratings = preference.ratings
        distance = preference.distance
        cuisine_weight = preference.cuisine_weight
        price_weight = preference.price_weight
        ratings_weight = preference.ratings_weight
        distance_weight = preference.distance_weight

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
    return render_template('fav-restaurant.html', title='LIKE')


@app.route("/match-restaurant", methods=['GET', 'POST'])
def getYourMatch():
    cuisines = Cuisines.query.all()  # pobranie wszystkich dostępnych rodzajów kuchni z bazy do wyświetlenie ich w liście dla użytkownika

    if request.method == 'POST':

        cuisine = request.form.get('cuisine')
        price = float(request.form.get('price'))
        ratings = float(request.form.get('ratings'))
        distance = float(request.form.get('distance'))
        cuisine_weight = int(request.form.get('cuisine_weight'))
        price_weight = int(request.form.get('price_weight'))
        ratings_weight = int(request.form.get('ratings_weight'))
        distance_weight = int(request.form.get('distance_weight'))

        params_weights = [cuisine_weight, price_weight, ratings_weight, distance_weight]

        # #sprawdzam dane pobrane od uzytkownika raczej to nie bedzie potrzebne
        # if distance == "other":
        #     print('af')
        # else:
        #     distance = float(distance)
        #
        # if ratings == "other":
        #     print('af')
        # else:
        #     ratings = float(ratings)
        #
        # if price == "other":
        #     print('af')
        # else:
        #     price = float(price)

        submit_type = request.form.get('submitType')

        if submit_type == 'save':
            preferences = Preferences(cuisine=cuisine, cuisine_importance=cuisine_weight, price=price,
                                      price_importance=price_weight, ratings=ratings, ratings_importance=ratings_weight,
                                      distance=distance, distance_importance=distance_weight, user_id=current_user.id)
            # print(preferences)
            db.session.add(preferences)
            db.session.commit()

        elif submit_type == 'getLocation':
            # print(cuisine)
            # print(price)
            # print(ratings)
            # print(distance)
            # print(cuisine_weight)
            # print(price_weight)
            # print(ratings_weight)
            # print(distance_weight)

            # pobranie lokalizacji użytkownika
            res = requests.get('https://ipinfo.io/')
            data = res.json()
            location = data['loc'].split(',')
            latitude = location[0]
            longitude = location[1]
            user_location = (latitude, longitude)

            print("Latitude : ", latitude)
            print("Longitude : ", longitude)

            # wyznaczanie wag - które filtry będę uwzględnione jako pierwsze
            weights = []
            pair_rating = ("rating", ratings_weight)
            pair_price = ("price", price_weight)
            pair_distance = ("allowed_distance", distance_weight)
            weights.append(pair_rating)
            weights.append(pair_price)
            weights.append(pair_distance)
            weights = sorted(weights, key=lambda x: x[1], reverse=True)

            # na podstawie nazwy kuchni pobieram id cusine - kuchnia kryterium, które będzie najważniejsze
            row_cuisine = Cuisines.query.filter_by(cuisine=cuisine).first()
            # print(row_cuisine.id)
            rowsCuisneRestaurant = CuisinesRestaurants.query.filter_by(cuisine_id=row_cuisine.id).all()
            print(rowsCuisneRestaurant)
            filtered_restaurants = []
            for rowCuisneRestaurant in rowsCuisneRestaurant:
                restaurant = Restaurants.query.filter_by(id=rowCuisneRestaurant.restaurant_id).first()
                filtered_restaurants.append({'name': restaurant.rest_name, 'cuisine': cuisine, 'price_range': restaurant.cost/10,
                               'rating': restaurant.rate, 'location': (restaurant.latitude, restaurant.longitude)})

#to na później
            # for i in weights:
            #     if i[0] == "price":
            #         result = price_filter(price, result)
            #     if i[0] == "rating":
            #         result = rating_filter(ratings, result)
            #     if i[0] == "allowed_distance":
            #         result = location_filter(user_location, distance, result)

            # póki co wypisanie co sie udało przefiltrować - dostajemy McD :)
            for i in filtered_restaurants:
                print(i)

            # lista tych restauracji do algorytmu ma trafić?
            result = ahpCalculate(filtered_restaurants, user_location, params_weights, distance)
            print(result)

            # na podstawie cuisine id szukam restauracji które pasują pod to kryterium
            # restaurantsWithSpecificCuisine = CuisinesRestaurants.query.filter_by(cuisine_id=cuisine_id.id).all()
            # print(restaurantsWithSpecificCuisine)
        return render_template('match.html', title='MATCH', cuisines=cuisines, carusel='true', saved_cuisine=cuisine,
                               saved_price=price, saved_ratings=ratings, saved_distance=distance,
                               saved_cuisine_weight=cuisine_weight, saved_price_weight=price_weight,
                               saved_ratings_weight=ratings_weight, saved_distance_weight=distance_weight)

    return render_template('match.html', title='MATCH', cuisines=cuisines, carusel='false')


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