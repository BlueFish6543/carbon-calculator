import db
import numpy as np
import matplotlib.pyplot as plt
import datetime
import random

foods = {'Rice': ['Rice', 1000], 'Oatmeal': ['Oatmeal', 1000], 'Potatoes': ['Potatoes', 1000], 'Beef': ['Bovine Meat (beef herd)', 400], 'Bread': ['Wheat & Rye (Bread)', 1000], 'Fish': ['Fish (farmed)', 400], 'Egg': ['Eggs', 400], 'Cheese': ['Cheese', 400], 'Milk': ['Milk', 624], 'Chicken': ['Poultry Meat', 400], 'Turkey': ['Poultry Meat', 400], 'Bacon': ['Pig Meat', 400], 'Ham': ['Pig Meat', 400], 'Pork': ['Pig Meat', 400], 'Lamb': ['Lamb & Mutton', 400], 'Mutton': ['Lamb & Mutton', 400], 'Banana': ['Bananas', 890], 'Apple': ['Apples', 520], 'Olive Oil': ['Olive Oil', 8048], 'Nut': ['Nuts', 400], 'Pea': ['Peas', 810], 'Tofu': ['Tofu', 400], 'Tomato': ['Tomatoes', 180], 'Berries': ['Berries & Grapes', 330], 'Shrimp': ['Crustaceans (farmed)', 400], 'Pasta': ['Wheat & Rye (Bread)', 1000]} #key is search item, value is [table item, NU factor]
email = 'bluefish6543@gmail.com'

if __name__ == '__main__':
    db.delete_data('{}-entry'.format(email))
    samples = np.zeros(200)
    samples = np.random.exponential(scale=50, size=samples.shape)
    today = datetime.date.today()
    for n in samples:
        if n > 100:
            continue
        n = (100 - n) / 3
        date = today - datetime.timedelta(n)
        food_type = random.choice(list(foods.keys()))
        footprint = round(np.random.random() * 50, 1)
        db.store_data(footprint, food_type, date.year, date.month, date.day, email=email)  
