from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug import *

import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:lucifer@localhost:7000/deltah2h'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(
    'postgresql://postgres:lucifer@localhost:7000/deltah2h')
