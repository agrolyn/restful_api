from datetime import datetime
from flask_jwt_extended import get_jwt_identity
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from utils import image_uploaded
from models.models import PlantDis, DetectionHistory, db

def disease_detection(disease, plant_type):
    try:
        plant_type_id = 2 if plant_type == "rice" else 1

        datenow = datetime.now()
        jwt_data = get_jwt_identity()
        user_id = jwt_data.get("id")

        # Ambil file gambar dari request
        img_det = request.files.get("img_pred")
        if not img_det:
            return jsonify({"message": "Tidak ada file yang diunggah"}), 400

        # Pisahkan kata kunci untuk pencarian penyakit
        keywords = disease.split()
        filters = [PlantDis.dis_name.ilike(f"%{kw}%") for kw in keywords]
        
        # Filter data penyakit berdasarkan jenis tanaman dan kata kunci
        data = PlantDis.query.filter(and_(*filters), PlantDis.plant_types_id == plant_type_id).all()
        data_predict = [pred.to_dict() for pred in data]

        if not data_predict:
            return jsonify({"message": "Gagal menampilkan hasil prediksi penyakit"}), 404

        # Unggah gambar dan catat nama file
        filename = image_uploaded.uploads_image(img_det)
        history_date = datenow.strftime('%Y-%m-%d %H:%M:%S')

        # Tambahkan riwayat deteksi ke database
        new_history = DetectionHistory(
            img_detection=filename,
            history_date=history_date,
            users_id=user_id,
            plant_dis_id=data_predict[0].get('id')  # Ambil ID penyakit pertama
        )

        db.session.add(new_history)
        db.session.commit()

        # Kembalikan hasil prediksi
        return jsonify({
            "message": "Sukses menampilkan hasil prediksi penyakit",
            "prediction": data_predict
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback jika ada error pada database
        return jsonify({
            "status": "error",
            "message": "Kesalahan saat deteksi penyakit tanaman",
            "error": str(e)
        }), 500
