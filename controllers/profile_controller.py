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