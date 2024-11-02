from datetime import *
from flask import jsonify
from models.models import *

from flask import jsonify

######################################################################
######################## Articles Endpoint ###########################
######################################################################

# Get All Articles
def get_all_articles():
    articles = Articles.query.all()

    articles_list = [article.to_dict() for article in articles]
    return jsonify({'status': 'success', 'data': articles_list}), 200

# Get Detail Article
def get_detail_articles(id_article):
    article = Articles.query.get(id_article)
    if article:
        return jsonify({'status': 'success', 'data': article.to_dict()}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Artikel tidak ditemukan'}), 404


