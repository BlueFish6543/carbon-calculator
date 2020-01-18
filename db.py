from google.cloud import datastore
import datetime

datastore_client = datastore.Client()

def store_data(value):
    entity = datastore.Entity(key=datastore_client.key('entry'))
    entity.update({
        'footprint': value,
        'timestamp': datetime.datetime.now(),
        'year': datetime.datetime.now().year,
        'month': datetime.datetime.now().month,
        'day': datetime.datetime.now().day
    })
    datastore_client.put(entity)

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