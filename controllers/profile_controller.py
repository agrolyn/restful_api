from datetime import *
from flask import *
from flask_jwt_extended import get_jwt_identity
from models.models import *
from utils import image_uploaded
import requests
from sqlalchemy.exc import SQLAlchemyError
    
def edit_profile():
    try:
        user_identity = get_jwt_identity()
        user_id = user_identity.get("id")
        user_me = Users.query.get(user_id)

        name = request.form["name"]
        address = request.form["address"]
        phone_number = request.form["phone_number"]
        img_p = request.files.get('img_profile')

        if name is not None:
            user_me.name = name
        if address is not None:
            user_me.address = address
        if phone_number is not None:
            user_me.phone_number = phone_number

        if img_p:
            filename_img = image_uploaded.uploads_image(img_p)
            if not filename_img:
                return jsonify({
                    "message": "Gagal mengunggah gambar."
                }), 500

            # Hapus gambar lama jika ada
            if user_me.img_profile:
                old_filename = user_me.img_profile.split('/')[-1]
                image_uploaded.delete_image(old_filename)

            user_me.img_profile = f"https://agrolyn.online/static/uploads/{filename_img}"

        if user_me is None:
            return jsonify({"message": "Pengguna tidak ditemukan."}), 404

        # Menyimpan perubahan ke database
        db.session.commit()

        return jsonify({"message": "Profil berhasil diperbarui."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengupdate profil', 'error': str(e)}), 500

def rating_users():
    try:
        user_identity = get_jwt_identity()
        users_id = user_identity.get("id")
        data = request.get_json()
        datenow = datetime.now()

        if users_id is None:
            return jsonify({"message": "Pengguna tidak valid."}), 404

        name = user_identity.get("name")
        review = data.get("review")
        released_date = datenow.strftime('%Y-%m-%d %H:%M:%S')

        # Call sentiment analysis API
        sentiment_api_url = "https://sentiment.linggashop.my.id/sentiment"
        payload = {"text": review}

        try:
            response = requests.post(sentiment_api_url, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            sentiment_data = response.json()
            type_review = sentiment_data.get("type_review", "Tidak Diketahui")
        except requests.RequestException as e:
            return jsonify({
                "status": "error",
                "message": "Kesalahan saat memproses analisis sentimen.",
                "error": str(e)
            }), 500

        # Assuming rating is still provided by the user
        rating = int(data.get("rating", 0))

        # Create a new review entry
        new_review_user = ReviewUsers(
            name=name,
            users_id=users_id,
            review=review,
            rating=rating,
            type_review=type_review,
            released_date=released_date
        )

        db.session.add(new_review_user)

        # Commit changes to the database
        db.session.commit()

        # Return success response
        return jsonify({
            "message": "Berhasil menambahkan ulasan aplikasi.",
            "review": new_review_user.to_dict()
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Kesalahan saat mengulas aplikasi.',
            'error': str(e)
        }), 500
