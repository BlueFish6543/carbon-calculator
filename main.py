from flask import Flask, render_template
from forms import UPCForm
from config import Config
import requests

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
    return data['label']

@app.route('/', methods=['GET', 'POST'])
def main():
    form = UPCForm()
    if form.validate_on_submit():
        label = query_barcode(form.data['upc'])
        # Do something with the label
    return render_template('index.html', title='Carbon footprint calculator', form=form)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)