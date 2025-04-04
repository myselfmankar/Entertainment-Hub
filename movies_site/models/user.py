from datetime import datetime

class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
        self.profile_picture = None
        self.created_at = datetime.now()

class Review:
    def __init__(self, user_id, media_id, content, rating):
        self.user_id = user_id
        self.media_id = media_id
        self.content = content
        self.rating = rating
        self.created_at = datetime.now()
