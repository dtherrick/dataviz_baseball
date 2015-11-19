from bson import json_util
from bson.json_util import dumps
from flask import Flask
from flask import render_template
import json
from pymongo import MongoClient

app = Flask(__name__)

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DBNAME = 'mlbstandings'
COLLECTION = 'standings2015'
FIELDS = {'Tm': True, 'GB': True, 'date': True, 'division': True, '_id': False}


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/standings/year')
def standings_year():
    connection = MongoClient(MONGO_HOST, MONGO_PORT)
    collection = connection[DBNAME][COLLECTION]
    allStandings = collection.find(projection=FIELDS)
    json_standings = []
    for standing in allStandings:
        json_standings.append(standing)
    json_standings = json.dumps(json_standings, default=json_util.default)
    connection.close()
    return json_standings

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
