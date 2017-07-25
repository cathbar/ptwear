#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
import os.path
import json,random
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils

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
    shot_obj = request.get_json()
    shot_probs = [.9, .6, .2, .5, .2, .05]
    print shot_obj

    cls = int(shot_obj['shotType'].replace("Type ", ""))
    shot_obj[shotType] = cls
    id = shot_obj['time_id']
    hit = random.random() < shot_probs[cls]
    sensor_data = shot_obj['sensor_data']
    acc_x = sensor_data['acc_x'] 
    acc_y = sensor_data['acc_y'] 
    acc_z = sensor_data['acc_z'] 
    rot_x = sensor_data['rot_x'] 
    rot_y = sensor_data['rot_y'] 
    rot_z = sensor_data['rot_z'] 
    shot_obj['shotType'] = cls
    last_rep['hit'] = hit
    if cls == -1:
        #Test shot
        with open('last_rep.txt', 'w') as the_file:
            the_file.write("{0}\n".format(last_rep))
        with open('test_shot.txt', 'w') as the_file:
            the_file.write("{0}  1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6}\n".format(cls, acc_x, acc_y, acc_z, rot_x, rot_y, rot_z))
        data_test = MLUtils.loadLibSVMFile(sc, "test_shot.txt")
        predictions = model.predict(testData.map(lambda x: x.features))
        print str(predictions.collect())
    else:
        #Training shot
        with open('all_reps.txt', 'a') as the_file:
            the_file.write("{0}  1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6}\n".format(cls, acc_x, acc_y, acc_z, rot_x, rot_y, rot_z))


    


    print "CLS: " + str(cls)
    return jsonify( { 'rep': make_public_rep(last_rep) } ), 201

def train_model(train_filename):
    # Load and parse the data file into an RDD of LabeledPoint.
    trainingData= MLUtils.loadLibSVMFile(sc, train_filename)
    # Train a RandomForest model.
    #  Empty categoricalFeaturesInfo indicates all features are continuous.
    #  Note: Use larger numTrees in practice.
    #  Setting featureSubsetStrategy="auto" lets the algorithm choose.
    model = RandomForest.trainClassifier(trainingData, numClasses=3, categoricalFeaturesInfo={},
                                         numTrees=3, featureSubsetStrategy="auto",
                                         impurity='gini', maxDepth=4, maxBins=32)
    return model

if __name__ == '__main__':
    last_rep = reps[0]
    model = train_model('training_data.txt')
    app.run(debug = True, host='0.0.0.0')
