from flask import render_template,redirect,request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 
from flask import flash


# main route
@app.route('/')
def index():
    return render_template('register_login.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect ('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/")

@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    return render_template('recipes.html', recipes= Recipe.get_all(),
                           user= User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
# 