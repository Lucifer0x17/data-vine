from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug import *

import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ovyyruepateoix:a5ba93f40a61ea6a88740d31a94ddb5b1b68459dcb3e557b0c110d30b92e76c4@ec2-34-203-91-150.compute-1.amazonaws.com:5432/d24nenp2hf2vqp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine('postgres://ovyyruepateoix:a5ba93f40a61ea6a88740d31a94ddb5b1b68459dcb3e557b0c110d30b92e76c4@ec2-34-203-91-150.compute-1.amazonaws.com:5432/d24nenp2hf2vqp')