from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    DB = 'recipe_schema'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.under30 = data['under30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def save(cls,data):
        query = """INSERT INTO recipes (name, under30, description, instructions, date_made, user_id) 
                VALUES (%(name)s, %(under30)s, %(description)s, %(instructions)s, %(date_made)s, %(user_id)s);"""
        return connectToMySQL(cls.DB).query_db(query,data)
    

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(cls.DB).query_db(query)
        all_recipes = []

        for row in results:
            all_recipes.append(cls(row))
        return all_recipes
    

    @classmethod
    def get_one(cls,data):
        query = """SELECT * FROM recipes LEFT JOIN users
        ON recipes.id = recipes.user_id WHERE recipes.id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0])

    
    @classmethod
    def update(cls,data):
        query = """UPDATE recipes SET name=%(name)s, under30=%(under30)s, description=%(description)s, instructions=%(instructions)s, 
        namdate_made=%(namdate_made)s WHERE id = %(id)s;"""
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @staticmethod
    def validate_recipe( recipe ):
        is_valid = True
        if len(recipe['name']) < 2:
            is_valid = False
            flash('Name is too short')
        if len(recipe['instructions']) < 2:
            is_valid = False
            flash('instructions is too short')
        if len(recipe['description']) < 2:
            is_valid = False
            flash('description is too short')
        if recipe['date_made'] == '':
            is_valid = False
            flash('Please enter a date')
        return is_valid
        
