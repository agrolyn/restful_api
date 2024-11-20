from datetime import *
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from models.models import *
from sqlalchemy.exc import SQLAlchemyError

from flask import jsonify

def get_all_products():
    try:
        all_products = Products.query.all()
        if not all_products:
            return jsonify({'status': 'error', 'message': 'Tidak ada produk tersedia'}), 404

        products = [product.to_dict() for product in all_products]
        return jsonify({
            "status": "success",
            "message": "Sukses menampilkan data produk",
            "data": products
        }), 200

    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": "Kesalahan saat mengambil data produk", "error": str(e)}), 500

def get_filtered_products(product_categories_id):
    try:
        # Ambil semua produk berdasarkan kategori
        filtered_products = Products.query.filter_by(product_categories_id=product_categories_id).all()
        
        # Jika tidak ada produk ditemukan
        if not filtered_products:
            return jsonify({'status': 'error', 'message': 'Produk dengan kategori ini tidak ditemukan'}), 404
        
        # Konversi hasil query ke dalam bentuk dictionary
        products = [product.to_dict() for product in filtered_products]
        
        return jsonify({
            "status": "success",
            "message": "Sukses menampilkan data produk berdasarkan kategori",
            "data": products
        }), 200

    except SQLAlchemyError as e:
        # Tangani jika terjadi error dengan database
        return jsonify({"status": "error", "message": "Kesalahan saat mengambil data produk", "error": str(e)}), 500
