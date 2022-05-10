import jwt
from flask import make_response 
from pymongo import MongoClient
from DAL.from_db import * 
from BL.customers import *
from BL.products import *
from datetime import date
import os 
from bson import ObjectId


class PurchasesBL:
    def __init__(self):
        self.__access_db = DB_DAL()

    def get_num_of_purchases(self):
        purchases = self.__access_db.get_purchases()
        return sum(purchases)

    def new_purchase(self, purchase_params):
        if (purchase_params["productID"] and purchase_params["customerID"]):
            purchase = {
            "productID" : purchase_params["productID"],
            "customerID" : purchase_params["customerID"],
            "date" : str(date.today())
            }
            product = self.__access_db.get_one_product({"_id": ObjectId(purchase["productID"])})
            if int(product["quantity"]) > 0:
                temp = int(product["quantity"])
                temp -= 1
                product["quantity"] = str(temp)
                product = { 
                    "productID" : purchase_params["productID"],
                    "quantity" : product["quantity"],
                    "price" : product["price"],
                    "name" : product["name"]
                }
                self.__access_db.edit_product(product)
                status = self.__access_db.add_purchase(purchase)
            else:
                status = "Error - product is currently unavailable"
            return status

    def get_all_purchases(self):
        purchases = self.__access_db.get_purchases()
    # Mapping all the purchases to exclude PK ID
        mapped_purchases = list( map( lambda purchase : {"customerID" : purchase["customerID"], "productID" : purchase["productID"], "date" : purchase["date"]} ,purchases ) )
        return mapped_purchases

    def search(self, search_request):
    # Mapping all the purchases to exclude PK ID
        mapped_purchases = list( map( lambda purchase : {"customerID" : purchase["customerID"], "productID" : purchase["productID"], "date" : purchase["date"]} ,self.__access_db.get_purchases() ) )
    # check if there are more then 3 keys - protect server from "flooding"\overloading - processing 
    # unneccecary requests
        if len(search_request.keys()) > 3:
            return []

    # server side filtering empty valus in the JSON - so client could send empty valued syntanx of JSONs
        obj = { key: val for key, val in search_request.items() if val }
        keys = list(obj.keys())

    # checking by the number of filters(Keys.) to search by - using HOF filter to match data from client
    # to the DB's
        if len(keys) == 1:
            filtered_purchases = list( filter(lambda purchase: obj[keys[0]] == purchase[keys[0]], mapped_purchases) )

        elif len(keys) == 2:  
            filtered_purchases = list( filter(lambda purchase: obj[keys[0]] == purchase[keys[0]] and obj[keys[1]] == purchase[keys[1]], mapped_purchases) )

        elif len(keys) == 3:
            filtered_purchases = list( filter(lambda purchase: obj[keys[0]] == purchase[keys[0]] and obj[keys[1]] == purchase[keys[1]] and obj[keys[2]] == purchase[keys[2]], mapped_purchases) )
        else:
    # if the request is empty - send all purchases data insted (as req by instructions to the project)
            arr = []
            for purchase in mapped_purchases:
                customer = self.__access_db.get_one_customer({"_id": ObjectId(purchase["customerID"])})
                product = self.__access_db.get_one_product({"_id": ObjectId(purchase["productID"])})
                purchase = {
                "date" : purchase["date"],
                "productID" : purchase["productID"],
                "customerID" : purchase["customerID"],
                "name" : product["name"],
                "price" : product["price"],
                "quantity" : product["quantity"],
                "firstname" : customer["firstname"],
                "lastname" : customer["lastname"],
                "city" : customer["city"]
                }
                arr.append(purchase)
            return arr

    # final loop to compile data into one array of JSONs
        arr = []
        for purchase in filtered_purchases:
            customer = self.__access_db.get_one_customer({"_id": ObjectId(purchase["customerID"])})
            product = self.__access_db.get_one_product({"_id": ObjectId(purchase["productID"])})
            purchase = {
            "date" : purchase["date"],
            "productID" : purchase["productID"],
            "customerID" : purchase["customerID"],
            "name" : product["name"],
            "price" : product["price"],
            "quantity" : product["quantity"],
            "firstname" : customer["firstname"],
            "lastname" : customer["lastname"],
            "city" : customer["city"]
            }
            arr.append(purchase)
        return arr