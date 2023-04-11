from flask import Flask
from flask_restful import Api
import json
from flask_cors import CORS

app = Flask(__name__) 
cors = CORS(app) 
api = Api(app) 

@app.route('/allObstacles')
def allObstacles():
    with open('public/Flughindernisse.geojson', 'r') as f:
        return json.load(f)

@app.route('/obstacles/<string:type>')
def obstacles(type):
    with open('public/Flughindernisse.geojson', 'r') as f:
        j = json.load(f)["features"]
        res = []
        for i in j:
            if i["properties"]["OBJEKTBEZEICHNUNG"] == type:
               res.append(i)
        return res

@app.route('/allObstacleTypes')
def allObstacleTypes():
    with open('public/Flughindernisse.geojson', 'r') as f:
        j = json.load(f)["features"]
        res = [] 
        for i in j:
            type = i["properties"]["OBJEKTBEZEICHNUNG"]
            if type not in res:
                res.append(type)
        return res
        
if __name__ == '__main__':
    app.run(debug=True)