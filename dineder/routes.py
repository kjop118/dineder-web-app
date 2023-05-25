from flask import render_template, url_for, flash, redirect, request, jsonify
from dineder import app, db, bcrypt
from dineder.forms import RegistrationForm, LoginForm
from dineder.models import Users, Restaurants, Cuisines
from flask_login import login_user, current_user, logout_user, login_required
import numpy as np
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
    return render_template('account.html', title='Account')

@app.route("/favourite", methods=['GET', 'POST'])
@login_required
def getFavRestaurant():
    return render_template('fav-restaurant.html', title='LIKE')

@app.route("/match-restaurant", methods=['GET', 'POST'])
def getYourMatch():
    cuisines = Cuisines.query.all()
    cuisine = Cuisines.query.get(10)
    print(cuisine)
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



def getMatchedRestaurants(user_location, weights, ):
    user_location = (51.5074, -0.1278)  # Przykładowa lokalizacja użytkownika (Londyn)
    restaurants_db = Restaurants.query.all()
    restaurants_all = []

    for restaurant in restaurants_db:
        restaurants_all.append({'id': restaurant.id, 'name': restaurant.rest_name, 'online_order': restaurant.online_order,
                            'book_table': restaurant.book_table, 'rating': restaurant.rate, 'votes': restaurant.votes,
                            'price_range': restaurant.cost, 'rest_location': restaurant.rest_locatio,
                            'location': (restaurant.latitude, restaurant.longitude)})

    restaurants = [
        {'name': 'Restauracja A', 'cuisine': 'Włoska', 'price_range': 3, 'rating': 4.2, 'location': (51.5115, -0.1160)},
        {'name': 'Restauracja B', 'cuisine': 'Meksykańska', 'price_range': 2, 'rating': 3.8,
         'location': (51.5033, -0.1195)},
        {'name': 'Restauracja C', 'cuisine': 'Francuska', 'price_range': 4, 'rating': 4.5,
         'location': (51.5067, -0.1340)},
        # ... Dodaj więcej restauracji
    ]

    w1 = 3  # Waga dla kryterium Rodzaj kuchni
    w2 = 2  # Waga dla kryterium Zakres cenowy
    w3 = 4  # Waga dla kryterium Ocena
    w4 = 5  # Waga dla kryterium Dystans
    max_distance_allowed = 5  # Maksymalny dozwolony dystans od użytkownika (w kilometrach)

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
    for i, restaurant in enumerate(top_10_restaurants):
        print(
            f"{i + 1}. {restaurant['name']}: {restaurant['cuisine']}, {restaurant['price_range']}, {restaurant['rating']}")