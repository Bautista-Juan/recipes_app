from flask import render_template,redirect,request, session

from flask_app.models.recipe import Recipe
from flask_app.models.user import User

from flask_app import app

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id'],
    }
    return render_template('new_recipe.html', user=User.get_by_id(data))


@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under30': int(request.form['under30']),
        'date_made': request.form['date_made'],
        'user_id': session['user_id']
    }
    Recipe.save(data)
    return redirect('/dashboard')


@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    user_data = {
        'id': session['user_id'],
        'first_name': session['first_name']
    }

    return render_template('edit_recipe.html', edit=Recipe.get_one(data),
                           user=User.get_by_id(user_data)) 


@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under30': int(request.form['under30']),
        'date_made': request.form['date_made'],
        'user_id': session['user_id']
    }
    Recipe.update(data) 
    return redirect('/dashboard')


@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('view_recipe.html', recipe=Recipe.get_one(data), 
                           user=User.get_by_id(user_data))


@app.route('/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Recipe.delete(data) 
    return redirect('/dashboard')

