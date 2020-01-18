from google.cloud import datastore
import datetime

datastore_client = datastore.Client()

def store_data(value):
    entity = datastore.Entity(key=datastore_client.key('entry'))
    entity.update({
        'footprint': value,
        'timestamp': datetime.datetime.now()
    })