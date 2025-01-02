import os
from groq import Groq
from flask import jsonify, request

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