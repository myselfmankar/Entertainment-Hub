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