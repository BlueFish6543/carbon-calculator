from google.cloud import datastore
import datetime

datastore_client = datastore.Client()

def store_data(footprint, food_type, year=None, month=None, day=None):
    entity = datastore.Entity(key=datastore_client.key('entry'))
    entity.update({
        'footprint': footprint,
        'type': food_type,
        # 'timestamp': datetime.datetime.now(),
        'year': year if year is not None else datetime.datetime.now().year,
        'month': month if month is not None else datetime.datetime.now().month,
        'day': day if day is not None else datetime.datetime.now().day
    })
    datastore_client.put(entity)

def get_all_data():
    query = datastore_client.query(kind='entry')
    data = list(query.fetch())
    return data

def get_data_by_date(year, month, day):
    query = datastore_client.query(kind='entry')
    query.add_filter('year', '=', year)
    query.add_filter('month', '=', month)
    query.add_filter('day', '=', day)
    data = list(query.fetch())
    return data

def delete_data():
    query = datastore_client.query(kind='entry')
    data = list(query.fetch())
    for entity in data:
        datastore_client.delete(entity.key)