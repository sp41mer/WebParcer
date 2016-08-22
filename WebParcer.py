# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,jsonify
from sources.models import Group
import parse_it, peewee

app = Flask(__name__)


@app.route('/')
def show_input_field():
    return render_template('enter_query.html')

@app.route('/searches')
def pass_query_strings():
    _query = 'материнский капитал'
    for group in Group.select():
        group_id = group.vk_id
    a = 1
    return a


@app.route('/input_query', methods=['POST'])
def create_tables():
     _query = request.form['queryString']
     database = peewee.PostgresqlDatabase(
                    'parsing_db',
                    user='root',
                    password='root',
                    host='localhost'
                )
     if Group.select().where(Group.query_string == _query):
        success = 0
     else:
         success = 1
     response = {
         'success': success,
         'message': _query
     }
     return jsonify(response)

if __name__ == '__main__':
    app.run()
