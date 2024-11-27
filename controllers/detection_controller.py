from models.models import *
from flask import jsonify, request
from utils.image_uploaded import predict_plant_disease

def rice_disease_detection():
    img_pred = request.files.get("img_pred")

    # Validasi gambar
    if not img_pred:
        return jsonify({
            "message": "Gambar tidak ditemukan."
        }), 400
    
    prediction = predict_plant_disease(img=img_pred, plant_type="rice")

    data = PlantDis.query.filter(PlantDis.dis_name.ilike(f"%{prediction}%")).all()
    
    data_predict = [pred.to_dict() for pred in data]

    if prediction:
        return jsonify({
            "message": "Sukses menampilkan hasil prediksi penyakit",
            "prediction": data_predict
        }), 200
    
    return jsonify({
            "message": "Gagal menampilkan hasil prediksi penyakit",
        }), 404

def corn_disease_detection():
    img_pred = request.files.get("img_pred")

    # Validasi gambar
    if not img_pred:
        return jsonify({
            "message": "Gambar tidak ditemukan."
        }), 400
    
    prediction = predict_plant_disease(img=img_pred, plant_type="corn")

    data = PlantDis.query.filter(PlantDis.dis_name.ilike(f"%{prediction}%")).all()

    data_predict = [pred.to_dict() for pred in data]
    
    if prediction:
        return jsonify({
            "message": "Sukses menampilkan hasil prediksi penyakit",
            "prediction": data_predict
        }), 200
    
    return jsonify({
            "message": "Gagal menampilkan hasil prediksi penyakit",
        }), 404