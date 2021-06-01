from flask import Flask, jsonify
import flask
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient
import os
import logging

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
database = client.tododb

# TODO: get info from database
# translate info from database into csv form if specified
# otherwise keep it in json form
# take into account top entries argument

def getData(which_format, num_entries, which_list):
    data = list(database.tododb.find())
    values = []

    # if num_entries is specified
    if num_entries == None:
        num_entries = len(data)
    if num_entries > len(data):
        num_entries = len(data) - 1
    if num_entries != -1:
    # get desired entries
        data = data[:num_entries]

    if which_list == "open":
        # only get km and open times - get rid of close times
        for entry in data:
            entry.pop("close", None)
            entry.pop("loc", None)
            entry.pop("_id", None)
            csv = "miles,km,open\n"
    elif which_list == "close":
        # only get km and close times - get rid of open times
        for entry in data:
            entry.pop("open", None)
            entry.pop("loc", None)
            entry.pop("_id", None)
            csv = "miles,km,close\n"
    else:
        # keep data as is
        for entry in data:
            entry.pop("_id", None)
            csv = "miles,km,loc,open,close\n"

    app.logger.debug(data)

    if which_format == "csv":
        i = 0
        for entry in data:
            # get values from dict
            values.append(list(entry.values())) # [0, 00:00, 01:00]
            # join values
            csv += ",".join(values[i]) + "\n" # 0,00:00,01:00\n
            app.logger.debug(csv)
            i += 1
        return csv
    else:
        # format is JSON
        app.logger.debug(jsonify(data))
        return jsonify(data)

# add top entries argument
parser = reqparse.RequestParser()
parser.add_argument('top', type=int)
class listAll(Resource):
    def get(self, dtype):
        args = parser.parse_args()
        num_entries = args['top']
        return getData(dtype, num_entries, "all")

parser = reqparse.RequestParser()
parser.add_argument('top', type=int)
class listOpenOnly(Resource):
    def get(self, dtype):
        args = parser.parse_args()
        num_entries = args['top']
        return getData(dtype, num_entries, "open")

parser = reqparse.RequestParser()
parser.add_argument('top', type=int)
class listCloseOnly(Resource):
    def get(self, dtype):
        args = parser.parse_args()
        num_entries = args['top']
        return getData(dtype, num_entries, "close")

# add resources
api.add_resource(listAll, '/listAll', '/listAll/<string:dtype>')
api.add_resource(listOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:dtype>')
api.add_resource(listCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:dtype>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
