from flask import jsonify
from models.models import Recommendations, RecommendCategories
from sqlalchemy.exc import SQLAlchemyError

######################################################################@@@@@@@
######################### Recommendation Endpoint ###########################
######################################################################@@@@@@@

# Get All Recommendation Category
def get_all_recom_cat():
    try:
        recom_cat = RecommendCategories.query.all()
        if not recom_cat:
            return jsonify({'status': 'error', 'message': 'Tidak ada rekomendasi olahan tersedia'}), 404

        recom_cat_list = [recipe.to_dict() for recipe in recom_cat]
        return jsonify({
            'status': 'success',
            'message': 'Daftar kategori rekomendasi olahan berhasil ditampilkan',
            'data': recom_cat_list
        }), 200

    except SQLAlchemyError as e:  # Menangani kesalahan database
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data rekomendasi olahan', 'error': str(e)}), 500


# Get Recommendation By Category
def get_recom_by_cat(id_cat):
    try:
        recommend = Recommendations.query.filter(Recommendations.recommend_category.has(id=id_cat)).all()
        if not recommend: 
            return jsonify({'status': 'error', 'message': 'Tidak ada rekomendasi olahan tersedia'}), 404

        recommend_list = [recom.to_dict() for recom in recommend]
        return jsonify({
            'status': 'success', 
            'message': 'Daftar rekomendasi olahan berhasil ditampilkan',
            'data': recommend_list
        }), 200

    except SQLAlchemyError as e:  # Menangani kesalahan database
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data rekomendasi olahan', 'error': str(e)}), 500

# Get Details of Recommendations
def get_details_recom(id):
    try:
        recommend = Recommendations.query.get(id)
        if recommend:
            return jsonify({
                'status': 'success',
                'message': 'Detail rekomendasi olahan berhasil ditampilkan',
                'data': recommend.to_dict()
            }), 200
        else:
            return jsonify({'status': 'error', 'message': 'Rekomendasi olahan tidak ditemukan'}), 404

    except SQLAlchemyError as e:  # Menangani kesalahan database
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data rekomendasi olahan', 'error': str(e)}), 500
