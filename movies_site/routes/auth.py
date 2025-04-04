from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, current_app
from firebase_admin import auth
import logging
from firebase_util import google_sign_in, reset_password

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')

        try:
            # Verify with Firebase Auth
            user = auth.get_user_by_email(email)
            # Here you should actually verify the password with Firebase
            # This is just a placeholder
            session['user_id'] = user.uid
            session['email'] = email
            
            if request.is_json:
                return jsonify({'success': True})
            return redirect(url_for('main.home'))
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            if request.is_json:
                return jsonify({
                    'success': False, 
                    'message': 'Invalid email or password'
                })
            flash('Invalid email or password')
            
    return render_template('auth/login.html', 
                         firebase_config=current_app.config['FIREBASE_CONFIG'])

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # Create user with username as part of email
            user = auth.create_user(
                email=f"{username}@example.com",
                password=password
            )
            session['user_id'] = user.uid
            session['username'] = username
            return redirect(url_for('main.home'))
        except Exception as e:
            logger.error(f"Signup error: {str(e)}")
            flash('Error creating account')
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

        # Store user info in session
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
    return render_template('auth/reset_password.html)', firebase_config=current_app.config['FIREBASE_CONFIG'])
