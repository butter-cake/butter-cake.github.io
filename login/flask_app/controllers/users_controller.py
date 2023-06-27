from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/login')
def loginpage():

    return render_template('/login.html')

@app.route('/loginuser', methods=['POST'])
def loginuser():

    login_data  = {'email': request.form['email']}
    user_in_db = User.GetUserByEmail(login_data)
    print("hello:", user_in_db.password, request.form['password'])

    if not user_in_db:
        flash('Invalid Email/Password')
        return redirect('/login')

    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password')
        return redirect('/login')

    session['user_id'] = user_in_db.id
    return redirect(f'/success/{user_in_db.id}')

@app.route('/register_user', methods=['POST'])
def successful_register():

    if not User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    newUser_data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password': pw_hash
    }
    user_id = User.CreateUser(newUser_data)
    session['user_id'] = user_id
    return redirect(f'/success/{user_id}')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/success/<int:user_id>')
def show_success(user_id):

    if 'user_id' not in session:
        return redirect('/')
    newUser = User.GetUserById({'user_id': user_id})

    return render_template('success.html', newUser = newUser)