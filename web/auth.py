from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, request
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return {'status': 'success', 'message': 'Login berhasil'}
                #return redirect(url_for('views.home'))

            else:
                flash('Incorrect password, try again.', category='error')
                return {'status': 'error', 'message': 'Incorrect password'}
        else:
            flash('Email does not exist.', category='error')
            return {'status': 'error', 'message': 'Email does not exist.'}
    
    #return render_template("login.html", user=current_user)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return {'status': 'success', 'message': 'Logout berhasil'}


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
            return {'status': 'error', 'message': 'Email already exists.'}
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            return {'status': 'error', 'message': 'Email must be greater than 3 characters.'}
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
            return {'status': 'error', 'message': 'First name must be greater than 1 character.'}
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
            return {'status': 'error', 'message': 'Passwords don\'t match.'}
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
            return {'status': 'error', 'message': 'Password must be at least 7 characters.'}
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return {'status': 'success', 'message': 'Registrasi Berhasil'}

    #return render_template("sign_up.html", user=current_user)

