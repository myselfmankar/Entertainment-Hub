from datetime import datetime
from firebase_util import get_firestore_client, initialize_firebase
import firebase_admin

class Favorite:
    def __init__(self, user_id, item_id, title, poster_path, media_type):
        self.user_id = user_id
        self.item_id = item_id
        self.title = title
        self.poster_path = poster_path
        self.media_type = media_type
        self.created_at = datetime.now()

    @staticmethod
    def get_collection():
        if not firebase_admin._apps:  # Ensure Firebase is initialized
            initialize_firebase()
        db = get_firestore_client()
        return db.collection('favorites')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'item_id': self.item_id,
            'title': self.title,
            'poster_path': self.poster_path,
            'media_type': self.media_type,
            'created_at': self.created_at
        }

    @staticmethod
    def from_dict(data):
        favorite = Favorite(
            data.get('user_id'),
            data.get('item_id'),
            data.get('title'),
            data.get('poster_path'),
            data.get('media_type')
        )
        favorite.created_at = data.get('created_at')
        return favorite
