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