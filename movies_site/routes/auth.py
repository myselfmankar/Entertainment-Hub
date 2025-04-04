from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
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

@auth_bp.route('/google_sign_in', methods=['POST'])
def google_sign_in_route():
    try:
        id_token = request.json.get('id_token')
        if not id_token:
            raise ValueError("No ID token provided")
        # Verify the token
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        email = decoded_token.get('email')
        session['user_id'] = user_id
        session['email'] = email
        
        return jsonify({
            'success': True,
            'message': 'Google sign-in successful'
        })
    except Exception as e:
        logger.error(f"Google sign-in error: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password_route():
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            reset_link = reset_password(email)
            flash(f"Password reset link sent to {email}.")
        except Exception as e:
            flash(f"Error: {str(e)}")
    return render_template('auth/reset_password.html', firebase_config=current_app.config['FIREBASE_CONFIG'])
