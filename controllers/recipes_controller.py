from flask import jsonify
from models.models import Recipes
from sqlalchemy.exc import SQLAlchemyError

######################################################################
######################### Recipes Endpoint ###########################
######################################################################

# Get All Recipes
def get_all_recipes():
    try:
        recipes = Recipes.query.all()
        if not recipes:  # Kondisi jika tidak ada resep ditemukan
            return jsonify({'status': 'error', 'message': 'Tidak ada resep tersedia'}), 404

        recipes_list = [recipe.to_dict() for recipe in recipes]
        return jsonify({'status': 'success', 'data': recipes_list}), 200

    except SQLAlchemyError as e:  # Menangani kesalahan database
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data resep', 'error': str(e)}), 500


# Get Detail Recipe
def get_detail_recipes(id_recipe):
    try:
        recipe = Recipes.query.get(id_recipe)
        if recipe:
            return jsonify({'status': 'success', 'data': recipe.to_dict()}), 200
        else:  # Jika resep tidak ditemukan
            return jsonify({'status': 'error', 'message': 'Resep tidak ditemukan'}), 404

    except SQLAlchemyError as e:  # Menangani kesalahan database
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data resep', 'error': str(e)}), 500
