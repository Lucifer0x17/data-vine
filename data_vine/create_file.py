import json
import os


def createJson(name, data):
    path = 'JSON'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, f"{name}.json"), 'w') as outfile:
        json.dump(data, outfile)


def createDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def createAvsc(name, data):
    path = 'AVSC'
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path, f"{name}.avsc"), 'w') as outfile:
        json.dump(data, outfile)


def checkPath(path):
    if not os.path.exists(path):
        return 0
