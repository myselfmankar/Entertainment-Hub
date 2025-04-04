import firebase_admin
from firebase_admin import credentials, firestore, auth
import config
import logging

logger = logging.getLogger(__name__)

def initialize_firebase():
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            logger.debug("Initializing Firebase Admin SDK...")
            cred = credentials.Certificate(config.FIREBASE_ADMIN_CONFIG)
            firebase_admin.initialize_app(cred)
            logger.debug("Firebase Admin SDK initialized successfully")
        else:
            logger.debug("Firebase Admin SDK already initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        raise

def get_firestore_client():
    if not firebase_admin._apps:
        raise ValueError("Firebase has not been initialized. Call initialize_firebase() first.")
    return firestore.client()

def google_sign_in(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token['uid']
        return user_id
    except Exception as e:
        logger.error(f"Google sign-in failed: {str(e)}")
        raise

def reset_password(email):
    try:
        link = auth.generate_password_reset_link(email)
        logger.debug(f"Password reset link generated: {link}")
        return link
    except Exception as e:
        logger.error(f"Failed to generate password reset link: {str(e)}")
        raise
