from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Painting:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.artist = data['artist']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data):
        query = "INSERT INTO paintings (name ,description, artist, price, quantity, user_id) VALUES (%(name)s,%(description)s,%(artist)s,%(price)s,%(quantity)s,%(user_id)s);"
        return connectToMySQL('paintings').query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET name = %(name)s, description = %(description)s, artist = %(artist)s, price = %(price)s, quantity = %(quantity)s,user_id = %(user_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('paintings').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings;"
        results = connectToMySQL('paintings').query_db(query)
        # Create an empty list to append our instances of paintings
        paintings = []
        # Iterate over the db results and create instances of paintings with cls.
        for painting in results:
            paintings.append( cls(painting) )
        return paintings

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        results = connectToMySQL('paintings').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0]) 

    @classmethod
    def delete(cls, id):
        query  = f"DELETE FROM paintings WHERE id = {id};"
        return connectToMySQL('paintings').query_db(query)

    @staticmethod
    def validate_painting( painting ):
        is_valid = True
        # test whether a field matches the pattern
        if len(painting['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False
        if len(painting['description']) < 10:
            flash("Description must be at least 10 characters.")
            is_valid = False
        if int(painting['price']) < 1:
            flash("Price must be more than $0.")
            is_valid = False


        return is_valid