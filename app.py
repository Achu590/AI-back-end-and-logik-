from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)  # allow Flutter/mobile apps to access

# Initialize OpenAI client (for now keep hardcoded, later we can use os.getenv)
client = OpenAI(api_key="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")

# -------------------
# Endpoint: Analyze Sensor Data
# -------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Get JSON data
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Build prompt
        user_prompt = f"""
        You are a health assistant. Analyze the following stroke detector headphone sensor data and provide
        a clear, professional doctor-style explanation for the user:

        {data}
        """

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.6
        )

        ai_reply = response.choices[0].message.content.strip()
        return jsonify({"analysis": ai_reply})

    except Exception as e:
        # Better error details
        return jsonify({"error": "Failed to process request", "details": str(e)}), 500


# -------------------
# Extra Endpoint: Chat Assistant
# -------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful medical AI assistant."},
                {"role": "user", "content": question},
            ],
            max_tokens=200,
            temperature=0.7,
        )

        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": "Failed to process chat", "details": str(e)}), 500


# -------------------
# Health Check (to see if API is alive)
# -------------------
@app.route("/", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "Stroke Detector API"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
