from datetime import *
import os
from flask import *
from flask_jwt_extended import get_jwt_identity
from models.models import *
import requests

######################################################################
######################## Utility Function ############################
######################################################################

def uploads_image(img):
    # Simpan file ke direktori sementara
    temp_path = "/tmp"
    filename = os.path.join(temp_path, img.filename)
    img.save(filename)

    # Gunakan file yang disimpan untuk upload
    url = "https://agrolyn.online/uploads-image/"
    with open(filename, 'rb') as img_file:
        files = {'img_upl': img_file}
        try:
            response = requests.post(url, files=files)
            # Cek status response
            if response.status_code == 201:
                print("Upload berhasil:", response.json().get("new_image"))
                return response.json().get("new_image")
            else:
                print("Gagal upload:", response.status_code, response.text)
                return None

        except Exception as e:
            print(f"Error during file upload: {e}")
            return None
        finally:
            # Hapus file sementara setelah selesai
            os.remove(filename)

def update_image(img_new, img_old):
    # Simpan file baru ke direktori sementara
    temp_path = "/tmp"
    filename_new = os.path.join(temp_path, img_new.filename)
    img_new.save(filename_new)

    url = f"https://agrolyn.online/update-image/{img_old}/"
    
    with open(filename_new, 'rb') as img_file:
        files = {'img_upl': img_file}
        try:
            # Kirimkan file untuk diupdate
            response = requests.post(url, files=files)
            
            # Cek status response dari server
            if response.status_code == 201:
                # Ambil nama file baru yang diupload dari respons API
                filename = response.json().get("new_image")
                print("Update berhasil:", filename)
                return filename
            else:
                print("Gagal update gambar:", response.status_code, response.text)
                return None

        except requests.exceptions.RequestException as e:
            # Tangani kesalahan dalam koneksi atau request
            print(f"Error during file update: {e}")
            return None

        finally:
            # Hapus file sementara setelah selesai
            if os.path.exists(filename_new):
                os.remove(filename_new)

def delete_image(img_name):
    url = f"https://agrolyn.online/delete-image/{img_name}/"
    
    try:
        response = requests.get(url)
        if response.status_code == 201:
            # Return pesan berhasil
            return "Gambar berhasil dihapus dari Agrolyn."
        elif response.status_code == 404:
            return "Gagal menghapus gambar. Gambar tidak ditemukan."
        else:
            return "Gagal menghapus gambar."
    except requests.exceptions.RequestException as e:
        return str(e), 500
