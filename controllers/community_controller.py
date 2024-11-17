from datetime import *
from flask import jsonify
from models.models import *

from flask import jsonify

######################################################################
######################## Question Endpoint ###########################
######################################################################

def get_all_question():
    community = []
    questions = Questions.query.all()

    for question in questions:
        community.append(
            {
                "id": question.id,
                "username": question.users.name,
                "user_profile": question.users.img_profile,
                "question_type": question.plant_types.plant_name,
                "question": question.question,
                "like_num": question.like_num,
                "question_thumbnail": question.img_q,
                "number_of_answer": len(question.disccus),
                "released_date": question.released_date
            }
        )
    
    try:
        return jsonify({
            'message': 'Berhasil menampilkan semua data pertanyaan komunitas',
            'data': community
        }), 200
    except Exception as e:
        return jsonify({'message': 'Error terjadi', 'error': str(e)}), 500

def get_detail_question(id):
    questions = Questions.query.get(id)
    if questions:
        return jsonify({'status': 'success', 'data': questions.to_dict()}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Pertanyaan tidak ditemukan'}), 404
    
######################################################################
######################### Disccus Endpoint ###########################
######################################################################

def get_disccus_by_question(questions_id):
    disccus_list = Disccus.query.filter_by(questions_id=questions_id).all()
    if disccus_list:
        return jsonify({
            'status': 'success',
            'data': [disccus.to_dict() for disccus in disccus_list]
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Diskusi tidak ditemukan untuk pertanyaan ini'
        }), 404