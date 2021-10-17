from flask import Flask
import data_vine.functions as dv
from flask.json import jsonify


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/<string:table>', methods=['GET'])
def currentState(table):
    curTable = dv.getCurrentState(table)
    return jsonify(curTable)


@app.route('/<string:table>/<string:date>',methods=['GET'])
def tableDiff(table,date):
    pkeyname = returnidname(table)
    delta = dv.fetchDelta(table,date,pkeyname)
    return jsonify(delta)


@app.route('/<string:table>/<string:date>/<int:id>',methods=['GET'])
def tableDiffHistory(table,date,id):
    pkeyname = returnidname(table)
    delta = dv.fetchDeltaHistory(table,date,pkeyname,id)
    return jsonify(delta)

def returnidname(table):
    if(table=='order'):
        return 'id'
    elif(table=='product'):
        return 'productid'
    elif(table=='user'):
        return 'userid'
    elif(table=='supplier'):
        return 'supplierid'


if __name__ == '__main__':
    app.run(debug=True,port=6969)