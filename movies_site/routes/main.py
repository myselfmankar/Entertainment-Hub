from flask import Blueprint, render_template, request, jsonify
import requests
import logging
from config import (
    TMDB_API_KEY, TMDB_TRENDING_URL, TMDB_IMAGE_BASE, 
    DEFAULT_POSTER, CATEGORY_NAMES, TMDB_SEARCH_URL
)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

main_bp = Blueprint('main', __name__, url_prefix='')  # Updated to empty prefix

@main_bp.route('/')
def landing():
    return render_template('landing.html')

@main_bp.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    
    params = {
        'api_key': TMDB_API_KEY,
        'page': page
    }
    
    # Use different endpoints based on category
    if category == 'movie':
        trending_url = 'https://api.themoviedb.org/3/trending/movie/day'
    elif category == 'tv':
        trending_url = 'https://api.themoviedb.org/3/trending/tv/day'
    elif category == 'anime':
        trending_url = 'https://api.themoviedb.org/3/discover/tv'
        params['with_keywords'] = '210024'  # Anime keyword
        params['sort_by'] = 'popularity.desc'
    else:
        trending_url = TMDB_TRENDING_URL
        
    try:
        trending_res = requests.get(trending_url, params=params)
        logging.debug(f"API Request URL: {trending_res.url}")
        logging.debug(f"API Response Status: {trending_res.status_code}")
        if not trending_res.ok:
            raise Exception(f"API request failed with status {trending_res.status_code}")
            
        trending_items = trending_res.json().get('results', [])
        
        # Set media_type for anime category
        if category == 'anime':
            for item in trending_items:
                item['media_type'] = 'tv'
        
        # Render JSON only for valid AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'items': trending_items})
        
        # Render the template for normal requests
        return render_template('index.html', 
                               trending_items=trending_items,
                               image_base=TMDB_IMAGE_BASE,
                               current_category=category,
                               category_title=CATEGORY_NAMES.get(category, 'Trending Entertainment'),
                               default_poster=DEFAULT_POSTER)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return render_template('error.html', error_message=str(e)), 500

@main_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    
    items = []
    if query:
        params = {
            'api_key': TMDB_API_KEY,
            'query': query,
            'page': page
        }
        
        if category != 'all':
            params['type'] = category
        
        res = requests.get(TMDB_SEARCH_URL, params=params)
        logging.debug(f"API Request URL: {res.url}")
        logging.debug(f"API Response Status: {res.status_code}")
        if res.ok:
            data = res.json()
            items = [item for item in data.get('results', []) 
                     if category == 'all' or item.get('media_type') == category]
            
            # Render JSON only for valid AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'items': items})
        else:
            logging.error(f"Search API request failed with status {res.status_code}")
    
    # Render the template for normal requests
    return render_template('index.html', 
                           items=items, 
                           trending_items=[],  # Empty for search results
                           image_base=TMDB_IMAGE_BASE,
                           default_poster=DEFAULT_POSTER,
                           current_category=category,
                           category_title="Search Results")