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

def weekly_average(today): #today = when 'today' is, either actually today or one week ago
    dates = []
    week_mean = 0
    for i in reversed(range(7)):
        date = today - datetime.timedelta(i)
        dates.append(str(date))
        data = db.get_data_by_date(date.year, date.month, date.day)
        for entity in data:
            week_mean += float(entity['footprint'])
    week_mean = week_mean/7
    return week_mean

def weekly_improvement():
    this_week = weekly_average(datetime.date.today()) #today
    last_week = weekly_average(datetime.date.today() - datetime.timedelta(7)) #one week ago

    if last_week == 0.0:
        return 'No data for previous week.'

    percentage_difference = (this_week - last_week)*100/last_week
    
    if percentage_difference >= 0:
        return "You're carbon footprint increased by " + str(round(percentage_difference, 1)) + "%" + " compared to last week."
    else:
        return "You're carbon footprint decreased by " + str(abs(round(percentage_difference, 1))) + "%" + " compared to last week."
    


print(weekly_improvement())