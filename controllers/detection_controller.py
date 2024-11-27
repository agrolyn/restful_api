# import numpy as np
# from flask import *
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image
# import io  
# from PIL import Image 

# # Corn Model
# MODEL_PATH = 'static/model_ai/corn_disease.keras'
# model_corn = load_model(MODEL_PATH)

# # Rice Model
# MODEL_PATH = 'static/model_ai/rice_disease.keras'
# model_rice = load_model(MODEL_PATH)

# def corn_disease_predict():
#     class_labels = [
#         'Cercospora_leaf_spot Gray_leaf_spot',
#         'Common_rust',
#         'Northern_Leaf_Blight',
#         'healthy'
#     ]

#     # Cek apakah file ada dalam request
#     if 'img_pred' not in request.files:
#         return jsonify({'error': 'Tidak ada file yang dikirimkan'}), 400

#     file = request.files['img_pred']

#     # Jika file kosong
#     if file.filename == '':
#         return jsonify({'error': 'File tidak ditemukan'}), 400

#     # Membaca gambar dari file yang diupload
#     try:
#         img = Image.open(io.BytesIO(file.read()))  # Membaca file menjadi gambar dengan PIL
#         img = img.resize((128, 128))  # Sesuaikan ukuran gambar dengan input model
#         img_array = np.array(img)  # Mengubah gambar menjadi array numpy
#         x = np.expand_dims(img_array, axis=0)  # Tambahkan batch dimension
#     except Exception as e:
#         return jsonify({'error': 'Failed to process image', 'message': str(e)}), 500

#     # Melakukan prediksi
#     try:
#         preds = model_corn.predict(x)
#         index = np.argmax(preds, axis=1)[0]
#         predicted_disease = class_labels[index]
#     except Exception as e:
#         return jsonify({'error': 'Failed Prediction', 'message': str(e)}), 500

#     # Mengembalikan hasil prediksi
#     return jsonify({'Corn Disease': predicted_disease})

# def rice_disease_predict():
#     class_labels = [
#         'bacterial_leaf_blight',
#         'bacterial_leaf_streak',
#         'bacterial_panicle_blight',
#         'blast',
#         'brown_spot',
#         'dead_heart',
#         'downy_mildew',
#         'hispa',
#         'normal',
#         'tungro'
#     ]
    
#     # Cek apakah file ada dalam request
#     if 'img_pred' not in request.files:
#         return jsonify({'error': 'Tidak ada file yang dikirimkan'}), 400

#     file = request.files['img_pred']

#     # Jika file kosong
#     if file.filename == '':
#         return jsonify({'error': 'File tidak ditemukan'}), 400

#     # Membaca gambar dari file yang diupload
#     try:
#         img = Image.open(io.BytesIO(file.read()))  # Membaca file menjadi gambar dengan PIL
#         img = img.resize((128, 128))  # Sesuaikan ukuran gambar dengan input model
#         img_array = np.array(img)  # Mengubah gambar menjadi array numpy
#         x = np.expand_dims(img_array, axis=0)  # Tambahkan batch dimension
#     except Exception as e:
#         return jsonify({'error': 'Failed to process image', 'message': str(e)}), 500

#     # Melakukan prediksi
#     try:
#         preds = model_rice.predict(x)
#         index = np.argmax(preds, axis=1)[0]
#         predicted_disease = class_labels[index]
#     except Exception as e:
#         return jsonify({'error': 'Failed Prediction', 'message': str(e)}), 500

#     # Mengembalikan hasil prediksi
#     return jsonify({'Rice Disease': predicted_disease})
