from datetime import *
from flask import jsonify
from models.models import *

from flask import jsonify
    
######################################################################
######################### Recipes Endpoint ###########################
######################################################################

# Get All Recipes
def get_all_recipes():
    recipes = Recipes.query.all()

    recipes_list = [recipe.to_dict() for recipe in recipes]
    return jsonify({'status': 'success', 'data': recipes_list}), 200

# Get Detail Recipe
def get_detail_recipes(id_recipe):
    recipe = Recipes.query.get(id_recipe)
    if recipe:
        return jsonify({'status': 'success', 'data': recipe.to_dict()}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Artikel tidak ditemukan'}), 404

