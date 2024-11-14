from datetime import *
from flask import jsonify
from models.models import *

from flask import jsonify
    
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