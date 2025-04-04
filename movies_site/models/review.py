from datetime import datetime
from firebase_util import get_firestore_client, initialize_firebase
import firebase_admin

db = get_firestore_client()

class Review:
    def __init__(self, user_id, media_id, content, rating):
        self.user_id = user_id
        self.media_id = media_id
        self.content = content
        self.rating = rating
        self.created_at = datetime.now()

    @staticmethod
    def get_collection():
        if not firebase_admin._apps:  # Ensure Firebase is initialized
            initialize_firebase()
        db = get_firestore_client()
        return db.collection('reviews')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'media_id': self.media_id,
            'content': self.content,
            'rating': self.rating,
            'created_at': self.created_at
        }
