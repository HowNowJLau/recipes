from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user_model
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        recipes_list = []
        if results:
            for row in results:
                recipe_instance = cls(row)
                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['created_at'],
                    'updated_at' : row['updated_at']
                }
                user_instance = user_model.User(user_data)
                recipe_instance.maker = user_instance
                recipes_list.append(recipe_instance)
        return recipes_list

    @classmethod
    def get_one(cls, data):
        query = """
        SELECT * FROM recipes JOIN users ON recipes.user_id = users.id 
        WHERE recipes.id = %(id)s
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            row = results[0]
            recipe_instance = cls(row)
            user_data = {
                **row,
                'id' : row['users.id'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
            user_instance = user_model.User(user_data)
            recipe_instance.maker = user_instance
            return recipe_instance
        return False

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO recipes(name, description, instructions, date_cooked, under_30, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_30)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
        UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s,
        date_cooked = %(date)s, under_30 = %(under_30)s WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM recipes WHERE id = %(id)s
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validator(form_data):
        print(form_data)
        is_valid = True
        if len(form_data['name']) < 1:
            flash("Name required")
            is_valid = False
        if len(form_data['description']) < 1:
            flash("Description required")
            is_valid = False
        if len(form_data['instructions']) < 1:
            flash("Instructions required")
            is_valid = False
        if len(form_data['date']) < 1:
            flash("Date required")
            is_valid = False
        if "under_30" not in form_data:
            flash("Check Under 30 Yes or No")
            is_valid = False
        print(is_valid)
        return is_valid