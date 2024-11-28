from models.models import *
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError

def rice_disease_detection():
    try:
        # Ambil query dari URL parameter dan hilangkan spasi tambahan
        query = request.args.get('disease', default='', type=str).strip()

        # Jika query kosong, kembalikan error
        if not query:
            return jsonify({'status': 'error', 'message': 'Parameter query tidak boleh kosong'}), 400
        
        # Pecah query menjadi kata-kata
        keywords = query.split()
        
        filters = [PlantDis.dis_name.ilike(f"%{kw}%") for kw in keywords]
        data = PlantDis.query.filter(db.or_(*filters)).all()

        data_predict = [pred.to_dict() for pred in data]

        if data_predict:
            return jsonify({
                "message": "Sukses menampilkan hasil prediksi penyakit",
                "prediction": data_predict
            }), 200

        return jsonify({
                "message": "Gagal menampilkan hasil prediksi penyakit",
            }), 404

    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": "Kesalahan saat deteksi penyakit tanaman", "error": str(e)}), 500

def corn_disease_detection():
    try:
        # Ambil query dari URL parameter dan hilangkan spasi tambahan
        query = request.args.get('disease', default='', type=str).strip()

        # Jika query kosong, kembalikan error
        if not query:
            return jsonify({'status': 'error', 'message': 'Parameter query tidak boleh kosong'}), 400
        
        # Pecah query menjadi kata-kata
        keywords = query.split()
        
        filters = [PlantDis.dis_name.ilike(f"%{kw}%") for kw in keywords]
        data = PlantDis.query.filter(db.or_(*filters)).all()

        data_predict = [pred.to_dict() for pred in data]

        if data_predict:
            return jsonify({
                "message": "Sukses menampilkan hasil prediksi penyakit",
                "prediction": data_predict
            }), 200

        return jsonify({
                "message": "Gagal menampilkan hasil prediksi penyakit",
            }), 404

    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": "Kesalahan saat deteksi penyakit tanaman", "error": str(e)}), 500