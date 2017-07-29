#!/usr/bin/python2.7
###flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for, send_file
import os.path
import json,random
import findspark
findspark.init(spark_home='/data/spark15')
from pyspark import SparkContext
sc = SparkContext()
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
from plotly.graph_objs import *
import plotly

app = Flask(__name__, static_url_path = "")
base_dir = 'file:///root/ptwear/'

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

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
    last_rep = {"ERROR": "Couldn't find a last rep. This shouldn't happen."}
    if os.path.isfile('last_rep.txt'): 
        with open('last_rep.txt', 'r') as the_file:
            last_rep=the_file.read().replace('\n', '')
    return str(last_rep)

@app.route('/ptwear/api/v1.0/reps', methods = ['POST'])
def create_rep():
    print "Got a post request!"
    if not request.get_json():
        abort(400)
    shot_obj = request.get_json()
    shot_probs = [.9, .6, .2, .5, .2, .05]
    print shot_obj

    cls = int(shot_obj['shotType'].replace("Type ", ""))
    shot_obj['shotType'] = cls
    id = shot_obj['time_id']
    sensor_data = shot_obj['sensor_data']
    acc_x = sensor_data['acc_x'] 
    acc_y = sensor_data['acc_y'] 
    acc_z = sensor_data['acc_z'] 
    rot_x = sensor_data['rot_x'] 
    rot_y = sensor_data['rot_y'] 
    rot_z = sensor_data['rot_z'] 
    shot_obj['shotType'] = cls
    if cls == -1:
        #Test shot
        print "Received test shot"
        data_test = MLUtils.loadLibSVMFile(sc, base_dir + "test_shot.txt")
        predictions = model.predict(data_test.map(lambda x: x.features)).collect()
        prediction = int(predictions[0])
        hit = random.random() < shot_probs[prediction]
        shot_obj['hit'] = int(hit)
        print "Predicting: {0}".format(prediction)
        shot_obj['shotType'] = int(prediction)
        with open('last_rep.txt', 'w') as the_file:
            the_file.write("{0}\n".format(shot_obj))
        with open('test_shot.txt', 'w') as the_file:
            the_file.write("{0}  1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6}\n".format(cls, acc_x, acc_y, acc_z, rot_x, rot_y, rot_z))
        with open('predictions.txt', 'a') as pred_file:
            for pred in predictions:
                pred_file.write("{0}\n".format(int(pred)))
        print "Predicting: {0}, {1}".format(prediction, hit)
        return str((prediction, hit))
    else:
        #Training shot
        print "Received training shot"
        #with open('all_reps.txt', 'a') as the_file:
        with open('training_data.txt', 'a') as the_file:
            the_file.write("{0}  1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6}\n".format(cls, acc_x, acc_y, acc_z, rot_x, rot_y, rot_z))
    print "CLS: " + str(cls)
    return jsonify( { 'rep': make_public_rep(shot_obj) } ), 201

@app.route('/ptwear/api/v1.0/score', methods = ['POST'])
def create_score():
    print "Got a score post request!"
    if not request.get_json():
        abort(400)
    score_obj = request.get_json()
    print str(score_obj)
    with open('scores.txt', 'a') as score_file:
        score_file.write("{0}\n".format(int(score_obj['score'])))
    return get_score()


@app.route('/ptwear/api/v1.0/score', methods = ['GET'])
def get_score():
    with open('scores.txt') as f:
        scores = f.readlines()
    if len(scores) != 0:
        scores = [int(x.strip()) for x in scores] 
    
    return str(sorted(scores, reverse=True)[:10])

@app.route('/ptwear/api/v1.0/get_image')
def get_image():
    filename = 'predictions_distribution.png'
    fig = plt.figure()
    ax = fig.add_subplot(111)
    shot_types = ('Normal', 'Chest Hurl', 'Shotput', 'Granny', 'Overhead', 'Overhand')
    y_pos = np.arange(len(shot_types))
    
    with open('predictions.txt') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    if len(content) != 0:
        content = [int(x.strip()) for x in content] 
    
    shot_counts = [content.count(0), content.count(1), content.count(2), content.count(3), content.count(4), content.count(5)]
    ax.barh(y_pos, shot_counts, align='center', color='green')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(shot_types)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Count')
    ax.set_title('Prediction Distribution')
    fig.savefig(filename)

    data = Data([ Histogram(x=content) ])
    plot_url = py.plot(data, filename='Predictions')

    return send_file(filename, mimetype='image/png')

@app.route('/ptwear/api/v1.0/get_image2')
def get_image2():
    filename = 'predictions_over_time.png'
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #y_pos = np.arange(len(shot_types))
    
    shot_probs = [.9, .6, .2, .5, .2, .05]
    with open('predictions.txt') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    if len(content) != 0:
        content = [int(x.strip()) for x in content] 
    xs = range(1, len(content)+1)
    shot_counts = content
    scores = []
    for shot in shot_counts:
        offset = random.random()%.25
        if random.random() < .5:
            offset = -offset
        new_score = shot*shot_probs[shot] + offset
        if new_score < 0:
            new_score = 0
        elif new_score > 1:
            new_score = 1
        scores.append(new_score)
    ax.plot(xs, scores, '-.', color='green')
    ax.plot(xs, scores, '*', ms=15, color='blue')
    ax.set_xticks(xs)
    ax.set_xticklabels(xs)
    ax.set_xlabel('Shot #')
    ax.set_title('Performance Over Time')
    fig.savefig(filename)



    data = Data([ Scatter(x=xs, y=scores) ])
    plot_url = py.plot(data, filename='PerformanceOverTime')

    return send_file(filename, mimetype='image/png')

def train_model(train_filename):
    # Load and parse the data file into an RDD of LabeledPoint.
    trainingData= MLUtils.loadLibSVMFile(sc, base_dir + train_filename)
    # Train a RandomForest model.
    #  Empty categoricalFeaturesInfo indicates all features are continuous.
    #  Note: Use larger numTrees in practice.
    #  Setting featureSubsetStrategy="auto" lets the algorithm choose.
#    model = RandomForest.trainClassifier(trainingData, numClasses=6, categoricalFeaturesInfo={},
#                                         numTrees=3, featureSubsetStrategy="auto",
#                                         impurity='gini', maxDepth=4, maxBins=32)
    model = RandomForest.trainClassifier(trainingData, numClasses=4, categoricalFeaturesInfo={},
                                         numTrees=3, featureSubsetStrategy="auto",
                                         impurity='gini', maxDepth=4, maxBins=32)
    return model

if __name__ == '__main__':
    plotly.tools.set_credentials_file(username='dkenny', api_key='I3maDPBABGUpd6My6ad2')
    print sc.parallelize([1,2,3]*1000).count()
    model = train_model('training_data.txt')
    app.run(debug = True, host='0.0.0.0')
