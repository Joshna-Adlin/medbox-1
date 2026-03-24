from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "PASTE_YOUR_API_KEY_HERE"


@app.route('/')
def home():
    return render_template("voice.html")


def get_ai_response(text):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [
            {
                "role": "user",
                "content": f"Patient: {text}. Give condition and advice shortly."
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

    except:
        pass  # ignore API failure

    # 🔥 FALLBACK (ALWAYS WORKS)
    text = text.lower()

    if "chest" in text or "heart" in text:
        return "Possible heart issue. Please go to hospital immediately."

    elif "fever" in text and "cough" in text:
        return "Possible flu or infection. Take rest and drink fluids."

    elif "headache" in text:
        return "Could be stress or dehydration. Take rest."

    elif "vomiting" in text:
        return "Possible stomach problem. Stay hydrated."

    else:
        return "General illness. Please consult a doctor."


@app.route('/process', methods=['POST'])
def process():

    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"result": "No input received", "emergency": False})

    result = get_ai_response(text)

    return jsonify({
        "result": result,
        "emergency": "heart" in result.lower() or "hospital" in result.lower()
    })


if __name__ == "__main__":
    app.run(debug=True)