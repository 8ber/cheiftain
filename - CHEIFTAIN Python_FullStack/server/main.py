#Importing relevant modules 
from flask import Flask, jsonify, request
from flask_cors import CORS 
import json
from BL.products import *
from BL.purchases import *
from BL.customers import *
from BL.auth import *
from bson import ObjectId 

#Creating an app to run a flask server with the file name 
app = Flask(__name__)

#Opening the app for Cross-Origin Resource Sharing
CORS(app)

#Creating instances for the BL classes
authBL = AuthBL()
productsBL = ProductsBL()
purchasesBL = PurchasesBL()
customersBL = CustomersBL()

#creating routes on the API server
@app.route('/login', methods=['POST'])
def login():
    username = request.json["username"]
    password = request.json["password"]
    token = authBL.get_token(username, password)
    return token #no jsonify - "make_response" makes it a json

@app.route('/products', methods=['GET'])
def products():
    if authBL.verify_token(request):
        prods = productsBL.get_all_products()
        return jsonify(prods)
    else: 
        return make_response({"Error" : "Authorization required." }, 401)

@app.route('/customers', methods=['GET'])
def customers():
    if authBL.verify_token(request):
        customers_all = customersBL.get_all_customers()
        return jsonify(customers_all)
    else: 
        return make_response({"Error" : "Authorization required." }, 401)

@app.route('/search', methods=['POST'])
def search():
    if authBL.verify_token(request):
        search_params = request.json
        data = purchasesBL.search(search_params)
        return jsonify(data)
    else: 
        return make_response({"Error" : "Authorization required." }, 401)

@app.route('/new_purchase', methods=['POST'])
def new_purchase():
    if authBL.verify_token(request):
        purchase_params = request.json
        data = purchasesBL.new_purchase(purchase_params)
        return jsonify(data)
    else: 
        return make_response({"Error" : "Authorization required." }, 401)

@app.route('/purchases', methods=['GET'])
def purchases():
    if authBL.verify_token(request):
        all_purchases = purchasesBL.get_all_purchases()
        return jsonify(all_purchases)
    else: 
        return make_response({"Error" : "Authorization required." }, 401)

    #----------[ restricted for admins only: ]----------------
@app.route('/edit_product', methods=['PUT'])
def edit_product():
    auth_res = authBL.verify_token(request)
    if auth_res == "admin":
        new_data = request.json
        status = productsBL.edit_product(new_data)
        return jsonify(status)
    elif auth_res == "user":
        return make_response({"Error" : "Administration privileges required." }, 401)
    else: 
        return make_response({"Error" : "Authorization required." }, 401)

@app.route('/del_product/<string:id>', methods=['DELETE'])
def del_product(id):
    auth_res = authBL.verify_token(request)
    if auth_res == "admin":
        status = productsBL.del_product(id)
        return jsonify(status)
    elif auth_res == "user":
        return make_response({"Error" : "Administration privileges required." }, 401)
    else: 
        return make_response({"Error" : "Authorization required." }, 401)

@app.route('/edit_customer', methods=['PUT'])
def edit_customer():
    auth_res = authBL.verify_token(request)
    if auth_res == "admin":
        new_data = request.json
        status = customersBL.edit_customer(new_data)
        return jsonify(status)
    elif auth_res == "user":
        return make_response({"Error" : "Administration privileges required." }, 401)
    else: 
        return make_response({"Error" : "Authorization required." }, 401)

@app.route('/del_customer/<string:id>', methods=['DELETE'])
def del_customer(id):
    auth_res = authBL.verify_token(request)
    if auth_res == "admin":
        status = customersBL.del_customer(id)
        return jsonify(status)
    elif auth_res == "user":
        return make_response({"Error" : "Administration privileges required." }, 401)
    else: 
        return make_response({"Error" : "Authorization required." }, 401)

# @app.route('/total_purchases', methods=['GET'])
# def total_purchases():
#     total_purchases = purchasesBL.get_num_of_purchases()
#     return jsonify(total_purchases) #num of purchases SERVERSIDE

#running the server/app I've defined
app.run(debug=True)