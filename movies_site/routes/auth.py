from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import logging

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

# In-memory user store for demo purposes
users = {}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = users.get(email)
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = email
            return redirect(url_for('main.home'))
        flash('Invalid email or password')
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if email in users:
            flash('User already exists!')
            return render_template('auth/signup.html')
        users[email] = {'id': email, 'username': username, 'password': password}
        session['user_id'] = email
        session['username'] = username
        session['email'] = email
        return redirect(url_for('main.home'))
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.landing'))
