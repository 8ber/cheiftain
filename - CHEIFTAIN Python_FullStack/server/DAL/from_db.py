from pymongo import MongoClient
from bson import ObjectId

class DB_DAL:
    def __init__(self):
        self.__client = MongoClient(port=27017)
        self.__db = self.__client["chief"] 
# users:
    def get_one_user(self, obj):
        return self.__db["users"].find_one(obj)


# products:

    def get_prods(self):
        data = self.__db["products"].find({})
        return data

    def edit_product(self, obj_to_edit):
        obj_shaped = {
        "name" : obj_to_edit["name"],
        "price" : obj_to_edit["price"],
        "quantity" : obj_to_edit["quantity"]
        }
        self.__db["products"].update_one({"_id": ObjectId(obj_to_edit["productID"])}, {"$set": obj_shaped})
        return "OK"

    def get_one_product(self, obj):
        return self.__db["products"].find_one(obj)

    def del_product(self, prod_to_del):
        self.__db["products"].delete_one(prod_to_del)
        return "OK"

# purchases:

    def get_purchases(self):
        data = self.__db["purchases"].find({})
        return data

    def add_purchase(self, obj):
        self.__db["purchases"].insert_one(obj)
        return "OK"

    def del_purchase(self, purchase_to_del):
        data = self.__db["purchases"].delete_one(purchase_to_del)
        return "OK"

# costumers:

    def get_customers(self):
        data = self.__db["customers"].find({})
        return data

    def get_one_customer(self, obj):
        return self.__db["customers"].find_one(obj)

    def edit_customer(self, obj_to_edit):
        obj_shaped = {
        "firstname" : obj_to_edit["firstname"],
        "lastname" : obj_to_edit["lastname"],
        "city" : obj_to_edit["city"]
        }
        self.__db["customers"].update_one({"_id": ObjectId(obj_to_edit["customerID"])}, {"$set": obj_shaped})
        return "OK"

    def del_customer(self, customer_to_del):
        self.__db["customers"].delete_one(customer_to_del)
        return "OK"