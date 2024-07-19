import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from api import send_answer

client = OpenAI(
    api_key='sk-proj-0JVE7hHtzn4s0viyhCaBT3BlbkFJt5XQJg8we3UhRAUHS9Mm'
)

app = Flask(__name__)


@app.get("/")
def index_get():
    return render_template("base.html")


@app.post("/nudge")
def nudge():
    message = {"answer": "Try asking for any information or typing 'What is the HR policy for Leaves?'"}
    return jsonify(message)


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = send_answer(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    os.system("replace_data.py")
