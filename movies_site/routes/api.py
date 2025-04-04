from flask import Blueprint, jsonify, request
import requests
from config import TMDB_API_KEY, TMDB_GENRES_URL, TMDB_SEARCH_URL

api_bp = Blueprint('api', __name__)

@api_bp.route('/genres')
def genres():
    params = {'api_key': TMDB_API_KEY}
    res = requests.get(TMDB_GENRES_URL, params=params)
    genres = res.json().get('genres', []) if res.ok else []
    return jsonify(genres)

@api_bp.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])

    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'page': 1,
        'sort_by': 'popularity.desc',
        'vote_count.gte': 100
    }
    res = requests.get(TMDB_SEARCH_URL, params=params)
    items = []
    if res.ok:
        results = res.json().get('results', [])
        sorted_results = sorted(results, 
                              key=lambda x: (x.get('popularity', 0), x.get('vote_count', 0)), 
                              reverse=True)
        
        for item in sorted_results[:8]:
            title = item.get('title') or item.get('name')
            items.append({
                'id': item.get('id'),
                'title': title,
                'poster_path': item.get('poster_path'),
                'media_type': item.get('media_type'),
                'year': item.get('release_date', '')[:4] if item.get('release_date') else '',
                'vote_average': item.get('vote_average', 0),
                'popularity': item.get('popularity', 0)
            })
    return jsonify(items)
