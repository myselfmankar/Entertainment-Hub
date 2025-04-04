from flask import Blueprint, jsonify, request, render_template
import requests
from config import (
    TMDB_API_KEY, TMDB_SEARCH_URL, TMDB_DETAIL_URL, 
    TMDB_IMAGE_BASE, DEFAULT_POSTER, DEFAULT_VIDEO
)

media_bp = Blueprint('media', __name__)

@media_bp.route('/detail/<media_type>/<int:id>')
def detail(media_type, id):
    params = {'api_key': TMDB_API_KEY, 'append_to_response': 'videos,credits,similar'}
    url = TMDB_DETAIL_URL.format(type=media_type, id=id)
    res = requests.get(url, params=params)
    
    if not res.ok:
        return render_template('404.html'), 404
        
    item = res.json()
    return render_template('detail.html', 
                         item=item, 
                         image_base=TMDB_IMAGE_BASE,
                         default_poster=DEFAULT_POSTER,
                         default_video=DEFAULT_VIDEO)

@media_bp.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
        
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'page': 1
    }
    
    res = requests.get(TMDB_SEARCH_URL, params=params)
    if res.ok:
        return jsonify(res.json().get('results', []))
    return jsonify([])
