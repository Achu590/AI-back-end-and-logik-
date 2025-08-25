from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=("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")
)

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Get JSON data from Flutter app
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Format the sensor data for the AI
        user_prompt = f"""
        You are a health assistant. Analyze the following stroke detector headphone sensor data and provide
        a clear, professional doctor-style explanation for the user:

        {data}
        """

        # Send request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300
        )

        ai_reply = response.choices[0].message.content

        # Return AI response to Flutter
        return jsonify({"analysis": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
