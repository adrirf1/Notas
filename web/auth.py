from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Login incorrecto", category='error')
        else:
            flash("No existe el usuario",category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('pass1')
        password2 = request.form.get('pass2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('email ya existe',category='error')

        if password1 != password2:
            flash('Password does not match', category='error')
        else:
            hashed_password = generate_password_hash(password1)
            nuevoUser = User(email=email,name=name,password=hashed_password)
            db.session.add(nuevoUser)
            db.session.commit()
            login_user(user,remember=True)
            flash("Account Created",category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)