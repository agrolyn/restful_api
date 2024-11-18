from datetime import *
from flask import *
from flask_jwt_extended import get_jwt_identity
from models.models import *
    
def edit_profile():
    user_identity = get_jwt_identity()
    user_id = user_identity['id']

    data = request.get_json()
    name = data.get("name")
    address = data.get("address")
    phone_number = data.get("phone_number")

    update_fields = {}
    if name is not None:
        update_fields["name"] = name
    if address is not None:
        update_fields["address"] = address
    if phone_number is not None:
        update_fields["phone_number"] = phone_number

    # Memeriksa apakah ada field yang ingin di-update
    if not update_fields:
        return jsonify({"message": "Tidak ada bidang yang valid untuk diperbarui."}), 400

    # Mengambil user berdasarkan user_id
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({"message": "Pengguna tidak ditemukan."}), 404

    # Melakukan update pada field yang diberikan
    for key, value in update_fields.items():
        setattr(user, key, value)

    # Menyimpan perubahan ke database
    db.session.commit()

    return jsonify({"message": "Profil berhasil diperbarui."}), 200