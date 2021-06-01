from flask import Flask, render_template, request, jsonify
import flask
import requests
import os
import config
import logging

app = Flask(__name__)


# MAIN PAGE - buttons to choose output
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# LIST EVERYTHING PAGE
@app.route('/listdata')
def listeverything():
    whichformat = request.args.get("whichformat", type=str)
    whichlist = request.args.get("whichlist", type=str)
    num_entries = request.args.get("num_entries", type=int)

    #all_data = requests.get('http://restapi:2000/listAll/' + whichformat +
            #'?top=' + str(num_entries))
    #open_data = requests.get('http://restapi:2000/listOpen/' + whichformat +
            #'?top=' + str(num_entries))
    #close_data = requests.get('http://restapi:2000/listClose/' + whichformat +
            #'?top=' + str(num_entries))
    #rslt = {"all_data": all_data.text, "open_data": open_data.text,
            #"close_data": close_data.text}

    data = requests.get('http://' + os.environ['BACKEND_ADDR'] + ':' + os.environ['BACKEND_PORT'] + whichlist + whichformat + '?top=' + str(num_entries))
    
    rslt = {'which_data': data.text}
    return jsonify(result=rslt)
    #return data.text

    # os.environ['BACKEND_PORT']
    # os.environ['BACKEND_ADDR']

    # TODO: get data by creating string of url with arguments from index.html

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
