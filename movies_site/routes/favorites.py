from flask import Blueprint, jsonify, request, render_template
from config import TMDB_IMAGE_BASE

favorites_bp = Blueprint('favorites', __name__)

# In-memory favorites store (for demo purposes)
favorites = []

@favorites_bp.route('/favorites')
def list_favorites():
    return render_template('favorites.html', 
                         favorites=favorites,
                         is_guest=False,
                         image_base=TMDB_IMAGE_BASE)

@favorites_bp.route('/favorites/toggle_fav', methods=['POST'])
def toggle_favorite():
    data = request.get_json()
    item_id = data.get('item_id')
    
    # Check if item exists in favorites
    existing_items = [item for item in favorites if item['item_id'] == item_id]
    
    if existing_items:
        # Remove from favorites
        favorites[:] = [item for item in favorites if item['item_id'] != item_id]
        return jsonify({
            'message': 'Removed from favorites!',
            'success': False
        })
    
    # Add to favorites
    favorite = {
        'item_id': item_id,
        'title': data.get('title'),
        'poster_path': data.get('poster_path'),
        'media_type': data.get('media_type')
    }
    
    favorites.append(favorite)
    return jsonify({
        'message': 'Added to favorites!',
        'success': True
    })
