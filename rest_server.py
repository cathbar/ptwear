#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import os.path
import json,random
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
    if not request.get_json():
        abort(400)
    last_rep = request.get_json()
    print last_rep
    shot_probs = [.9, .6, .2, .5, .2, .05]
    shot_obj = last_rep
    #shot_obj = json.loads(last_rep.replace("u'",'"').replace("'",'"'))
#{u'shotType': u'Type 1', u'time_id': 1500952518695, u'sensor_data': {u'acc_z': -0.28961142897605896, u'acc_y': -0.64209622144699097, u'acc_x': 0.065950259566307068}}
    cls = int(shot_obj['shotType'].replace("Type ", ""))
    id = shot_obj['time_id']
    hit = random.random() < shot_probs[cls]
    sensor_data = shot_obj['sensor_data']
    acc_x = sensor_data['acc_x'] 
    acc_y = sensor_data['acc_y'] 
    acc_z = sensor_data['acc_z'] 
    rot_x = sensor_data['rot_x'] 
    rot_y = sensor_data['rot_y'] 
    rot_z = sensor_data['rot_z'] 
    last_rep['shotType'] = cls
    last_rep['hit'] = hit
    print "CLS: " + str(cls)
    with open('last_rep.txt', 'w') as the_file:
        the_file.write("{0}\n".format(last_rep))
    with open('all_reps.txt', 'a') as the_file:
        the_file.write("{0}  1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6}\n".format(cls, acc_x, acc_y, acc_z, rot_x, rot_y, rot_z))
    return jsonify( { 'rep': make_public_rep(last_rep) } ), 201

if __name__ == '__main__':
    last_rep = reps[0]
    app.run(debug = True, host='0.0.0.0')
