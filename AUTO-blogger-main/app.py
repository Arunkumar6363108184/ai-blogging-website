import os
from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

print("GROQ KEY FOUND:", bool(os.environ.get("GROQ_API_KEY")))

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    topic = request.json.get("topic")

    chat = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"""
                Write a detailed, SEO-friendly blog on:
                "{topic}"

                Include:
                - Introduction
                - Headings
                - Conclusion
                """
            }
        ]
    )

    return jsonify({
        "blog": chat.choices[0].message.content
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
