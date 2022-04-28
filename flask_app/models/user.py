from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# PW_REGEX = re.compile(r'((?=.*\d)(?=.*[A-Z])(?=.*[a-z]){8,})')
PW_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$")
from flask import flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired
from flask_app.models import painting
import pprint

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.purchases = []
        self.this_purchase = data['this_purchase']

    @staticmethod
    def validate_register( user ):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('paintings').query_db(query,user)
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False 
        if len(user['first_name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Name must be at least 2 characters.")
            is_valid = False
        if len(results) > 1:
            flash("Email is already in use!")
            is_valid = False
        if not PW_REGEX.match(user['password']):
            flash('Bad Password!! Password must contain 8 characters and have one uppercase letter and one number.')
            is_valid = False
        if (user['password']) != (user['confirm']):
            flash("Name must be at least 2 characters.")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("paintings").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO users ( first_name , last_name, email, password, created_at , updated_at ) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(),NOW());"
        return connectToMySQL('paintings').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('paintings').query_db(query)
        # Create an empty list to append our instances of ninjas
        users = []
        # Iterate over the db results and create instances of ninjas with cls.
        for email in results:
            users.append( cls(email) )
        return users

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('paintings').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0]) 

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM emails WHERE id = %(id)s;"
        return connectToMySQL('paintings').query_db(query,data)

    # Gets users fav paintings and puts it into a list to be iterated on in dashboard
    @classmethod
    def get_purchases( cls , data):
        query = "SELECT * FROM users JOIN purchased ON users.id = purchased.user_id JOIN paintings ON paintings.id = purchased.painting_id WHERE users.id = %(id)s;"
        results = connectToMySQL('paintings').query_db( query , data)
        pprint.pprint(results, sort_dicts=False)
        
        purchases = []
        for row_from_db in results:
            
            painting_data = {
                "id" : row_from_db["paintings.id"],
                "name" : row_from_db["name"],
                "artist" : row_from_db["artist"],
                "description" : row_from_db["description"],
                "price" : row_from_db["price"],
                "quantity" : row_from_db["quantity"],
                "user_id" : row_from_db["user_id"],
                "created_at" : row_from_db["paintings.created_at"],
                "updated_at" : row_from_db["paintings.updated_at"]
            }
            new_purchase = painting.Painting(painting_data)
            print("New Purchase:", new_purchase)
            user_data = {
                "id": row_from_db['id'],
                "first_name": row_from_db['first_name'],
                "last_name": row_from_db['last_name'],
                "email": row_from_db['email'],
                "password" : row_from_db['password'],
                "created_at" : row_from_db['created_at'],
                "updated_at" : row_from_db['updated_at'],
                "this_purchase": new_purchase
            }

            print(user_data['this_purchase'])
            purchases.append( cls( user_data ) )
        print ("T**********", purchases)
        return purchases
    

    #add user's fav painting to association table
    @classmethod
    def make_purchase(cls,data):
        query = "INSERT INTO purchased (user_id,painting_id) VALUES (%(user_id)s,%(painting_id)s);"
        return connectToMySQL('paintings').query_db(query,data);

    @classmethod
    def update_quantity(cls, data):
        query = "UPDATE paintings SET quantity = %(quantity)s, updated_at = NOW() WHERE id = %(painting_id)s;"
        return connectToMySQL('paintings').query_db(query,data);
