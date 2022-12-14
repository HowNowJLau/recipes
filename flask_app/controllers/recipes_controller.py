from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_app import app

@app.route('/recipes/new')
def new_recipe():
    return render_template("new_recipe.html")

@app.route('/recipes/create', methods=["POST"])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect('/recipes/new')
    recipe_data = {
        **request.form,
        'user_id' : session['user_id']
    }
    Recipe.create(recipe_data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>/view')
def view_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id' : id}
    one_recipe = Recipe.get_one(data)
    user_data = {'id' : session['user_id']}
    logged_user =  User.get_by_id(user_data)
    return render_template("view_recipe.html", logged_user=logged_user, one_recipe=one_recipe)

@app.route('/recipes/<int:id>/edit')
def edit_recipe_form(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id' : id}
    one_recipe = Recipe.get_one(data)
    return render_template("edit_recipe.html", one_recipe=one_recipe)

@app.route('/recipes/<int:id>/update', methods=["POST"])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect(f'/recipes/{id}/edit')
    data = {
        **request.form,
        'id' : id
    }
    Recipe.update(data)
    return redirect('/recipes')

@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {'id':id}
    this_recipe = Recipe.get_one(data)
    if not this_recipe.user_id == session['user_id']:
        flash("Nice try")
        return redirect('/recipes')
    Recipe.delete(data)
    return redirect('/recipes')
