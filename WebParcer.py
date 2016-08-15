from flask import Flask, render_template, request,json
from sources import *

app = Flask(__name__)


@app.route('/')
def show_input_field():
    return render_template('enter_query.html')


@app.route('/input_query', methods=['POST'])
def create_tables():
     _query = request.form['queryString']



if __name__ == '__main__':
    app.run()
