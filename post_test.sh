#!/bin/bash
#curl -H "Content-Type: application/json" -X POST -d '{"exercise_name":"Gut Buster", "sensor_data": { "time": 0.0, "x": 0.0, "y": 0.0, "z": 0.0 }, { "time": 1.0, "x": 0.0, "y": 10.0, "z": 0.0 }, { "time": 2.0, "x": 0.0, "y": 20.0, "z": 0.0 } ] }' http://localhost:5000/ptwear/api/v1.0/reps 
curl -H "Content-Type: application/json" -X POST -d '{"exercise_name":"Gut Buster", "sensor_data": [{"time:": 0.0, "x": 0.0, "y": 0.0, "z": 0.0},{"time:": 0.0, "x": 10.0, "y": 0.0, "z": 0.0},{"time:": 0.0, "x": 20.0, "y": 0.0, "z": 0.0}]}' http://localhost:5000/ptwear/api/v1.0/reps 
