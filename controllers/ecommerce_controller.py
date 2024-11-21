from datetime import *
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from models.models import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from utils import image_uploaded


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

def search_product():
    try:
        # Ambil query dari URL parameter dan hilangkan spasi tambahan
        query = request.args.get('query', default='', type=str).strip()
        
        # Jika query kosong, kembalikan error
        if not query:
            return jsonify({'status': 'error', 'message': 'Parameter query tidak boleh kosong'}), 400
        
        # Pecah query menjadi kata-kata
        keywords = query.split()
        
        # Filter menggunakan semua kata kunci
        filters = [
            Products.product_name.ilike(f"%{keyword}%") | Products.desc_product.ilike(f"%{keyword}%")
            for keyword in keywords
        ]
        
        # Gabungkan filter dengan operator "or"
        matching_products = Products.query.filter(or_(*filters)).all()
        
        # Jika tidak ada produk ditemukan
        if not matching_products:
            return jsonify({'status': 'error', 'message': 'Produk tidak ditemukan'}), 404
        
        # Konversi hasil query ke dalam bentuk dictionary
        products = [product.to_dict() for product in matching_products]
        
        return jsonify({
            "status": "success",
            "message": f"Sukses menemukan {len(products)} produk berdasarkan pencarian",
            "data": products
        }), 200

    except SQLAlchemyError as e:
        # Tangani jika terjadi error dengan database
        return jsonify({"status": "error", "message": "Kesalahan saat mencari produk", "error": str(e)}), 500



def new_product():
    user_identity = get_jwt_identity()
  

    # Mengambil ID user dari JWT
    users_id = user_identity.get("id")

    # Mengambil data dari form
    product_name = request.form["product_name"]
    desc_product = request.form["desc_product"]
    price = int(request.form.get("price", 0))
    stock = int(request.form.get("stock", 0))
    product_categories_id = request.form["product_categories_id"]
    img_product = request.files.get("img_product")


    # Validasi gambar
    if not img_product:
        return jsonify({
            "message": "Gagal menambahkan data. Gambar tidak ditemukan."
        }), 400

    # Upload gambar menggunakan fungsi utility
    filename_img = image_uploaded.uploads_image(img_product)

    if not filename_img:
        return jsonify({
            "message": "Gagal mengunggah gambar."
        }), 500

    # Jika upload berhasil, buat instance produk baru
    new_product = Products(
        product_name=product_name,
        desc_product=desc_product,
        img_product=f"https://yourwebsite.com/static/uploads/{filename_img}",
        price=price,
        stock=stock,
        sold=0,  # Default
        product_categories_id=product_categories_id,
        users_id=users_id
    )

    # Simpan ke database
    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "message": "Sukses menambahkan produk",
        "new_product": new_product.to_dict()
    }), 200
    