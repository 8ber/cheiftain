import jwt
from flask import make_response 
from pymongo import MongoClient
from datetime import datetime, timedelta
import os 
from DAL.from_db import * 
from bson import ObjectId
    
class AuthBL:
    def __init__(self):
        self.__access_db = DB_DAL()
        self.__key = "Arafat"
        self.__algorithm = "HS256"
 
    def __check_user(self, username, password):
        #  check if user exists in DB users collection -> return unique value
        query = { "username" : username,
                  "password" : password }
        user_found = self.__access_db.get_one_user(query)
        if user_found:
            return user_found
        else: return None

    def get_token(self, username, password):
        user = self.__check_user(username ,password)
        if user is not None:
            token = jwt.encode({"_id" : str(user["_id"]), "exp" : datetime.utcnow() + timedelta(minutes=5) }, self.__key, self.__algorithm )
            return make_response({ "token" : token}, 200)
        else:
            return make_response({"error" : "Login attempt failed." }, 401)

    def verify_token(self, request):
        if request.headers and request.headers.get("x-access-token"):
            token = request.headers.get("x-access-token")
            try:
                data = jwt.decode(token, self.__key, self.__algorithm)
                user_found = self.__access_db.get_one_user({ "_id" : ObjectId(data["_id"]) })
                print(user_found)
                if user_found["rank"] == "user":
                    return "user"
                elif user_found["rank"] == "admin":
                    return "admin"
            except: 
                return False
        else:
            return False    