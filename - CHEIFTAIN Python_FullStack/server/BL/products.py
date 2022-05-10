import jwt
from flask import make_response 
from pymongo import MongoClient
from DAL.from_db import * 
from BL.customers import *
from BL.purchases import *
from datetime import date
import os 

class ProductsBL:
    def __init__(self):
        self.__access_db = DB_DAL()

 
    def get_all_products(self):
        all_prods = self.__access_db.get_prods()
        arr = []
        for product in all_prods:
            product = { "name" : product["name"], "price" : product["price"], "quantity" : product["quantity"], "productID" : str(product["_id"]) }
            arr.append(product)
        return arr

    def edit_product(self, obj_to_edit):
        product_exist = self.__access_db.get_one_product({"_id": ObjectId(obj_to_edit["productID"])})
        if product_exist:
                send_to_edit = self.__access_db.edit_product(obj_to_edit)
                if send_to_edit:
                    return "OK"
        else:
            return make_response("Error", 401)


    def del_product(self, id):
        status = self.__access_db.del_product({"_id": ObjectId(id)})
        if status:
            all_purchases = self.__access_db.get_purchases()
            for purchase in all_purchases:
                if id == purchase["productID"]:
                    print(purchase["_id"])
                    self.__access_db.del_purchase({"_id": purchase["_id"]})
                    return status
        # API_users = self.__users_from_api.get_all_users()
        # mapped = list(map(lambda user : {"name" : user["name"] , "email" : user["email"]},API_users[0:3]))
        # is_found_in_API = list(filter(lambda user : user["name"] == name and user["email"] == email, mapped))
        # if is_found_in_API:
        #     is_user_in_DB = self.__users_from_DB.get_user({ "fullname" : is_found_in_API[0]["name"] })
        #     if is_user_in_DB:
        #         name_actions_id = { "name" : is_user_in_DB["fullname"], "numofactions" : is_user_in_DB["numofactions"], "id" : is_user_in_DB["externalid"] }
        #         return name_actions_id
       
