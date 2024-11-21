from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from models.models import *


######################################################################
######################### Product Endpoint ###########################
######################################################################

# Get All Recipes
def get_all_product():
    products = Products.query.all()

    product_list = [products.to_dict() for products in products if products]
    return jsonify({'status': 'success', 'data': product_list}), 200

# # Get Detail Recipe n
# def get_detail_recipes(id_recipe):
#     recipe = Recipes.query.get(id_recipe)
#     if recipe:
#         return jsonify({'status': 'success', 'data': recipe.to_dict()}), 200
#     else:
#         return jsonify({'status': 'error', 'message': 'Artikel Recipes  tidak ditemukan'}), 404

