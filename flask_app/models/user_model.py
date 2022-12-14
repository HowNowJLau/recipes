from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO users(first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM users WHERE id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users WHERE email = %(email)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['first_name']) < 3:
            flash("First name must be at least 2 characters long", "reg")
            is_valid = False
        elif not form_data['first_name'].isalpha():
            flash("First name may only contain letters", "reg")
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash("Last name must be at least 2 characters long", "reg")
            is_valid = False
        elif not form_data['last_name'].isalpha():
            flash("Last name may only contain letters", "reg")
            is_valid = False
        if len(form_data['email']) < 1:
            flash("Email required", "reg")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data['email']):
            flash("Invalid email format", "reg")
            is_valid = False
        else:
            data = {'email':form_data['email']}
            potential_user = User.get_by_email(data)
            if potential_user:
                flash("Email has been previously registered", "reg")
                is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters long", "reg")
            is_valid = False
        elif not form_data['password'] == form_data['conf_pass']:
            flash("Passwords must match", "reg")
            is_valid = False
        return is_valid
        
        