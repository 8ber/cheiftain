import jwt
from flask import make_response 
from pymongo import MongoClient
from DAL.from_db import * 
from BL.purchases import *
from BL.products import *
from datetime import date
import os 

class CustomersBL:
    def __init__(self):
        self.__access_db = DB_DAL()

    def get_all_customers(self):
        all_customers = self.__access_db.get_customers()
        arr = []
        for customer in all_customers:
            customer = { "firstname" : customer["firstname"], "lastname" : customer["lastname"], "city" : customer["city"], "customerID" : str(customer["_id"]) }
            arr.append(customer)
        return arr

    def edit_customer(self, obj_to_edit):
        customer_exist = self.__access_db.get_one_customer({"_id": ObjectId(obj_to_edit["customerID"])})
        if customer_exist:
            send_to_edit = self.__access_db.edit_customer(obj_to_edit)
            if send_to_edit:
                return "OK"
        else:
            return make_response("Error", 401)


    def del_customer(self, id):
        customer_id = {"_id": ObjectId(id)}
        status = self.__access_db.del_customer(customer_id)
        if status:
            all_purchases = self.__access_db.get_purchases()
            for purchase in all_purchases:
                if id == purchase["customerID"]:
                    print(purchase["_id"])
                    self.__access_db.del_purchase({"_id": purchase["_id"]})
                    return status

    # def get_one_customer(self, obj):
    #     customer = self.__access_db.get_one_customer()

