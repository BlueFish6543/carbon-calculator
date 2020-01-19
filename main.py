from flask import Flask, render_template, redirect, url_for
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

app = Flask(__name__)
app.config.from_object(Config)

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

@app.route('/', methods=['GET', 'POST'])
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