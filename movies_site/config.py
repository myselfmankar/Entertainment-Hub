from dotenv import load_dotenv
import os
load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
DEFAULT_POSTER = "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=500&q=80"
DEFAULT_VIDEO = "https://www.youtube.com/embed/dQw4w9WgXcQ"

CATEGORY_NAMES = {
    'all': 'Trending Entertainment',
    'movie': 'Trending Movies',
    'tv': 'Trending TV Shows',
    'anime': 'Trending Anime'
}

# API URLs
TMDB_SEARCH_URL = 'https://api.themoviedb.org/3/search/multi'
TMDB_TRENDING_URL = 'https://api.themoviedb.org/3/trending/all/day'
TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p/w500'
TMDB_DETAIL_URL = 'https://api.themoviedb.org/3/{type}/{id}'
TMDB_GENRES_URL = 'https://api.themoviedb.org/3/genre/movie/list'
TMDB_WATCH_PROVIDERS_URL = 'https://api.themoviedb.org/3/{type}/{id}/watch/providers'

# Firebase Web Config
FIREBASE_CONFIG = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID')
}

# Firebase Admin SDK credentials
FIREBASE_ADMIN_CONFIG = {
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
}