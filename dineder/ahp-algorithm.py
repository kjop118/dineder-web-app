import numpy as np
from geopy.distance import geodesic
#from dineder.models import Restaurants
# Dane wejściowe

user_location = (51.5074, -0.1278)  # Przykładowa lokalizacja użytkownika (Londyn)

restaurants = [
    {'name': 'Restauracja A', 'cuisine': 'Włoska', 'price_range': 3, 'rating': 4.2, 'location': (51.5115, -0.1160)},
    {'name': 'Restauracja B', 'cuisine': 'Meksykańska', 'price_range': 2, 'rating': 3.8, 'location': (51.5033, -0.1195)},
    {'name': 'Restauracja C', 'cuisine': 'Francuska', 'price_range': 4, 'rating': 4.5, 'location': (51.5067, -0.1340)},
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
    [1, w1, w2, w3],    # Rodzaj kuchni
    [1/w1, 1, w4, w4],  # Zakres cenowy
    [1/w2, 1/w4, 1, w4],    # Ocena
    [1/w3, 1/w4, 1/w4, 1]    # Dystans
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
    print(f"{i+1}. {restaurant['name']}: {restaurant['cuisine']}, {restaurant['price_range']}, {restaurant['rating']}")

def getMatchedRestaurants():
    # user_location = (51.5074, -0.1278)  # Przykładowa lokalizacja użytkownika (Londyn)
    # restaurants_db = Restaurants.query.all()
    # restaurants_all = []

    # for restaurant in restaurants_db:
    #     restaurants_all.append({'id': restaurant.id, 'name': restaurant.rest_name, 'online_order': restaurant.online_order,
    #                         'book_table': restaurant.book_table, 'rating': restaurant.rate, 'votes': restaurant.votes,
    #                         'price_range': restaurant.cost, 'rest_location': restaurant.rest_locatio,
    #                         'location': (restaurant.latitude, restaurant.longitude)})


 # dane, które wpisze user
    cuisine = 'Italian'
    cuisine_w = 5
    rating = 3.8
    rating_w = 3
    price = 700
    price_w = 4
    allowed_distance = 27
    allowed_distance_w = 2
    # to jakos pobierać
    user_location = (20, 50)

    # wyznaczanie wag - które filtry będę uwzględnione jako pierwsze
    weights = []   
    pair_rating = ("rating", rating_w)
    pair_price = ("price", price_w)
    pair_distance = ("allowed_distance", allowed_distance_w)
    weights.append(pair_rating)
    weights.append(pair_price)
    weights.append(pair_distance)
    weights = sorted(weights,key=lambda x: x[1], reverse=True)


    # na podstawie nazwy kuchni pobieram id cusine - kuchnia kryterium, które będzie najważniejsze
    row_cuisine = Cuisines.query.filter_by(cuisine=cuisine).first()
    print(row_cuisine.id)
    rowsCuisneRestaurant = CuisinesRestaurants.query.filter_by(cuisine_id=row_cuisine.id) 

    restaurants = []
    for rowCuisneRestaurant in rowsCuisneRestaurant:
        restaurant = Restaurants.query.filter_by(id=rowCuisneRestaurant.restaurant_id).first()
        restaurants.append({'name': restaurant.rest_name, 'cuisine': cuisine, 'price_range': restaurant.cost, 'rating': restaurant.rate, 'location': (restaurant.longitude, restaurant.latitude)})
    
    for i in weights:
        if i[0] == "price":
            restaurants = price_filter(price, restaurants)
        if i[0] == "rating":
            restaurants = rating_filter(rating, restaurants)
        if i[0] == "allowed_distance":
            restaurants = location_filter(user_location, allowed_distance, restaurants)

    #póki co wypisanie co sie udało przefiltrować 
    if len(restaurants) == 0:
        print("empty filter resultes")

    for i in restaurants:
        print(i)

    # restaurants = [
    #     {'name': 'Restauracja A', 'cuisine': 'Włoska', 'price_range': 3, 'rating': 4.2, 'location': (51.5115, -0.1160)},
    #     {'name': 'Restauracja B', 'cuisine': 'Meksykańska', 'price_range': 2, 'rating': 3.8,
    #      'location': (51.5033, -0.1195)},
    #     {'name': 'Restauracja C', 'cuisine': 'Francuska', 'price_range': 4, 'rating': 4.5,
    #      'location': (51.5067, -0.1340)},
    #     # ... Dodaj więcej restauracji
    # ]

    # w1 = 3  # Waga dla kryterium Rodzaj kuchni
    # w2 = 2  # Waga dla kryterium Zakres cenowy
    # w3 = 4  # Waga dla kryterium Ocena
    # w4 = 5  # Waga dla kryterium Dystans
    # max_distance_allowed = 5  # Maksymalny dozwolony dystans od użytkownika (w kilometrach)

    # Obliczanie odległości użytkownika od restauracji
    distances = []
    for restaurant in restaurants:
        restaurant_location = restaurant['location']
        distance = geodesic(user_location, restaurant_location).km
        distances.append(distance)

    for i in distances:
        print(i)
    
    # Normalizacja odległości
    max_distance = max(distances)
    normalized_distances = [distance / max_distance for distance in distances]

    
    for i in normalized_distances:
        print(i)

    # Macierz porównań
    comparison_matrix = np.array([
        [1, cuisine_w, price_w, rating_w],  # Rodzaj kuchni
        [1 / cuisine_w, 1, allowed_distance_w, allowed_distance_w],  # Zakres cenowy
        [1 / price_w, 1 / allowed_distance_w, 1, allowed_distance_w],  # Ocena
        [1 / rating_w, 1 / allowed_distance_w, 1 / allowed_distance_w, 1]  # Dystans
    ])

    # Waga dystansu
    normalized_distances_weight = allowed_distance_w  # Waga dla dystansu (ostatniego kryterium)

    # Uwzględnienie wag dla odległości w macierzy porównań
    weighted_comparison_matrix = np.copy(comparison_matrix)
    print (weighted_comparison_matrix)

    for i, distance_weight in enumerate(normalized_distances):
        print("iteration: " + str(i) + str(distance_weight))
        if distances[i] > allowed_distance:
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

    #tu jeszcze normalizacja była?
    result = []
    for restaurant in restaurants:
         restaurant_location = restaurant['location']
         distance = geodesic(user_location, restaurant_location).km
         if distance < allowed_distance:
             result.append(restaurant)
    return result

    #getMatchedRestaurants()
    # # dane, które wpisze user
    # cuisine = 'Afghan'
    # cuisine_w = 5
    # rating = 3.8
    # rating_w = 3
    # price = 700
    # price_w = 4
    # allowed_distance = 27
    # allowed_distance_w = 2
    # # to jakos pobierać
    # user_location = (20, 50)

    # # wyznaczanie wag - które filtry będę uwzględnione jako pierwsze
    # weights = []   
    # pair_rating = ("rating", rating_w)
    # pair_price = ("price", price_w)
    # pair_distance = ("allowed_distance", allowed_distance_w)
    # weights.append(pair_rating)
    # weights.append(pair_price)
    # weights.append(pair_distance)
    # weights = sorted(weights,key=lambda x: x[1], reverse=True)


    # # na podstawie nazwy kuchni pobieram id cusine - kuchnia kryterium, które będzie najważniejsze
    # row_cuisine = Cuisines.query.filter_by(cuisine=cuisine).first()
    # print(row_cuisine.id)
    # rowsCuisneRestaurant = CuisinesRestaurants.query.filter_by(cuisine_id=row_cuisine.id) 

    # result = []
    # for rowCuisneRestaurant in rowsCuisneRestaurant:
    #     restaurant = Restaurants.query.filter_by(id=rowCuisneRestaurant.restaurant_id).first()
    #     result.append({'name': restaurant.rest_name, 'cuisine': cuisine, 'price_range': restaurant.cost, 'rating': restaurant.rate, 'location': (restaurant.longitude, restaurant.latitude)})
    
    # for i in weights:
    #     if i[0] == "price":
    #         result = price_filter(price, result)
    #     if i[0] == "rating":
    #         result = rating_filter(rating, result)
    #     if i[0] == "allowed_distance":
    #         result = location_filter(user_location, allowed_distance, result)

    # #póki co wypisanie co sie udało przefiltrować - dostajemy McD :)
    # for i in result:
    #     print(i)