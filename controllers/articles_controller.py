from flask import jsonify
from models.models import Articles
from sqlalchemy.exc import SQLAlchemyError

######################################################################
######################## Articles Endpoint ###########################
######################################################################

# Get All Articles
def get_all_articles():
    try:
        articles = Articles.query.all()
        if not articles:  # Kondisi jika tidak ada artikel ditemukan
            return jsonify({'status': 'error', 'message': 'Tidak ada artikel tersedia'}), 404

        articles_list = [article.to_dict() for article in articles]
        return jsonify({'status': 'success', 'data': articles_list}), 200

    except SQLAlchemyError as e:  # Menangani kesalahan database
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data artikel', 'error': str(e)}), 500

# Get Detail Article
def get_detail_articles(id_article):
    try:
        article = Articles.query.get(id_article)
        if article:
            return jsonify({'status': 'success', 'data': article.to_dict()}), 200
        else:  # Jika artikel tidak ditemukan
            return jsonify({'status': 'error', 'message': 'Artikel tidak ditemukan'}), 404

    except SQLAlchemyError as e:  # Menangani kesalahan database
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data artikel', 'error': str(e)}), 500
