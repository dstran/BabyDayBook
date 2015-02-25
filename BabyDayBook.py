import os
import json

from pymongo import MongoClient
from flask import Flask, render_template, url_for, make_response, send_file, jsonify, request
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy
from SearchBabyDaybook import SearchBabyDaybook

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')
# This already imnport from mongoengine
from DataModel.Checkup import *



app = Flask(__name__)

# Database helper
dbfile = os.path.dirname(os.path.abspath(__file__)) + '\\babydaybook.db'
dbHelper = SearchBabyDaybook(dbfile)

# Use hardcode data for now.
checkups = [
    {
        'weight': 91,
        'weight_percent': 0,
        'height': 18.9,
        'height_percent': 0,
        'head_cir': 0,
        'head_cir_percent': 0,
        'notes': 'Newborn',
    },
    {
        'weight': 134,
        'weight_percent': 26,
        'height': 21.75,
        'height_percent': 66,
        'head_cir': 14,
        'head_cir_percent': 17,
        'notes': 'One month checkup',
    },
    {
        'weight': 182,
        'weight_percent': 49,
        'height': 23.25,
        'height_percent': 68,
        'head_cir': 15,
        'head_cir_percent': 20,
        'notes': 'Two month checkup',
    }
]

# Talking to MongoDB works but require setup so that's why it's commented out now.
# # MongoEngine
# connect('checkups_db2')


@app.route('/')
@app.route('/index')
def index():
    # Using render_template will cause Flask to interpret angular templates as jinja templates.
    return send_file('templates/index.html')

@app.route('/api/summary', methods=['GET'])
def get_summary():
    # return Checkup.objects.to_json()
    # Must have hash key.
    return jsonify({'summary': checkups})

@app.route('/api/summaryAdd', methods=['POST'])
def put_summary():
    args = json.loads(request.data)

    # Insert to mongodb.
    # mongoDBItems.insert({'value': args['item']})
    # return jsonify({'success': True})

    checkups.append(args['item'])
    return jsonify({'success': True})

@app.route('/api/search', methods=['POST'])
def search_db():
    args = json.loads(request.data)
    recs = dbHelper.query_db(args['item'])

    rows = [ dict(rec) for rec in recs ]
    json_data = json.dumps(rows)
    return jsonify({'results': json_data})

@app.route('/api/prepareChart', methods=['GET'])
def prepare_chart():
    items = dbHelper.prepare_chart()
    print items

    chart_json = json.dumps([obj.__dict__ for obj in items.values()])
    print chart_json

    return jsonify({'chart': chart_json})

if __name__ == "__main__":
    app.run(debug=True)

