import pandas as pd
import main

data = pd.read_excel(r'aaq0216_DataS2.xls')

datadict = {}
for i in range(43):
    datadict[data.iloc[i, 0]] = data.iloc[i, 1]

def calc_emissions(UPC): #017082884022 05100023355
    product = main.query_barcode(UPC) 

    foods = {'Rice': ['Rice', 1000], 'Oatmeal': ['Oatmeal', 1000], 'Potatoes': ['Potatoes', 1000], 'Beef': ['Bovine Meat (beef herd)', 400], 'Bread': ['Wheat & Rye (Bread)', 1000], 'Fish': ['Fish (farmed)', 400], 'Egg': ['Eggs', 400], 'Cheese': ['Cheese', 400], 'Milk': ['Milk', 624], 'Chicken': ['Poultry Meat', 400], 'Turkey': ['Poultry Meat', 400], 'Bacon': ['Pig Meat', 400], 'Ham': ['Pig Meat', 400], 'Pork': ['Pig Meat', 400], 'Lamb': ['Lamb & Mutton', 400], 'Mutton': ['Lamb & Mutton', 400], 'Banana': ['Bananas', 890], 'Apple': ['Apples', 520], 'Olive Oil': ['Olive Oil', 8048], 'Nut': ['Nuts', 400], 'Pea': ['Peas', 810], 'Tofu': ['Tofu', 400], 'Tomato': ['Tomatoes', 180], 'Berries': ['Berries & Grapes', 330], 'Shrimp': ['Crustaceans (farmed)', 400]} #key is search item, value is [table item, NU factor]

    footprint = 'Unknown'

    for food in foods:
        if product[0].find(food) != -1: #ie beef found
            footprint = datadict[foods[food][0]]*product[1]/foods[food][1] #starch is 1000kcal
            break

    return footprint


print(calc_emissions('05100023355')) #chicken example
#{'Wheat & Rye (Bread)': 0.6, 'Maize (Meal)': 0.4, 'Barley (Beer)': 0.2, 'Oatmeal': 0.9, 'Rice': 1.2, 'Potatoes': 0.6, 'Cassava': 1.4, 'Cane Sugar': 3.2, 'Beet Sugar': 1.8, 'Other Pulses': 0.8, 'Peas': 0.4, 'Nuts': 0.3, 'Groundnuts': 1.2, 'Soymilk': 1.0, 'Tofu': 2.0, 'Soybean Oil': 6.3, 'Palm Oil': 7.3, 'Sunflower Oil': 3.6, 'Rapeseed Oil': 3.8, 'Olive Oil': 5.4, 'Tomatoes': 2.1, 'Onions & Leeks': 0.5, 'Root Vegetables': 0.4, 'Brassicas': 0.5, 'Other Vegetables': 0.5, 'Citrus Fruit': 0.4, 'Bananas': 0.9, 'Apples': 0.4, 'Berries & Grapes': 1.5, 'Wine': 0.1, 'Other Fruit': 1.1, 'Coffee': 0.4, 'Dark Chocolate': 2.3, 'Bovine Meat (beef herd)': 50.0, 'Bovine Meat (dairy herd)': 17.0, 'Lamb & Mutton': 20.0, 'Pig Meat': 7.6, 'Poultry Meat': 5.7, 'Milk': 3.2, 'Cheese': 11.0, 'Eggs': 4.2, 'Fish (farmed)': 6.0, 'Crustaceans (farmed)': 18.0}