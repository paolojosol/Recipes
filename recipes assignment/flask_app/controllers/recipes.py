from operator import methodcaller
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask import Flask, get_flashed_messages, redirect, session, render_template, request, flash


@app.route('/recipes/new')
def new_recipe():
    return render_template('new_recipe.html', messages = get_flashed_messages())

@app.route('/recipes/create', methods = ['post'])
def create_recipe():
    if Recipe.is_valid(request.form):
        r = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'made': request.form['made'],
            'under_30': request.form['under_30'],
            'user_id': session['user_id']
        }
        Recipe.create(r)
        return redirect('/home')
    return redirect('/recipes/new')

@app.route('/recipes/<int:id>')
def show_recipe(id):
    recipe = Recipe.get_by_id({'id': id})
    return render_template('show_recipe.html', recipe = recipe, user = User.get_by_id({'id': recipe.user_id}))

@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    recipe = Recipe.get_by_id({'id': id})
    return render_template('edit_recipe.html', user = User.get_by_id({'id': recipe.user_id}), recipe = recipe, messages = get_flashed_messages())

@app.route('/recipes/update/<int:id>', methods=['post'])
def update_recipe(id):
    if Recipe.is_valid(request.form):
        r = {
            'id': id,
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'made': request.form['made'],
            'under_30': request.form['under_30'],
            'user_id': session['user_id']
        }
        Recipe.update_by_id(r)
        return redirect('/home')
    return redirect('/recipes/edit/'+str(id))

@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    Recipe.delete({'id': id})
    return redirect('/home')