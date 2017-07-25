#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import os.path

app = Flask(__name__, static_url_path = "")
last_rep = {}
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

reps = [
    {
    'exercise_name': 'butt turdler',
    'sensor_data': [
        {
            'time': 0.0,
            'x': 0.0,
            'y': 0.0,
            'z': 0.0,
        },
        {
            'time': 1.0,
            'x': 10.0,
            'y': 0.0,
            'z': 0.0,
        },
        {
            'time': 2.0,
            'x': 20.0,
            'y': 0.0,
            'z': 0.0,
        }
        ]
    },
    {
    'exercise_name': 'shoulder buster',
    'sensor_data': [
        {
            'time': 0.0,
            'x': 0.0,
            'y': 0.0,
            'z': 0.0,
        },
        {
            'time': 1.0,
            'x': 0.0,
            'y': 10.0,
            'z': 0.0,
        },
        {
            'time': 2.0,
            'x': 0.0,
            'y': 20.0,
            'z': 0.0,
        }
        ]
    },
]

def make_public_rep(rep):
    new_rep = {}
    for field in rep:
        if field == 'id':
            new_rep['uri'] = url_for('get_rep', rep_id = rep['id'], _external = True)
        else:
            new_rep[field] = rep[field]
    return new_rep

@app.route('/ptwear/api/v1.0/last_rep', methods = ['GET'])
def get_last_rep():
    #return last_rep
    last_rep = {"exercise_name": "This shouldn't happen"}
    if os.path.isfile('last_rep.txt'): 
        with open('last_rep.txt', 'r') as the_file:
            last_rep=the_file.read().replace('\n', '')
    return str(last_rep)

@app.route('/ptwear/api/v1.0/reps', methods = ['POST'])
def create_rep():
    if not request.json :
        abort(400)
    last_rep = request.get_json()
    with open('last_rep.txt', 'w') as the_file:
        the_file.write(str(last_rep))
    return jsonify( { 'rep': make_public_rep(last_rep) } ), 201

if __name__ == '__main__':
    last_rep = reps[0]
    app.run(debug = True, host='0.0.0.0')
