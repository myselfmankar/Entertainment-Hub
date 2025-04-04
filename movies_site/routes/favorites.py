from flask import Blueprint, jsonify, request, render_template, session
from models.favorite import Favorite
from config import TMDB_IMAGE_BASE
from auth import login_required

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('/favorites')
def list_favorites():
    user_id = session.get('user_id')
    if not user_id:
        # Return empty favorites for guest users
        return render_template('favorites.html', 
                             favorites=[],
                             is_guest=True,
                             image_base=TMDB_IMAGE_BASE)
    
    favorites_ref = Favorite.get_collection()
    favorites_data = [doc.to_dict() for doc in favorites_ref.where('user_id', '==', user_id).get()]
    return render_template('favorites.html', 
                         favorites=favorites_data,
                         is_guest=False,
                         image_base=TMDB_IMAGE_BASE)

@favorites_bp.route('/favorites/toggle_fav', methods=['POST'])
def toggle_favorite():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({
            'message': 'Please login to add favorites',
            'code': 401,
            'success': False
        }), 401
    
    data = request.get_json()
    item_id = data.get('item_id')
    favorites_ref = Favorite.get_collection()
    
    existing_fav = favorites_ref.where('item_id', '==', item_id).where('user_id', '==', user_id).get()
    
    if len(list(existing_fav)) > 0:
        for doc in existing_fav:
            doc.reference.delete()
        return jsonify({
            'message': 'Removed from favorites!',
            'success': False
        })
    
    favorite = Favorite(
        user_id=user_id,
        item_id=data.get('item_id'),
        title=data.get('title'),
        poster_path=data.get('poster_path'),
        media_type=data.get('media_type')
    )
    
    favorites_ref.add(favorite.to_dict())
    return jsonify({
        'message': 'Added to favorites!',
        'success': True
    })
