from flask import Flask, render_template
from forms import UPCForm, UPCFileForm, UPCStringForm
from config import Config
import history
import requests
import os
import db
from flask import request

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

@app.route('/', methods=['GET', 'POST'])
def main():
    form = UPCForm()
    file_form = UPCFileForm()
    string_form = UPCStringForm()
    if file_form.validate_on_submit():
        print("looking for image")
        # print(form.files)
        # image_data = form.data['image']
        image_data = request.files[form.image.name].read()
        print(image_data)
        label, calories = query_barcode(image_data)
        if not label:
            pass
        else:
            # Do something with the label and calories data
            print(label, calories)
    elif string_form.validate_on_submit():
        print("looking for string")
        label, calories = query_barcode(form.data['upc'])
        if not label:
            pass
        else:
            # Do something with the label and calories data
            pass

    return render_template('index.html', title='Carbon footprint calculator', form=form)

@app.route('/history')
def show_history():
    history.plot()
    table_data = history.sort_types()
    filename = os.path.join(app.config['UPLOAD_FOLDER'], 'tmp.png')
    return render_template('history.html', image=filename, table_data=table_data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)