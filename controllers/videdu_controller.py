from flask import jsonify
from models.models import VideoEducation
from sqlalchemy.exc import SQLAlchemyError

def get_all_videdu():
    try:
        videdus = VideoEducation.query.all()
        if not videdus:
            return jsonify({'status': 'error', 'message': 'Tidak ada video edukasi tersedia'}), 404

        videdus_list = [videdu.to_dict() for videdu in videdus]
        return jsonify({'status': 'success', 'data': videdus_list}), 200

    except SQLAlchemyError as e:
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data video edukasi', 'error': str(e)}), 500

def get_detail_videdu():
    try:
        videdus = VideoEducation.query.get(id)
        if videdus:
            return jsonify({'status': 'success', 'data': videdus.to_dict()}), 200
        else:  # Jika resep tidak ditemukan
            return jsonify({'status': 'error', 'message': 'Video edukasi tidak ditemukan'}), 404

    except SQLAlchemyError as e:  # Menangani kesalahan database
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data video edukasi', 'error': str(e)}), 500