from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
from forms import UPCForm, UPCFileForm, UPCStringForm
from config import Config
import history
import requests
import os
import datetime
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

def store_time(dt, email):
    entity = datastore.Entity(key=datastore_client.key('{}-visit'.format(email)))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit, email):
    query = datastore_client.query(kind='{}-visit'.format(email))
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
date_range = 7

def authenticate():
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
            print(claims)
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

        # Record and fetch the recent times a logged-in user has accessed
        # the site. This is currently shared amongst all users, but will be
        # individualized in a following step.
        if claims is not None:
            store_time(datetime.datetime.now(), claims['email'])
            times = fetch_times(10, claims['email'])
    
    return claims, error_message, times

@app.route('/')
def user():
    claims, error_message, times = authenticate()
    return render_template(
        'user.html',
        user_data=claims, error_message=error_message, times=times)

@app.route('/add', methods=['GET', 'POST'])
def main():
    claims, error_message, times = authenticate()
    if claims is None:
        return redirect(url_for('user'))
    
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
                        footprint, food_type = calc_emissions((label, calories))
                        footprint = round(float(footprint), 1)
                        db.store_data(footprint, food_type, email=claims['email'])
                        text += "<br>Success!<br>Label: {}<br>Food type: {}<br>Carbon footprint: {} kg CO2".format(label, food_type, footprint)
                    except ValueError:
                        text += "<br>Unable to obtain carbon footprint."
        else:
            # Look up
            labels = detect(filename)
            try:
                footprint, food_type = calc_emissions_pic(labels)
                footprint = round(float(footprint), 1)
                db.store_data(footprint, food_type, email=claims['email'])
                text = "Success!<br>Food type: {}<br>Carbon footprint: {}".format(food_type, footprint)
            except ValueError:
                text = "Unable to obtain carbon footprint."
        return redirect(url_for('main'))

    elif string_form.validate_on_submit():
        label, calories = query_barcode(form.data['upc'])
        if not label:
            text = "Unable to obtain carbon footprint."
        else:
            try:
                footprint, food_type = calc_emissions((label, calories))
                footprint = round(float(footprint), 1)
                db.store_data(footprint, food_type, email=claims['email'])
                text = "Success!<br>Label: {}<br>Food type: {}<br>Carbon footprint: {} kg CO2".format(label, food_type, footprint)
            except ValueError:
                text = "Unable to obtain carbon footprint."
        return redirect(url_for('main'))

    return render_template('index.html', title='Carbon footprint calculator', form=form, text=text)

@app.route('/history', methods=['GET', 'POST'])
def show_history():
    claims, error_message, times = authenticate()
    print(claims)
    if claims is None:
        return redirect(url_for('user'))

    global date_range
    try:
        date_range = int(request.form['range'])
    except KeyError:
        date_range = 7
    history.plot(date_range, email=claims['email'])
    history.plot_pie_chart(email=claims['email'])
    table_data = history.sort_types(email=claims['email'])
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'tmp.png')
    filename2 = os.path.join(app.config['UPLOAD_FOLDER'], 'tmp2.png')
    reduction = history.weekly_improvement(email=claims['email'])
    return render_template('history.html', image=filename, table_data=table_data, reduction=reduction, image2=filename2)

@app.after_request
def adding_header_content(head):
    head.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    head.headers["Pragma"] = "no-cache"
    head.headers["Expires"] = "0"
    head.headers['Cache-Control'] = 'public, max-age=0'
    return head

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)