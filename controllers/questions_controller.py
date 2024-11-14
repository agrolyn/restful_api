from datetime import *
from flask import jsonify
from models.models import *

from flask import jsonify

######################################################################
######################## Question Endpoint ###########################
######################################################################

def get_all_question():
    questions = Questions.query.all()

    questions_list = [question.to_dict() for question in questions]
    return jsonify({'status': 'success', 'data': questions_list}), 200

def get_detail_question(id):
    questions = Questions.query.get(id)
    if questions:
        return jsonify({'status': 'success', 'data': questions.to_dict()}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Pertanyaan tidak ditemukan'}), 404



