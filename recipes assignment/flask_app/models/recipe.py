from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.made = data['made']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under_30, made, user_id) VALUES (%(name)s, %(description)s,%(instructions)s,%(under_30)s,%(made)s ,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_by_id(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, made = %(made)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        recipe_list= []
        for dict in results:
            recipe_list.append(cls(dict))
        return recipe_list    

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @staticmethod
    def is_valid(r_data):
        is_valid = True
        if len(r_data['name']) < 3:
            flash('Recipe name must be 3 or more characters long.')
            is_valid = False
        if len(r_data['description']) < 3:
            flash('Recipe description must be 3 or more characters long.')
            is_valid = False
        if len(r_data['instructions']) < 3:
            flash('Recipe instructions must be 3 or more characters long.')
            is_valid = False
        return is_valid

        