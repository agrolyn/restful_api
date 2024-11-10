from datetime import *
from flask import *
from flask_jwt_extended import get_jwt_identity
from models.models import *
import requests

######################################################################
######################## Utility Function ############################
######################################################################

def uploads_image(img):
    url = "https://agrolyn.online/uploads-image"
    
    with open(img, 'rb') as img_file:
        files = {'img_profile': img_file}
        try:
            response = requests.post(url, files=files)
            # Cek status response
            if response.status_code == 201:
                return jsonify({
                    "message": "Image uploaded successfully to Agrolyn",
                    "data": response.json()
                }), 201
            else:
                return jsonify({
                    "message": "Failed to upload image",
                }), response.status_code
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500
        
def delete_image(img_name):
    url = f"https://agrolyn.online/delete-image/{img_name}/"
    
    try:
        response = requests.get(url)
        if response.status_code == 201:
            return jsonify({
                "message": "Image deleted successfully from Agrolyn",
                "data": response.json()
            }), 201
        elif response.status_code == 404:
            return jsonify({
                "message": "Failed to delete image. Image not found.",
                "error": response.json()
            }), 404
        else:
            return jsonify({
                "message": "Failed to delete image",
                "error": response.json()
            }), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    
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
        return jsonify({"message": "No valid fields to update"}), 400

    # Mengambil user berdasarkan user_id
    user = Users.query.get(user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404

    # Melakukan update pada field yang diberikan
    for key, value in update_fields.items():
        setattr(user, key, value)

    # Menyimpan perubahan ke database
    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200