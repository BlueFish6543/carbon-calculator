from flask import Flask, render_template
from forms import UPCForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def upc_lookup():
    form = UPCForm()
    return render_template('index.html', title='UPC Lookup', form=form)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)