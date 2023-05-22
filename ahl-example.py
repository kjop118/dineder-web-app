# importowanie potrzebnych modułów
from collections import defaultdict
import random

# lista restauracji
restaurant_list = [
    {"name": "Restauracja 1", "location": "Warszawa", "cuisine": "włoska", "price_range": "średni", "user_ratings": 4},
    {"name": "Restauracja 2", "location": "Kraków", "cuisine": "francuska", "price_range": "wysoki", "user_ratings": 5},
    {"name": "Restauracja 3", "location": "Gdańsk", "cuisine": "meksykańska", "price_range": "niski", "user_ratings": 3},
    {"name": "Restauracja 4", "location": "Wrocław", "cuisine": "japońska", "price_range": "średni", "user_ratings": 4},
    {"name": "Restauracja 5", "location": "Kraków", "cuisine": "włoska", "price_range": "wysoki", "user_ratings": 4},
]

# implementuj funkcję get_restaurants(), która zwróci listę restauracji spełniających kryteria
def get_restaurants(location):#, cuisine, price_range, user_ratings):
    # filtruj listę restauracji po kryteriach użytkownika
    filtered_restaurants = []
    for restaurant in restaurant_list:
        #  and restaurant["cuisine"] == cuisine and restaurant["price_range"] == price_range and restaurant["user_ratings"] >= user_ratings
        if restaurant["location"] == location:
            filtered_restaurants.append(restaurant)

    return filtered_restaurants



def choose_restaurant(location, cuisine, price_range, user_ratings):
    # przygotowanie listy restauracji spełniających kryteria użytkownika
    restaurants = get_restaurants(location)
    # print(restaurants)


    # inicjalizacja wag dla każdego kryterium decyzyjnego, docolowo użytkownik podaje kryterium
    weights = {"location": 0.25, "cuisine": 0.25, "price_range": 0.25, "user_ratings": 0.25}

    # inicjalizacja słownika dla każdej restauracji, aby przechowywać liczbę trafień
    restaurants_hits = {'restaurant': 0 for restaurant in restaurants}


    # liczba iteracji algorytmu
    num_iterations = 10

    for i in range(num_iterations):
        # losowe ustawienie wag dla każdego kryterium
        for k in weights.keys():
            weights[k] = random.uniform(0, 1)

        # wyliczenie punktów dla każdej restauracji
        for restaurant in restaurants:
            hits = 0
            for k, v in weights.items():
                if k == "location" and restaurant['location'] == location:
                    hits += v
                elif k == "cuisine" and restaurant['cuisine'] == cuisine:
                    hits += v
                elif k == "price_range" and restaurant['price_range'] == price_range:
                    hits += v
                elif k == "user_ratings" and restaurant['user_ratings'] >= user_ratings:
                    hits += v

            # zwiększenie liczby trafień dla danej restauracji
            restaurants_hits['restaurant'] += hits

    # wybór najlepszej restauracji na podstawie liczby trafień
    best_restaurant = max(restaurants_hits, key=restaurants_hits.get)
    print(best_restaurant)
    # best_restaurant = restaurants_hits

    return best_restaurant
# (location, cuisine, price_range, user_ratings)
search_restaurant = choose_restaurant("Kraków", "włoska", "wysoki", 4)
# print(search_restaurant)

