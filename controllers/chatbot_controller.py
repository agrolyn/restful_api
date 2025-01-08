from groq import Groq
import os
from flask import jsonify, request
import requests

def get_chatbot_res():
    data = request.get_json()
    prompt_user = data.get("prompt")

    client = Groq(
        # This is the default and can be omitted
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Nama kamu adalah AGROBOT yaitu chatbot cerdas dari aplikasi AGROLYN, kamu seorang chatbot yang berguna untuk menjawab pertanyaan terkait bidang agraria atau pertanian, selain pertanyaan tentang sektor pertanian tolong berikan penolakan, gunakan bahasa yang baik, santun, dan mudah dipahami."
            },
            {
                "role": "user",
                "content": prompt_user,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    if chat_completion:
        return jsonify({
            "message": "Sukses menampilkan hasil respon chatbot",
            "res_answer": chat_completion.choices[0].message.content
        }), 200

    return jsonify({
        "message": "Gagal menampilkan hasil respon chatbot",
    }), 404

def get_chatbot_llama_pretrained():
    data = request.get_json()
    prompt = data.get("prompt")

    chabot_api_url = "https://chatbot.linggashop.my.id/chatbot"
    payload = {"prompt": prompt}

    try:
        response = requests.post(chabot_api_url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        chatbot_res = response.json()
        res = chatbot_res.get("chat", "Tidak dapat memproses pertanyaan yang diajukan")

        return jsonify({
            "message": "Sukses menampilkan hasil respon chatbot llama pre-trained",
            "res_answer": res
        })
    except requests.RequestException as e:
        return jsonify({
            "status": "error",
            "message": "Kesalahan saat memproses analisis sentimen.",
            "error": str(e)
        }), 500
    