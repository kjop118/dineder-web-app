import numpy as np
from geopy.distance import geodesic
import gpsd

def get_user_location():
    # Połączenie z serwerem gpsd
    gpsd.connect()

    # Odczyt bieżących danych lokalizacyjnych
    packet = gpsd.get_current()

    if packet.mode >= 2:
        user_location = (packet.lat, packet.lon)
        return user_location
    else:
        print("Nie można pobrać lokalizacji użytkownika.")

# Przykład użycia
user_location = get_user_location()
if user_location:
    print("Aktualna lokalizacja użytkownika:", user_location)




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





# import numpy as np
#
# # Dane dotyczące restauracji (przykładowe dane)
# restaurants = [
#     {"name": "Restauracja A", "location": (52.2297, 21.0122), "cuisine": "Włoska", "price_range": "$$$", "rating": 4.5},
#     {"name": "Restauracja B", "location": (52.2370, 21.0175), "cuisine": "Meksykańska", "price_range": "$$", "rating": 4.0},
#     {"name": "Restauracja C", "location": (52.2283, 20.9984), "cuisine": "Azjatycka", "price_range": "$$$$", "rating": 4.8},
#     # ...dodaj więcej restauracji...
# ]
#
# # restaurant_list = [
# #     {"name": "Restauracja 1", "location": "Warszawa", "cuisine": "włoska", "price_range": "średni", "user_ratings": 4},
# #     {"name": "Restauracja 2", "location": "Kraków", "cuisine": "francuska", "price_range": "wysoki", "user_ratings": 5},
# #     {"name": "Restauracja 3", "location": "Gdańsk", "cuisine": "meksykańska", "price_range": "niski", "user_ratings": 3},
# #     {"name": "Restauracja 4", "location": "Wrocław", "cuisine": "japońska", "price_range": "średni", "user_ratings": 4},
# #     {"name": "Restauracja 5", "location": "Kraków", "cuisine": "włoska", "price_range": "wysoki", "user_ratings": 4},
# #     {"name": "Restauracja 6", "location": "Kraków", "cuisine": "włoska", "price_range": "niski", "user_ratings": 3},
# #     {"name": "Restauracja 7", "location": "Kraków", "cuisine": "włoska", "price_range": "średni", "user_ratings": 5},
# # ]
#
# # Wagi kryteriów (przykładowe wagi)
# weights = {
#     "location": 5.0,
#     "cuisine": 4.0,
#     "price_range": 1.0,
#     "rating": 1.0,
#     "distance": 5.0
# }
#
# # Lokalizacja użytkownika (przykładowe dane)
# user_location = (52.2305, 21.0084)
#
# # Obliczanie dystansu dla każdej restauracji
# def calculate_distance(location1, location2):
#     # Tutaj możesz użyć odpowiednich funkcji do obliczenia dystansu na podstawie długości i szerokości geograficznej
#     # Przykład: obliczenie odległości na podstawie współrzędnych geograficznych (przykładowa implementacja)
#     return np.sqrt((location1[0] - location2[0]) ** 2 + (location1[1] - location2[1]) ** 2)
#
# # Obliczanie normalizowanych wartości dla kryteriów
# def normalize_values(values):
#     normalized_values = np.array(values)
#     return normalized_values / np.sum(normalized_values)
#
# # Obliczanie wyników dla restauracji
# def calculate_scores(restaurants):
#     scores = []
#     for restaurant in restaurants:
#         score = (
#             weights["location"] * calculate_distance(user_location, restaurant["location"]) +
#             weights["cuisine"] +
#             weights["price_range"] +
#             weights["rating"]
#         )
#         scores.append(score)
#     return scores
#
# # Rangowanie i wybór 10 najlepszych restauracji
# def select_top_restaurants(restaurants, scores):
#     sorted_restaurants = [r for _, r in sorted(zip(scores, restaurants), reverse=True)]
#     return sorted_restaurants[:10]
#
# # Wywołanie funkcji i wyświetlenie wyników
# scores = calculate_scores(restaurants)
# top_restaurants = select_top_restaurants(restaurants, scores)
#
# for i, restaurant in enumerate(top_restaurants, 1):
#     print(f"{i}. {restaurant['name']}")





# from collections import defaultdict
# from dineder import db
# import random
#
# # lista restauracji
# restaurant_list = [
#     {"name": "Restauracja 1", "location": "Warszawa", "cuisine": "włoska", "price_range": "średni", "user_ratings": 4},
#     {"name": "Restauracja 2", "location": "Kraków", "cuisine": "francuska", "price_range": "wysoki", "user_ratings": 5},
#     {"name": "Restauracja 3", "location": "Gdańsk", "cuisine": "meksykańska", "price_range": "niski", "user_ratings": 3},
#     {"name": "Restauracja 4", "location": "Wrocław", "cuisine": "japońska", "price_range": "średni", "user_ratings": 4},
#     {"name": "Restauracja 5", "location": "Kraków", "cuisine": "włoska", "price_range": "wysoki", "user_ratings": 4},
#     {"name": "Restauracja 6", "location": "Kraków", "cuisine": "włoska", "price_range": "niski", "user_ratings": 3},
#     {"name": "Restauracja 7", "location": "Kraków", "cuisine": "włoska", "price_range": "średni", "user_ratings": 5},
# ]
#
# # implementuj funkcję get_restaurants(), która zwróci listę restauracji spełniających kryteria
# def get_restaurants(location):#, cuisine, price_range, user_ratings):
#     # filtruj listę restauracji po kryteriach użytkownika
#     filtered_restaurants = []
#     for restaurant in restaurant_list:
#         #  and restaurant["cuisine"] == cuisine and restaurant["price_range"] == price_range and restaurant["user_ratings"] >= user_ratings
#         if restaurant["location"] == location:
#             filtered_restaurants.append(restaurant)
#
#     return filtered_restaurants
#
#
#
# def choose_restaurant(location, cuisine, price_range, user_ratings):
#     # przygotowanie listy restauracji spełniających kryteria użytkownika
#     restaurants = get_restaurants(location)
#
# #po co mi to jest
#     restaurants_hits = []
#     for restaurant in restaurants:
#         restaurants_hits.append({restaurant.get("name"): 0})
#         # print(restaurant)
#
#     # print(restaurants_hits)
#
#
#     # inicjalizacja wag dla każdego kryterium decyzyjnego, docolowo użytkownik podaje kryterium
#     weights = {"location": 5, "cuisine": 4, "price_range": 2, "user_ratings": 1}
#
#     # inicjalizacja słownika dla każdej restauracji, aby przechowywać liczbę trafień
#     # restaurants_hits = {'restaurant': 0 for restaurant in restaurants}
#     # print(restaurants_hits)
#     # def restaurants_hits = []
#
#     # liczba iteracji algorytmu
#     num_iterations = 10
#
#     for i in range(num_iterations):
#         # losowe ustawienie wag dla każdego kryterium
#         # for k in weights.keys():
#         #     weights[k] = random.uniform(0, 1)
#
#         # wyliczenie punktów dla każdej restauracji
#         for restaurant in restaurants:
#             hits = 0
#             print(restaurant)
#             for k, v in weights.items():
#                 if k == "location" and restaurant['location'] == location:
#                     hits += v
#                 elif k == "cuisine" and restaurant['cuisine'] == cuisine:
#                     hits += v
#                 elif k == "price_range" and restaurant['price_range'] == price_range:
#                     hits += v
#                 elif k == "user_ratings" and restaurant['user_ratings'] >= user_ratings:
#                     hits += v
#
#             # zwiększenie liczby trafień dla danej restauracji
#             restaurants_hits[restaurant] += hits
#
#     # wybór najlepszej restauracji na podstawie liczby trafień
#     best_restaurant = max(restaurants_hits, key=restaurants_hits.get)
#     print(best_restaurant)
#     # best_restaurant = restaurants_hits
#
#     return best_restaurant
# # (location, cuisine, price_range, user_ratings)
# # print(get_restaurants("Kraków"))
# search_restaurant = choose_restaurant("Kraków", "włoska", "wysoki", 4)
# print(search_restaurant)
#
