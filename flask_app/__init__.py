from flask import Flask
app = Flask(__name__)
app.secret_key = "Nothing to see here"
DATABASE = "recipe_schema"