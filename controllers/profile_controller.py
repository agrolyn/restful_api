from datetime import *
from flask import *
from flask_jwt_extended import create_access_token
from flask_mail import Message
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