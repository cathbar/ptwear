#!/bin/bash
#curl -H "Content-Type: application/json" -X POST -d "{"exercise_name":"Gut Buster", "sensor_data": { "time": 0.0, "x": 0.0, "y": 0.0, "z": 0.0 }, { "time": 1.0, "x": 0.0, "y": 10.0, "z": 0.0 }, { "time": 2.0, "x": 0.0, "y": 20.0, "z": 0.0 } ] }" http://localhost:5000/ptwear/api/v1.0/reps 
#curl -H "Content-Type: application/json" -X POST -d "{"exercise_name":"Gut Buster", "sensor_data": [{"time:": 0.0, "x": 0.0, "y": 0.0, "z": 0.0},{"time:": 0.0, "x": 10.0, "y": 0.0, "z": 0.0},{"time:": 0.0, "x": 20.0, "y": 0.0, "z": 0.0}]}" http://localhost:5000/ptwear/api/v1.0/reps 
#curl -H "Content-Type: application/json" -X POST -d "{"exercise_name": "shoulder buster", "sensor_data": [{"y": 0, "x": 0, "z": 0, "time": 0}, {"y": 205, "x": 115, "z": 300, "time": 1}, {"y": 20, "x": 15, "z": 115, "time": 10}]}" http://localhost:5000/ptwear/api/v1.0/reps 
#curl -H "Content-Type: application/json" -X POST -d "{"shotType": "Type 1", "time_id": 1500959134185, "sensor_data": {"rot_z": 0.041813991963863373, "rot_y": 0.0096010398119688034, "rot_x": -0.088323228061199188, "acc_z": -0.11028144508600235, "acc_y": -0.61829781532287598, "acc_x": 0.66272741556167603}}" http://localhost:5000/ptwear/api/v1.0/reps


#curl -H "Content-Type: application/json" -X POST -d '{"shotType": "Type 1", "time_id": 1500959134185, "sensor_data": {"rot_z": 0.041813991963863373, "rot_y": 0.0096010398119688034, "rot_x": -0.088323228061199188, "acc_z": -0.11028144508600235, "acc_y": -0.61829781532287598, "acc_x": 0.66272741556167603}}' http://localhost:5000/ptwear/api/v1.0/reps
#curl -H "Content-Type: application/json" -X POST -d '{"shotType": "Type -1", "time_id": 1500959134185, "sensor_data": {"rot_z": 0.041813991963863373, "rot_y": 0.0096010398119688034, "rot_x": -0.088323228061199188, "acc_z": -0.11028144508600235, "acc_y": -0.61829781532287598, "acc_x": 0.66272741556167603}}' http://localhost:5000/ptwear/api/v1.0/reps
curl -H "Content-Type: application/json" -X POST -d '{"score": 12}' http://localhost:5000/ptwear/api/v1.0/score

