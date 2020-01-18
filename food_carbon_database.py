import pandas as pd

data = pd.read_excel(r'aaq0216_DataS2.xls')
#df = pd.DataFrame(data, columns= ['Product','Price'])
datadict = {}
for i in range(43):
    datadict[data.iloc[i, 0]] = data.iloc[i, 1]
print(data)
print(datadict)

#{'Wheat & Rye (Bread)': 1.57, 'Maize (Meal)': 1.7, 'Barley (Beer)': 1.18, 'Oatmeal': 2.48, 'Rice': 4.45, 'Potatoes': 0.46, 'Cassava': 1.32, 'Cane Sugar': 3.2, 'Beet Sugar': 1.81, 'Other Pulses': 1.79, 'Peas': 0.98, 'Nuts': 0.43, 'Groundnuts': 3.23, 'Soymilk': 0.98, 'Tofu': 3.16, 'Soybean Oil': 6.32, 'Palm Oil': 7.32, 'Sunflower Oil': 3.6, 'Rapeseed Oil': 3.77, 'Olive Oil': 5.42, 'Tomatoes': 2.09, 'Onions & Leeks': 0.5, 'Root Vegetables': 0.43, 'Brassicas': 0.51, 'Other Vegetables': 0.53, 'Citrus Fruit': 0.39, 'Bananas': 0.86, 'Apples': 0.43, 'Berries & Grapes': 1.53, 'Wine': 1.79, 'Other Fruit': 1.05, 'Coffee': 28.53, 'Dark Chocolate': 46.65, 'Bovine Meat (beef herd)': 99.48, 'Bovine Meat (dairy herd)': 33.3, 'Lamb & Mutton': 39.72, 'Pig Meat': 12.31, 'Poultry Meat': 9.87, 'Milk': 3.15, 'Cheese': 23.88, 'Eggs': 4.67, 'Fish (farmed)': 13.63, 'Crustaceans (farmed)': 26.87}