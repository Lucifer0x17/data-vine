from . import json_a
from . import schema
from . import create_file
import os
import re
import glob


def createDelta(tableName, oldState, newState, method, updatedAt, pkeyName=None, pkey=None):
    delta = []
    path = f'AVRO/{tableName}/'
    create_file.createDir(path)
    if method == "PUT":
        for eachRow in oldState:
            if eachRow[pkeyName] == pkey:
                delta.append(eachRow)
                create_file.createDir(f'{path}/{eachRow[pkeyName]}')
                json_a.json_to_avro(
                    delta, f'AVRO/{tableName}/{eachRow[pkeyName]}/{updatedAt}.avro', f'AVSC/{tableName}.avsc')
                break
    elif method == "POST":
        newRow = newState.pop()
        # columns = newRow.keys()
        # for column in columns:
        #     if column != pkeyName:
        #         newRow[column] = None
        # delta.append(newRow)
        # print(delta)
        create_file.createDir(f'{path}/{newRow[pkeyName]}')
        # json_a.json_to_avro(
        #     delta, f'AVRO/{tableName}/{newRow[pkeyName]}/{updatedAt}.avro', f'AVSC/{tableName}.avsc')
        f = open(f'AVRO/{tableName}/{newRow[pkeyName]}/{updatedAt}.created','w')
        f.close()
    elif method == "DELETE":
        for eachRow in oldState:
            if eachRow[pkeyName] == pkey:
                delta.append(eachRow)
                create_file.createDir(f'{path}/{eachRow[pkeyName]}')
                json_a.json_to_avro(
                    delta, f'AVRO/{tableName}/{eachRow[pkeyName]}/{updatedAt}.avro', f'AVSC/{tableName}.avsc')
                break
    else:
        return "NOT A VALID REQUEST"
    updateState(tableName, newState)


def updateState(tableName, newState):
    try:
        path = f'AVRO/current_state'
        create_file.createDir(path)
        json_a.json_to_avro(
            newState, f'AVRO/current_state/{tableName}.avro', f'AVSC/{tableName}.avsc')
    except Exception as e:
        print(e)


def createAvsc(tableName, columnDetails):
    try:
        avsc = schema.getAvsc(columnDetails, tableName)
        create_file.createAvsc(tableName, avsc)
    except Exception as e:
        print(e)


def getCurrentState(tableName):
    try:
        path = f'AVRO/current_state/{tableName}.avro'
        if create_file.checkPath(path) == 0:
            return "NO TABLE TO SHOW"
        currentState = json_a.avro_to_json(path)
        return currentState
    except Exception as e:
        print(e)



def fetchDeltaHistory(tableName, timeStamp, pkeyName, pkey):
    oldState = []
    currentState = getCurrentState(tableName)
    if currentState:
        for eachRow in currentState:
            if eachRow[pkeyName] == pkey:
                oldState.append(eachRow)
                break
    if len(oldState) == 0:
        oldState.append({"Deleted":"True"})
    path = f'AVRO/{tableName}/{pkey}/'
    if create_file.checkPath(path) == 0:
        return oldState
    deltapaths = os.listdir(path)
    deltapaths.sort(reverse=True)
    for deltapath in deltapaths:
        if deltapath.endswith(".created"):
            ts = deltapath.split('.')[0]
            oldState.append({"created":"True","Timestamp":f'{ts}'})
            continue
        deltapath = deltapath.split('.')[0]
        if deltapath > timeStamp:
            # print(deltapath)
            oldRow = json_a.avro_to_json(f'{path}{deltapath}.avro')
            oldState.append(oldRow[0])
            # if oldState[len(oldState)-1] == oldState[len(oldState)-2]:
            #     oldState.pop()
            #     return oldState
    return oldState

def fetchDelta(tableName, timeStamp, pkeyName):
    oldState = []
    alteredRows = os.listdir(f'AVRO/{tableName}/')
    alteredRows = list(alteredRows)
    alteredRows = [int(i) for i in alteredRows]
    currentState = getCurrentState(tableName)
    res = [ sub[f'{pkeyName}'] for sub in currentState ]
    rowsId = res + alteredRows
    rowsId.sort()
    for eachId in rowsId:
        history = fetchDeltaHistory(tableName,timeStamp,pkeyName,eachId)
        print(history)
        oldState.append(history[len(history)-1])
    return oldState


