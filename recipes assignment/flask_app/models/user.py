from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_app.models import recipe

EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

class User:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        user_list= []
        for dict in results:
            user_list.append(cls(dict))
        return user_list

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) <= 0:
            return False
        return cls(results[0])

    @classmethod
    def update_by_id(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)
        return

    @staticmethod
    def is_valid(user_data):
        is_valid = True
        all_users = User.get_all_users()
        if user_data['password'] != user_data['confirm_pass']:
            flash('Password do not match.')
            is_valid = False
        if not EMAIL_REGEX.match(user_data['email']):
            flash('Please enter a valid email.')
            is_valid = False
        if len(user_data['first_name']) < 2:
            flash('First name must be at least 2 characters long.')
            is_valid = False
        if len(user_data['last_name']) < 2:
            flash('Last name must be at least 2 characters long.')
            is_valid = False
        if len(user_data['password']) < 8:
            flash('Password must be at least 8 characters long.')
            is_valid = False
        if not EMAIL_REGEX.match(user_data['email']):
            flash('Email must be valid.')
            is_valid = False
        for user in all_users:
            if user.email == user_data['email']:
                flash("A user with that email already exists")
                is_valid = False
        return is_valid
