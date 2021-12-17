from flask_cors import CORS, cross_origin
import data_vine.functions as dv
from flask import Flask, request, Response, jsonify
from flask_cors import core
from flask_cors.extension import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug import *
from sqlalchemy.inspection import inspect
from deltah2h import *


app = Flask(__name__)
cors = CORS(app)

# order routes


@app.route('/order', methods=['GET'])
@cross_origin
def get_order():
    return jsonify({'Orders': ordertable.get_all_orders()})


@app.route('/order/<int:id>', methods=['GET'])
@cross_origin
def get_order_by_id(id):
    return_value = ordertable.get_order(id)
    return jsonify(return_value)


@app.route('/order', methods=['POST'])
@cross_origin
def add_order():
    request_data = request.get_json()
    ordertable.add_order(request_data["userid"], request_data["status"],
                         request_data["subtotal"], request_data["discount"], request_data["tax"], request_data["grandtotal"], request_data["description"])
    response = Response("Order added", 201, mimetype='application/json')
    return response


@app.route('/order/<int:id>', methods=['PUT'])
@cross_origin
def update_order(id):

    request_data = request.get_json()
    ordertable.update_order(id, request_data["userid"], request_data["status"],
                            request_data["subtotal"], request_data["discount"], request_data["tax"], request_data["grandtotal"], request_data["description"])
    response = Response("Order Updated", status=200,
                        mimetype='application/json')
    return response


@app.route('/order/<int:id>', methods=['DELETE'])
@cross_origin
def remove_order(id):

    ordertable.delete_order(id)
    response = Response("Order Deleted", status=200,
                        mimetype='application/json')
    return response


# user routes
@app.route('/user', methods=['GET'])
@cross_origin
def get_user():
    return jsonify({'users': usertable.get_all_users()})


@app.route('/user/<int:userid>', methods=['GET'])
@cross_origin
def get_user_by_id(userid):
    return_value = usertable.get_user(userid)
    return jsonify(return_value)


@app.route('/user', methods=['POST'])
@cross_origin
def add_user():
    request_data = request.get_json()
    usertable.add_user(
        request_data["username"], request_data["contactno"], request_data["email"])
    response = Response("user added", 201, mimetype='application/json')
    return response


@app.route('/user/<int:userid>', methods=['PUT'])
@cross_origin
def update_user(userid):

    request_data = request.get_json()
    usertable.update_user(userid, request_data["username"],
                          request_data["contactno"], request_data["email"])
    response = Response("user Updated", status=200,
                        mimetype='application/json')
    return response


@app.route('/user/<int:userid>', methods=['DELETE'])
@cross_origin
def remove_user(userid):

    usertable.delete_user(userid)
    response = Response("user Deleted", status=200,
                        mimetype='application/json')
    return response


# product routes
@app.route('/product', methods=['GET'])
@cross_origin
def get_product():
    return jsonify({'Products': producttable.get_all_products()})


@app.route('/product/<int:productid>', methods=['GET'])
@cross_origin
def get_product_by_id(productid):
    return_value = producttable.get_product(productid)
    return jsonify(return_value)


@app.route('/product', methods=['POST'])
@cross_origin
def add_product():
    request_data = request.get_json()
    producttable.add_product(request_data["productname"], request_data["price"],
                             request_data["quantity"], request_data["description"], request_data["supplierid"])
    response = Response("Product added", 201, mimetype='application/json')

    return response


@app.route('/product/<int:productid>', methods=['PUT'])
@cross_origin
def update_product(productid):

    request_data = request.get_json()
    producttable.update_product(productid, request_data["productname"], request_data["price"],
                                request_data["quantity"], request_data["description"], request_data["supplierid"])
    response = Response("Product Updated", status=200,
                        mimetype='application/json')
    return response


@app.route('/product/<int:productid>', methods=['DELETE'])
@cross_origin
def remove_product(productid):

    producttable.delete_product(productid)
    response = Response("Product Deleted", status=200,
                        mimetype='application/json')
    return response


# supplier routes
@app.route('/supplier', methods=['GET'])
@cross_origin
def get_supplier():
    return jsonify({'Suppliers': suppliertable.get_all_suppliers()})


@app.route('/supplier/<int:supplierid>', methods=['GET'])
@cross_origin
def get_supplier_by_id(supplierid):
    return_value = suppliertable.get_supplier(supplierid)
    return jsonify(return_value)


@app.route('/supplier', methods=['POST'])
@cross_origin
def add_supplier():
    request_data = request.get_json()
    suppliertable.add_supplier(
        request_data["suppliername"], request_data["description"], request_data["contactno"], request_data["email"])
    response = Response("supplier Added", 201, mimetype='application/json')
    return response


@app.route('/supplier/<int:supplierid>', methods=['PUT'])
@cross_origin
def update_supplier(supplierid):

    request_data = request.get_json()
    suppliertable.update_supplier(
        supplierid, request_data["suppliername"], request_data["description"], request_data["contactno"], request_data["email"])
    response = Response("Supplier Updated", status=200,
                        mimetype='application/json')
    return response


@app.route('/supplier/<int:supplierid>', methods=['DELETE'])
@cross_origin
def remove_supplier(supplierid):

    suppliertable.delete_supplier(supplierid)
    response = Response("supplier Deleted", status=200,
                        mimetype='application/json')
    return response


if __name__ == '__main__':
    db.create_all()
    dv.createAvsc("order", formatdb('order'))
    dv.createAvsc("product", formatdb('product'))
    dv.createAvsc("user", formatdb('user'))
    dv.createAvsc("supplier", formatdb('supplier'))
    app.run()
