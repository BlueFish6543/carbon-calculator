import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
import db
import os

def plot():
    today = datetime.date.today()

    footprints, dates = [], []
    for i in reversed(range(7)):
        date = today - datetime.timedelta(i)
        dates.append(str(date))
        data = db.get_data_by_date(date.year, date.month, date.day)
        fp = 0.
        for entity in data:
            fp += float(entity['footprint'])
        footprints.append(fp)

    fig = plt.figure()
    x_pos = [i for i, _ in enumerate(footprints)]
    plt.bar(dates, footprints)
    plt.xlabel('Dates')
    plt.ylabel('Carbon Footprint')
    plt.xticks(x_pos, dates, rotation=45)
    plt.grid()
    plt.tight_layout()
    plt.savefig(os.path.join('static', 'tmp', 'tmp.png'))

def sort_types():
    today = datetime.date.today()

    dictionary = {}
    for i in range(7):
        date = today - datetime.timedelta(i)
        data = db.get_data_by_date(date.year, date.month, date.day)
        for entity in data:
            try:
                dictionary[entity['type']] += entity['footprint']
            except KeyError:
                dictionary[entity['type']] = entity['footprint']
    
    sorted_data = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    return sorted_data