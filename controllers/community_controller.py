from datetime import *
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from models.models import *
from utils import image_uploaded
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_

from flask import jsonify

######################################################################
########################## Get Endpoint ##############################
######################################################################

def get_all_question():
    community = []
    questions = Questions.query.all()

    for question in questions:
        community.append(
            {
                "id": question.id,
                "username": question.users.name,
                "user_profile": question.users.img_profile,
                "question_type": question.plant_types.plant_name,
                "title_question": question.title_q,
                "like_num": question.like_num,
                "question_thumbnail": question.img_q,
                "number_of_answer": len(question.disccus),
                "released_date": question.released_date
            }
        )
    
    try:
        return jsonify({
            "message": "Berhasil menampilkan semua data pertanyaan komunitas",
            "data": community
        }), 200
    except Exception as e:
        return jsonify({"message": "Error terjadi", "error": str(e)}), 500

def get_detail_question(id):
    question = Questions.query.get(id)
    answer = Disccus.query.filter(Disccus.questions_id == question.id).all()
    list_answer = []

    community_question = {
                    "id": question.id,
                    "username": question.users.name,
                    "user_profile": question.users.img_profile,
                    "question_type": question.plant_types.plant_name,
                    "title_question": question.title_q,
                    "description": question.description,
                    "like_num": question.like_num,
                    "question_thumbnail": question.img_q,
                    "number_of_answer": len(question.disccus),
                    "released_date": question.released_date
                }
    
    for ans in answer:
        list_answer.append(
            {
                "id": ans.id,
                "username": ans.users.name,
                "user_profile": ans.users.img_profile,
                "answer": ans.answer,
                "like_num": ans.like_num,
                "released_date": ans.released_date
            }
        )
    
    if question:
        return jsonify({
            "message": "success",
            "data": {
                "question_detail": community_question,
                "list_answer": list_answer,
            }
        }), 200
    else:
        return jsonify({"message": "error", "message": "Pertanyaan komunitas tidak ditemukan"}), 404

def get_filtered_question(filter_name):
    valid_filters = ["umum", "padi", "jagung", "answerme"]
    if filter_name not in valid_filters:
        return jsonify({"message": "Filter tidak valid"}), 400

    try:
        community = []
        if filter_name in ["umum", "padi", "jagung"]:
            questions = Questions.query.filter(Questions.plant_types.has(plant_name=filter_name)).all()
        elif filter_name == "answerme":
            user_identity = get_jwt_identity()
            user_id = user_identity.get("id")
            questions = Questions.query.filter(Questions.users_id == user_id).all()
        
        # Proses data pertanyaan
        for question in questions:
            community.append(
                {
                    "id": question.id,
                    "username": question.users.name if question.users else None,
                    "user_profile": question.users.img_profile if question.users else None,
                    "question_type": question.plant_types.plant_name if question.plant_types else None,
                    "title_question": question.title_q,
                    "like_num": question.like_num,
                    "question_thumbnail": question.img_q,
                    "number_of_answer": len(question.disccus),
                    "released_date": question.released_date
                }
            )
        
        # Jika community kosong
        if not community:
            return jsonify({
                "message": f"Tidak ada data pertanyaan komunitas untuk filter '{filter_name}'",
                "data": []
            }), 200

        # Jika community ada isinya
        return jsonify({
            "message": "Berhasil menampilkan semua data pertanyaan komunitas berdasarkan filtering",
            "data": community
        }), 200

    except Exception as e:
        return jsonify({"message": "Error terjadi", "error": str(e)}), 500

def search_community_question():
    try:
        # Ambil query dari URL parameter dan hilangkan spasi tambahan
        query = request.args.get('query', default='', type=str).strip()
        
        # Jika query kosong, kembalikan error
        if not query:
            return jsonify({'status': 'error', 'message': 'Parameter query tidak boleh kosong'}), 400
        
        # Pecah query menjadi kata-kata
        keywords = query.split()
        
        # Filter menggunakan semua kata kunci
        filters = [
            Questions.title_q.ilike(f"%{keyword}%") | Questions.description.ilike(f"%{keyword}%")
            for keyword in keywords
        ]
        
        # Gabungkan filter dengan operator "or"
        matching_questions = Questions.query.filter(or_(*filters)).all()
        
        # Jika tidak ada pertanyaan ditemukan
        if not matching_questions:
            return jsonify({'status': 'error', 'message': 'Pertanyaan tidak ditemukan'}), 404
        
        # Konversi hasil query ke dalam bentuk dictionary
        questions = [question.to_dict() for question in matching_questions]
        
        return jsonify({
            "status": "success",
            "message": f"Sukses menemukan {len(questions)} pertanyaan komunitas berdasarkan pencarian",
            "data": questions
        }), 200

    except SQLAlchemyError as e:
        # Tangani jika terjadi error dengan database
        return jsonify({"status": "error", "message": "Kesalahan saat mencari pertanyaan komunitas", "error": str(e)}), 500
    
######################################################################
###################### Like Dislike Endpoint #########################
######################################################################

def inc_like_q(id):
    question = Questions.query.get(id)
    try:
        if(question):
            question.like_num += 1
            db.session.commit()

            return jsonify({
                "message": "Sukses menyukai (like) pertanyaan komunitas"
            })
        else:
            return jsonify({
                "message": "Gagal menyukai (like) pertanyaan komunitas"
            })
    except Exception as e:
        return jsonify({"message": "Error terjadi", "error": str(e)}), 500


def dec_like_q(id):
    question = Questions.query.get(id)
    try:
        if(question):
            if(question.like_num > 0):
                question.like_num -= 1
                db.session.commit()

                return jsonify({
                    "message": "Sukses tidak menyukai (dislike) pertanyaan komunitas"
                })
            else:
                return jsonify({
                    "message": "Gagal tidak menyukai (dislike) pertanyaan komunitas"
                })
        else:
            return jsonify({
                "message": "Gagal tidak menyukai (dislike) pertanyaan komunitas"
            })
    except Exception as e:
        return jsonify({"message": "Error terjadi", "error": str(e)}), 500

def inc_like_ans(id):
    disccus = Disccus.query.get(id)
    try:
        if(disccus):
            disccus.like_num += 1
            db.session.commit()

            return jsonify({
                "message": "Sukses menyukai (like) jawaban dari pertanyaan komunitas"
            })
        else:
            return jsonify({
                "message": "Gagal menyukai (like) jawaban dari pertanyaan komunitas"
            })
    except Exception as e:
        return jsonify({"message": "Error terjadi", "error": str(e)}), 500

def dec_like_ans(id):
    disccus = Disccus.query.get(id)
    try:
        if(disccus):
            if(disccus.like_num > 0):
                disccus.like_num -= 1
                db.session.commit()

                return jsonify({
                    "message": "Sukses tidak menyukai (dislike) jawaban dari pertanyaan komunitas"
                })
            else:
                return jsonify({
                    "message": "Gagal tidak menyukai (dislike) jawaban dari pertanyaan komunitas"
                })
        else:
            return jsonify({
                "message": "Gagal tidak menyukai (dislike) jawaban dari pertanyaan komunitas"
            })
    except Exception as e:
        return jsonify({"message": "Error terjadi", "error": str(e)}), 500

#######################################################################################
######################## Question Answer Community Endpoint ###########################
#######################################################################################

# Question Endpoint (Create, Edit dan Delete)
def new_q():
    user_identity = get_jwt_identity()
    datenow = datetime.now()
    
    users_id = user_identity.get("id")
    title_q = request.form["title_q"]
    description = request.form["description"]
    plant_types_id = request.form["plant_types_id"]
    img_q = request.files.get('img_q')
    like_num = 0
    released_date = datenow.strftime('%Y-%m-%d %H:%M:%S')  # Format: '2024-11-18 12:30:45'

    if not img_q:
        return jsonify({
            "message": "Gagal menambahkan data. Gambar tidak ditemukan."
        }), 400

    # Upload image menggunakan fungsi utility
    filename_img = image_uploaded.uploads_image(img_q)

    if not filename_img:
        return jsonify({
            "message": "Gagal mengunggah gambar."
        }), 500

    # Jika upload berhasil, lanjutkan menambahkan ke database
    add_q = Questions(
        title_q=title_q,
        description=description,
        like_num=like_num,
        users_id=users_id,
        plant_types_id=plant_types_id,
        released_date=released_date,
        img_q=f"https://agrolyn.online/static/uploads/{filename_img}"
    )

    db.session.add(add_q)
    db.session.commit()
    
    return jsonify({
        "message": "Sukses menambahkan data pertanyaan komunitas",
        "new_question": add_q.to_dict()
    }), 201


def update_q(question_id):
    # Ambil data pertanyaan berdasarkan ID
    question = Questions.query.get(question_id)
    if not question:
        return jsonify({
            "message": "Pertanyaan tidak ditemukan."
        }), 404

    # Ambil data dari form request
    title_q = request.form.get("title_q", question.title_q)
    description = request.form.get("description", question.description)
    plant_types_id = request.form.get("plant_types_id", question.plant_types_id)
    img_q = request.files.get('img_q')

    # Cek apakah gambar baru diupload
    if img_q:
        # Upload gambar baru
        filename_img = image_uploaded.update_image(img_q, question.img_q.split('/')[-1])
        if not filename_img:
            return jsonify({
                "message": "Gagal mengunggah gambar baru."
            }), 500
        # Update URL gambar baru
        question.img_q = f"https://agrolyn.online/static/uploads/{filename_img}"

    # Perbarui data pertanyaan
    question.title_q = title_q
    question.description = description
    question.plant_types_id = plant_types_id

    db.session.commit()

    return jsonify({
        "message": "Sukses memperbarui data pertanyaan",
        "updated_question": question.to_dict()
    }), 200

def delete_q(question_id):
    # Ambil data pertanyaan berdasarkan ID
    question = Questions.query.get(question_id)
    if not question:
        return jsonify({
            "message": "Pertanyaan tidak ditemukan."
        }), 404

    # Hapus gambar yang terkait dengan pertanyaan
    res = image_uploaded.delete_image(question.img_q.split('/')[-1])

    # Hapus pertanyaan dari database
    db.session.delete(question)
    db.session.commit()

    return jsonify({
        "message": "Sukses menghapus pertanyaan."
    }), 200

def new_ans(question_id):
    try:
        jwt_data = get_jwt_identity()
        data = request.get_json()
        datenow = datetime.now()

        answer = data.get("answer")
        plant_types_id = data.get("plant_types_id")
        users_id = jwt_data.get("id")

        # Validasi data
        if not answer or not users_id:
            return jsonify({"error": "Answer atau User ID tidak boleh kosong"}), 400

        if not question_id:
            return jsonify({"error": "Question ID tidak boleh kosong"}), 400

        released_date = datenow.strftime('%Y-%m-%d %H:%M:%S')  # Format: '2024-11-18 12:30:45'

        new_answer = Disccus(
            answer=answer,
            questions_id=question_id,
            plant_types_id=plant_types_id,
            like_num=0,
            users_id=users_id,
            released_date=released_date
        )

        db.session.add(new_answer)
        db.session.commit()

        return jsonify({"message": "Sukses Menambahkan Jawaban Atas Pertanyaan Komunitas"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Gagal menambahkan jawaban: {str(e)}"}), 500


def update_ans(answer_id):
    try:
        data = request.get_json()
        jwt_data = get_jwt_identity()
        user_id = jwt_data.get("id")

        answer = data.get("answer")

        # Validasi
        if not answer:
            return jsonify({"error": "Answer tidak boleh kosong"}), 400

        ans = Disccus.query.filter_by(id=answer_id, users_id=user_id).first()
        if not ans:
            return jsonify({"error": "Jawaban tidak ditemukan atau Anda tidak berhak mengubahnya"}), 404

        ans.answer = answer
        db.session.commit()

        return jsonify({"message": "Jawaban berhasil diperbarui"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Gagal memperbarui jawaban: {str(e)}"}), 500


def delete_ans(answer_id):
    try:
        jwt_data = get_jwt_identity()
        user_id = jwt_data.get("id")

        ans = Disccus.query.filter_by(id=answer_id, users_id=user_id).first()
        if not ans:
            return jsonify({"error": "Jawaban tidak ditemukan atau Anda tidak berhak menghapusnya"}), 404

        db.session.delete(ans)
        db.session.commit()

        return jsonify({"message": "Jawaban berhasil dihapus"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Gagal menghapus jawaban: {str(e)}"}), 500
