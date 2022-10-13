from flask import Flask, request
import flask
from app_service import AppService
import json

app = Flask(__name__)
appService = AppService();


@app.route('/')
def home():
    return "App Works!!!"


@app.route('/api/tasks')
def tasks():
    return appService.get_tasks()

## Custom POST to convert subnet to cidr ##
@app.route('/api/convert', methods=['POST'])
def create_task():
    # check body is a valid json
    try: 
        request_data = request.get_json()
    except: 
        resp = flask.Response(json.dumps({'error': "Your body is not a valid json."}), 400)
        resp.headers['Content-Type']="application/json"
        return resp

    # check body has key subnet 
    if "subnet" not in request_data: 
        resp = flask.Response(json.dumps({'error': "Your body must contain key 'subnet'."}), 400)
        resp.headers['Content-Type']="application/json"
        return resp

    # covert subnet to cidr 
    try: 
        cidr_body = request_data['subnet']
        cidr = sum(bin(int(x)).count('1') for x in cidr_body.split('.'))
        resp = flask.Response(json.dumps({'cidr': cidr}))
        resp.headers['Content-Type']="application/json"
        return resp
    except: 
        resp = flask.Response(json.dumps({'error': "There was a problem decoding your subnet. Please provide a valid subnet value."}), 400)
        resp.headers['Content-Type']="application/json"
        return resp


@app.route('/api/task', methods=['PUT'])
def update_task():
    request_data = request.get_json()
    return appService.update_task(request_data['task'])


@app.route('/api/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    return appService.delete_task(id)

