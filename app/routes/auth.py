from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        new_user = User(name=name, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_name'] = user.name
            session['player_id'] = user.id
            session['players'] = [user.name]
            flash('Logged in successfully')
            return redirect(url_for('quiz.home'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')
    
@auth_bp.route('/logout')
def logout():
    session.pop('user_name', None)
    session.pop('player_id', None)
    session.pop('players', None)
    session.pop('questions_per_player', None)
    session.pop('current_player_index', None)
    flash('You have been logged out')
    return redirect(url_for('main.index'))
