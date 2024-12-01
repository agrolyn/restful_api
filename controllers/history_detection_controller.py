from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from models.models import DetectionHistory, db
from sqlalchemy.exc import SQLAlchemyError
from utils import image_uploaded

def get_all_history():
    try:
        all_history = []
        # Mendapatkan data user dari JWT
        jwt_data = get_jwt_identity()
        user_id = jwt_data.get("id")
        if not user_id:
            return jsonify({'status': 'error', 'message': 'Pengguna tidak valid'}), 401

        # Mengambil data history berdasarkan users_id
        detection_histories = DetectionHistory.query.filter_by(users_id=user_id).all()
        if not detection_histories:
            return jsonify({'status': 'error', 'message': 'Tidak ada riwayat deteksi tersedia'}), 404

        for detection_history in detection_histories:
            all_history.append(
                {
                    "id": detection_history.id,
                    "history_date": detection_history.history_date,
                    "disease_name": detection_history.plant_dis.dis_name,
                    "disease_indonesian_name": detection_history.plant_dis.dis_indo_name,
                    "image_detection": detection_history.img_detection
                }
            )

        return jsonify({
            'status': 'success',
            'data': all_history
        }), 200

    except SQLAlchemyError as e:
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data riwayat deteksi', 'error': str(e)}), 500


def get_detail_history(id_history):
    try:
        # Mendapatkan data user dari JWT
        jwt_data = get_jwt_identity()
        user_id = jwt_data.get("id")
        if not user_id:
            return jsonify({'status': 'error', 'message': 'Pengguna tidak valid'}), 401

        # Mengambil detail riwayat berdasarkan id dan users_id
        detection_history = DetectionHistory.query.filter_by(id=id_history, users_id=user_id).first()
        if not detection_history:
            return jsonify({'status': 'error', 'message': 'Riwayat deteksi tidak ditemukan atau tidak milik Anda'}), 404
        
        detail_history = {
            "id": detection_history.id,
            "history_date": detection_history.history_date,
            "disease_name": detection_history.plant_dis.dis_name,
            "disease_indonesian_name": detection_history.plant_dis.dis_indo_name,
            "image_detection": detection_history.img_detection,
            "description":detection_history.plant_dis.description,
            "handling":detection_history.plant_dis.handling,
        }

        # Mengembalikan data dalam bentuk dict
        return jsonify({
            'status': 'success',
            'data': detail_history
        }), 200

    except SQLAlchemyError as e:  # Menangani kesalahan database
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengambil data riwayat deteksi', 'error': str(e)}), 500

def delete_detection_by_id(id_detection):
    try:
        # Mendapatkan data user dari JWT
        jwt_data = get_jwt_identity()
        user_id = jwt_data.get("id")
        if not user_id:
            return jsonify({'status': 'error', 'message': 'Pengguna tidak valid'}), 401

        # Mencari deteksi berdasarkan ID dan users_id
        detection_history = DetectionHistory.query.filter_by(id=id_detection, users_id=user_id).first()
        if not detection_history:
            return jsonify({'status': 'error', 'message': 'Deteksi tidak ditemukan atau tidak milik Anda'}), 404
        
        if detection_history.img_detection:
            filename_img = detection_history.img_detection.split('/')[-1]
            image_uploaded.delete_image(filename_img)

        # Menghapus deteksi
        db.session.delete(detection_history)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Deteksi berhasil dihapus'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback jika terjadi kesalahan
        return jsonify({'status': 'error', 'message': 'Kesalahan saat menghapus deteksi', 'error': str(e)}), 500


def delete_all_detections():
    try:
        # Mendapatkan data user dari JWT
        jwt_data = get_jwt_identity()
        user_id = jwt_data.get("id")
        if not user_id:
            return jsonify({'status': 'error', 'message': 'Pengguna tidak valid'}), 401

        # Mengambil semua deteksi yang terkait dengan user
        delete_all_history = DetectionHistory.query.filter_by(users_id=user_id).all()
        
        if not delete_all_history:
            return jsonify({'status': 'error', 'message': 'Tidak ada deteksi untuk dihapus'}), 404

        for d_all in delete_all_history:
            # Jika ada gambar terkait, hapus gambar tersebut
            if d_all.img_detection:
                filename_img = d_all.img_detection.split('/')[-1]
                image_uploaded.delete_image(filename_img)

            # Hapus deteksi dari database
            db.session.delete(d_all)

        db.session.commit()  # Simpan perubahan

        return jsonify({'status': 'success', 'message': 'Semua deteksi Anda berhasil dihapus'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback jika terjadi kesalahan
        return jsonify({'status': 'error', 'message': 'Kesalahan saat menghapus semua deteksi', 'error': str(e)}), 500


