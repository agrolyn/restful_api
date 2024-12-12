from datetime import *
from flask import *
from flask_jwt_extended import get_jwt_identity
from models.models import *
from utils import image_uploaded
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

        name = user_identity.get("name")
        review = data.get("review")
        rating = int(data.get("rating"))
        released_date = datenow.strftime('%Y-%m-%d %H:%M:%S')
        type_review = ''

        if rating == 1:
            type_review = "Komentar Negatif"
        elif rating == 2:
            type_review = "Komentar Negatif"
        elif rating == 3:
            type_review = "Komentar Netral"
        elif rating == 4:
            type_review = "Komentar Positif"
        elif rating == 5:
            type_review = "Komentar Positif"

        new_review_user = ReviewUsers(
            name=name,
            users_id=users_id,
            review=review,
            rating=rating,
            type_review=type_review,
            released_date=released_date    
        )

        db.session.add(new_review_user)

        # Menyimpan perubahan ke database
        db.session.commit()

        if users_id is None:
            return jsonify({"message": "Pengguna tidak valid."}), 404
        else:
            # Assuming you want to return the created review details
            return jsonify({
                "message": "Berhasil menambahkan ulasan aplikasi.",
                "review": new_review_user.to_dict()
            }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Kesalahan saat mengulas aplikasi', 'error': str(e)}), 500