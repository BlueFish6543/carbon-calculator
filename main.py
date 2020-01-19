from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
from forms import UPCForm, UPCFileForm, UPCStringForm
from config import Config
import history
import requests
import os
import db
from food_carbon_database import calc_emissions
from food_scan import detect, calc_emissions_pic
import barcode_reader
from google.auth.transport import requests as google_requests
from google.cloud import datastore
import google.oauth2.id_token
import datetime

firebase_request_adapter = google_requests.Request()
datastore_client = datastore.Client()

app = Flask(__name__)
app.config.from_object(Config)

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times

def query_barcode(upc):
    url = 'https://api.edamam.com/api/food-database/parser'
    params = {
        'upc': str(upc),
        'app_id': '33ae2aa3',
        'app_key': 'e7dc83ee3feec2561e8a66012bdaa72d'
    }
    r = requests.get(url=url, params=params)
    data = r.json()
    try:
        label = data['hints'][0]['food']['label']
        calories = data['hints'][0]['food']['nutrients']['ENERC_KCAL']
    except KeyError:
        label = ''
        calories = ''
    return label, calories

text = ""

@app.route('/')
def user():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

        # Record and fetch the recent times a logged-in user has accessed
        # the site. This is currently shared amongst all users, but will be
        # individualized in a following step.
        store_time(datetime.datetime.now())
        times = fetch_times(10)

    return render_template(
        'user.html',
        user_data=claims, error_message=error_message, times=times)

@app.route('/addfood', methods=['GET', 'POST'])
def main():
    global text
    form = UPCForm()
    file_form = UPCFileForm()
    string_form = UPCStringForm()

    if file_form.validate_on_submit():
        f = form.image.data
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(filename)
        if form.barcode_submit.data:
            # Scan barcode and look up
            barcode = barcode_reader.scan(filename)
            if not barcode:
                text = "Failed to read barcode."
            else:
                upc = barcode.decode('ascii')
                text = "Barcode: {}".format(upc)
                label, calories = query_barcode(upc)
                if not label:
                    text += "<br>Unable to obtain carbon footprint."
                else:
                    try:
                        footprint = round(float(calc_emissions((label, calories))), 1)
                        db.store_data(footprint, 'test')
                        text += "<br>Success!<br>Label: {}<br>Carbon footprint: {}".format(label, footprint)
                    except ValueError:
                        text += "<br>Unable to obtain carbon footprint."
        else:
            # Look up
            labels = detect(filename)
            try:
                footprint = round(float(calc_emissions_pic(labels)), 1)
                db.store_data(footprint, 'test')
                text = "Success!<br>Carbon footprint: {}".format(footprint)
            except ValueError:
                text = "Unable to obtain carbon footprint."
        return redirect(url_for('main'))

    elif string_form.validate_on_submit():
        label, calories = query_barcode(form.data['upc'])
        if not label:
            text = "Unable to obtain carbon footprint."
        else:
            try:
                footprint = round(float(calc_emissions((label, calories))), 1)
                db.store_data(footprint, 'test')
                text = "Success!<br>Label: {}<br>Carbon footprint: {}".format(label, footprint)
            except ValueError:
                text = "Unable to obtain carbon footprint."
        return redirect(url_for('main'))

    return render_template('index.html', title='Carbon footprint calculator', form=form, text=text)

@app.route('/history', methods=['GET', 'POST'])
def show_history():
    history.plot()
    table_data = history.sort_types()
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'tmp.png')
    return render_template('history.html', image=filename, table_data=table_data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)