from firebase_admin import auth
from functools import wraps
from flask import session, redirect, url_for, jsonify
import logging

logger = logging.getLogger(__name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please login to access this feature',
                'code': 401
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def verify_user(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token['uid']
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        return None
