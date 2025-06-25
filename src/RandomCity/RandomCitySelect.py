import json
import random

def selectRandomCity(path):
    with open(path, 'r') as file:
        data = json.load(file)

    print(data["cities"])
    cities = data["cities"]
    return cities[random.randint(0,len(cities))]